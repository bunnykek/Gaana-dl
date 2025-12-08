#!/usr/bin/env python3
import base64
import json
import sys
import os
import subprocess
import requests
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# ===============================================================
# COLORS
# ===============================================================

class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


# ===============================================================
# AES DECRYPTION
# ===============================================================

def from_words(words):
    return b"".join(w.to_bytes(4, byteorder="big", signed=True) for w in words)


AES_KEY = from_words([1735995764, 593641578, 1814585892, 2004118885])


def decrypt_stream_path(stream_path: str) -> str:
    offset = int(stream_path[0])
    iv = stream_path[offset: offset + 16].encode("utf-8")
    ciphertext = base64.b64decode(stream_path[offset + 16:])
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode("utf-8")


# ===============================================================
# REDUX DATA EXTRACTOR
# ===============================================================

def extract_redux_data(html: str) -> dict:
    start = html.find("window.REDUX_DATA")
    if start == -1:
        raise ValueError("REDUX_DATA not found")

    brace_start = html.find("{", start)
    if brace_start == -1:
        raise ValueError("Opening brace not found")

    brace_count = 0
    json_str = ""
    in_string = False
    escape = False
    string_char = None

    for ch in html[brace_start:]:
        json_str += ch
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if not in_string:
            if ch == '"':
                in_string = True
                string_char = '"'
        elif ch == string_char:
            in_string = False
            string_char = None
        if not in_string:
            if ch == "{":
                brace_count += 1
            elif ch == "}":
                brace_count -= 1
                if brace_count == 0:
                    break

    return json.loads(json_str.replace("\\u002F", "/"))


# ===============================================================
# THUMBNAIL EXTRACTION
# ===============================================================

def extract_thumbnail_url(html: str) -> str:
    """Extract thumbnail URL from HTML meta tags or img tag"""
    # Try og:image first (best quality)
    og_pattern = r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'](https://[^"\']*)["\']'
    match = re.search(og_pattern, html)
    if match:
        return match.group(1)
    
    # Try twitter:image
    tw_pattern = r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\'](https://[^"\']*)["\']'
    match = re.search(tw_pattern, html)
    if match:
        return match.group(1)
    
    # Fallback to img tag
    img_pattern = r'<img src="(https://[^"]*gaanacdn\.com/[^"]*)"[^>]*alt="[^"]*"'
    match = re.search(img_pattern, html)
    if match:
        return match.group(1)
    
    return None


def get_track_thumbnail(track: dict) -> str:
    """Get thumbnail URL from track data"""
    # Try artworkLink first (higher quality)
    artwork = track.get("artworkLink") or track.get("artwork")
    if artwork:
        return artwork
    
    # Try artwork_large, artwork_medium
    for key in ["artwork_large", "artwork_web", "artwork"]:
        if track.get(key):
            return track[key]
    
    return None


def download_thumbnail(url: str, output_path: str) -> bool:
    """Download thumbnail image"""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        return False


# ===============================================================
# DATA EXTRACTION
# ===============================================================

def find_tracks(obj, tracks=None):
    if tracks is None:
        tracks = []
    if isinstance(obj, dict):
        if "track_title" in obj and "urls" in obj:
            tracks.append(obj)
        for v in obj.values():
            find_tracks(v, tracks)
    elif isinstance(obj, list):
        for item in obj:
            find_tracks(item, tracks)
    return tracks


def get_main_track(redux: dict):
    song = redux.get("song", {}).get("songDetail", {})
    if song and "track_title" in song and "urls" in song:
        return [song]
    tracks = redux.get("song", {}).get("tracks", [])
    if tracks and len(tracks) > 0:
        first_track = tracks[0]
        if "track_title" in first_track and "urls" in first_track:
            return [first_track]
    return None


def get_collection_name(redux: dict) -> str:
    pl_detail = redux.get("playlist", {}).get("playlistDetail", {})
    nested_pl = pl_detail.get("playlist", {})
    if nested_pl.get("title"):
        return str(nested_pl["title"])
    for k in ("title", "playlist_title", "playlistTitle", "name"):
        if pl_detail.get(k):
            return str(pl_detail[k])
    album = redux.get("album", {}).get("albumDetail", {})
    for k in ("title", "album_title", "name"):
        if album.get(k):
            return str(album[k])
    song = redux.get("song", {}).get("songDetail", {})
    for k in ("title", "track_title", "name"):
        if song.get(k):
            return str(song[k])
    tracks = redux.get("song", {}).get("tracks", [])
    if tracks and len(tracks) > 0:
        return tracks[0].get("track_title", "Unknown")
    return "Unknown"


def get_quality_url(track, quality_key):
    """Get URL for specified quality"""
    urls = track.get("urls") or {}
    url_entry = urls.get(quality_key)
    
    if url_entry and url_entry.get("message"):
        try:
            url = decrypt_stream_path(url_entry["message"])
            
            # For auto quality, replace 'f' with '320'
            if quality_key == "auto":
                url = url.replace("/f.mp4.master.m3u8", "/320.mp4.master.m3u8")
            
            return url
        except:
            pass
    
    return None


def sanitize_filename(name: str) -> str:
    bad = ['/', '\\', ':', '|', '?', '*', '<', '>', '"', "'"]
    for b in bad:
        name = name.replace(b, "_")
    return name.strip()


def embed_thumbnail(mp3_path: str, thumbnail_path: str, title: str, artist: str, album: str):
    """Embed thumbnail and metadata into MP3 using ffmpeg"""
    temp_output = mp3_path + ".temp.mp3"
    try:
        cmd = [
            "ffmpeg",
            "-i", mp3_path,
            "-i", thumbnail_path,
            "-map", "0:a",
            "-map", "1:0",
            "-c:a", "copy",
            "-c:v", "mjpeg",
            "-disposition:v", "attached_pic",
            "-metadata", f"title={title}",
            "-metadata", f"artist={artist}",
            "-metadata", f"album={album}",
            "-y",
            temp_output
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Replace original with embedded version
        if os.path.exists(temp_output):
            os.replace(temp_output, mp3_path)
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n{C.RED}FFmpeg error:{C.ENDC} {e.stderr}")
        # Clean up temp file if it exists
        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except:
                pass
        return False
    except Exception as e:
        print(f"\n{C.RED}Embed error:{C.ENDC} {str(e)}")
        # Clean up temp file if it exists
        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except:
                pass
        return False


def download_with_ytdlp(url: str, output_path: str, title: str, artist: str, album: str, thumbnail_url: str, output_dir: str):
    """Download audio"""
    try:
        # Download audio with progress
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--progress",
            "--newline",
            "-o", output_path,
            url
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        for line in process.stdout:
            line = line.strip()
            if line:
                # Check for download progress
                if '[download]' in line and '%' in line:
                    # Extract percentage
                    if 'of' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if '%' in part:
                                percent = part.strip('%')
                                try:
                                    pct = float(percent)
                                    bar_length = 30
                                    filled = int(bar_length * pct / 100)
                                    bar = '█' * filled + '░' * (bar_length - filled)
                                    print(f"\r{C.YELLOW}⟳{C.ENDC} {title}: [{bar}] {pct:.1f}%", end='', flush=True)
                                except:
                                    pass
                                break
                elif '[ExtractAudio]' in line or 'Deleting original file' in line:
                    print(f"\r{C.YELLOW}⟳{C.ENDC} {title}: Converting to MP3...{' '*20}", end='', flush=True)
        
        process.wait()
        
        if process.returncode != 0:
            return False
        
        # Find the actual output file
        base_name = os.path.splitext(output_path)[0]
        mp3_file = base_name + ".mp3"
        
        if not os.path.exists(mp3_file):
            return False
        
        return True
    except Exception as e:
        print(f"\n{C.RED}Error:{C.ENDC} {str(e)}")
        return False


# ===============================================================
# MAIN
# ===============================================================

def main():
    print(f"""{C.CYAN}{C.BOLD}
  ▒▒▒▒▒▒╗  ▒▒▒▒▒╗  ▒▒▒▒▒╗ ▒▒▒╗   ▒▒╗ ▒▒▒▒▒╗ 
 ▒▒╔═══╝ ▒▒╔══▒▒╗▒▒╔══▒▒╗▒▒▒▒╗  ▒▒║▒▒╔══▒▒╗
 ▒▒║  ▒▒▒╗▒▒▒▒▒▒▒║▒▒▒▒▒▒▒║▒▒╔▒▒╗ ▒▒║▒▒▒▒▒▒▒║
 ▒▒║   ▒▒║▒▒╔══▒▒║▒▒╔══▒▒║▒▒║╚▒▒╗▒▒║▒▒╔══▒▒║
 ╚▒▒▒▒▒▒╔╝▒▒║  ▒▒║▒▒║  ▒▒║▒▒║ ╚▒▒▒▒║▒▒║  ▒▒║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
            DOWNLOADER v3.0{C.ENDC}
""")
    
    url = input(f"{C.BOLD}URL:{C.ENDC} ").strip()
    if not url:
        print(f"{C.RED}✗ No URL{C.ENDC}")
        return
    
    print(f"\n{C.YELLOW}⟳{C.ENDC} Fetching...", end="", flush=True)
    
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        html = resp.text
        redux = extract_redux_data(html)
        thumbnail_url = extract_thumbnail_url(html)
        
        is_song_page = "/song/" in url
        
        if is_song_page:
            tracks = get_main_track(redux)
            if not tracks:
                all_tracks = find_tracks(redux)
                tracks = [all_tracks[0]] if all_tracks else []
        else:
            tracks = find_tracks(redux)
        
        collection_name = get_collection_name(redux)
        
        if collection_name == "Unknown":
            url_parts = url.rstrip('/').split('/')
            if len(url_parts) > 0:
                collection_name = url_parts[-1].replace('-', ' ').title()
        
        print(f"\r{C.GREEN}✓{C.ENDC} Fetched: {C.CYAN}{collection_name}{C.ENDC} ({len(tracks)} tracks)")
    except Exception as e:
        print(f"\r{C.RED}✗{C.ENDC} Error: {e}")
        return
    
    if not tracks:
        print(f"{C.RED}✗ No tracks{C.ENDC}")
        return
    
    # Show tracks
    print()
    for i, t in enumerate(tracks, 1):
        title = t.get("track_title", "Unknown")
        artists = ", ".join(a.get("name", "") for a in t.get("artist", []))
        print(f"  {C.DIM}{i:2d}.{C.ENDC} {title} {C.DIM}[{artists}]{C.ENDC}")
    
    # Select tracks
    print(f"\n{C.BOLD}Select:{C.ENDC} {C.DIM}(1,3,5 or 'all' or Enter=all){C.ENDC}")
    sel = input(f"{C.BOLD}Choice:{C.ENDC} ").strip().lower()
    
    if not sel or sel == "all":
        indices = list(range(len(tracks)))
    else:
        indices = []
        for part in sel.split(","):
            try:
                n = int(part.strip())
                if 1 <= n <= len(tracks):
                    indices.append(n - 1)
            except:
                pass
    
    if not indices:
        print(f"{C.RED}✗ No selection{C.ENDC}")
        return
    
    # Choose quality
    print(f"\n{C.BOLD}Quality:{C.ENDC}")
    print(f"  {C.DIM}1.{C.ENDC} 320 kbps")
    print(f"  {C.DIM}2.{C.ENDC} 128 kbps")
    print(f"  {C.DIM}3.{C.ENDC} 64 kbps")
    quality = input(f"{C.BOLD}Choice:{C.ENDC} ").strip()
    
    quality_map = {"1": "auto", "2": "high", "3": "medium"}
    quality_key = quality_map.get(quality, "auto")
    
    output_dir = f"downloads/{sanitize_filename(collection_name)}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{C.YELLOW}⟳{C.ENDC} Downloading {len(indices)} track(s)...\n")
    
    for idx in indices:
        track = tracks[idx]
        title = track.get("track_title", "Unknown")
        artists = ", ".join(a.get("name", "") for a in track.get("artist", []))
        album = track.get("album_title", "")
        
        # Try to get track-specific thumbnail first, fallback to page thumbnail
        track_thumbnail = get_track_thumbnail(track)
        thumb_to_use = track_thumbnail if track_thumbnail else thumbnail_url
        
        url_to_download = get_quality_url(track, quality_key)
        
        if not url_to_download:
            print(f"{C.RED}✗{C.ENDC} {title} - No URL")
            continue
        
        safe_title = sanitize_filename(f"{title} - {artists}")
        output_path = f"{output_dir}/{safe_title}.%(ext)s"
        
        print(f"{C.YELLOW}⟳{C.ENDC} {title}...", end="", flush=True)
        
        if download_with_ytdlp(url_to_download, output_path, title, artists, album, thumb_to_use, output_dir):
            print(f"\r{C.GREEN}✓{C.ENDC} {title}")
        else:
            print(f"\r{C.RED}✗{C.ENDC} {title}")
    
    print(f"\n{C.GREEN}✓{C.ENDC} Done! Saved to: {C.YELLOW}{output_dir}{C.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}⚠ {C.ENDC} Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}✗{C.ENDC} Error: {e}")
        sys.exit(1)