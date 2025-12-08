# 🎵 Gaana Downloader

A powerful command-line tool to download high-quality MP3 songs from Gaana.com with an elegant interface and real-time progress tracking.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)

## ✨ Features

- 🎧 Download songs in multiple quality options (320kbps, 128kbps, 64kbps)
- 📝 Support for single songs, albums, and playlists
- 📊 Real-time download progress bar
- 🎨 Beautiful colored terminal interface
- 📁 Organized downloads with collection-based folders
- 🔄 Batch download support
- 💻 Cross-platform support (Windows, macOS, Linux)
- ⚡ Fast and efficient

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### 1. Python 3.6 or higher

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

**Install Python:**

- **Windows**: Download from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH" during installation
- **macOS**: Pre-installed or use `brew install python3`
- **Linux**: 
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

### 2. yt-dlp (YouTube-DL fork)

**Install using pip:**
```bash
# Windows
pip install yt-dlp

# macOS/Linux
pip3 install yt-dlp
```

**Or install globally:**
```bash
# Windows (PowerShell as Admin)
python -m pip install --user yt-dlp

# macOS/Linux
python3 -m pip install --user yt-dlp
```

**Verify installation:**
```bash
yt-dlp --version
```

### 3. FFmpeg (for audio conversion)

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Extract the ZIP file
3. Add `ffmpeg/bin` folder to System PATH
4. Or use Chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 4. Python Dependencies

Install required packages:
```bash
# Windows
pip install requests pycryptodome

# macOS/Linux
pip3 install requests pycryptodome
```

**Or use requirements.txt:**
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

## 📦 Installation

### Quick Start

1. **Download the script:**
   - Download `gaana.py` from this repository
   - Or clone: `git clone https://github.com/yourusername/gaana-downloader.git`

2. **Install dependencies:**
   ```bash
   # Windows
   pip install requests pycryptodome
   
   # macOS/Linux
   pip3 install requests pycryptodome
   ```

3. **Run the script:**
   ```bash
   # Windows
   python gaana.py
   
   # macOS/Linux
   python3 gaana.py
   ```

## 🚀 Usage

### Running the Program

**Windows (Command Prompt or PowerShell):**
```bash
python gaana.py
```

**macOS/Linux (Terminal):**
```bash
python3 gaana.py
```

### Step-by-Step Guide

1. **Start the program**
   - Open Terminal (macOS/Linux) or Command Prompt (Windows)
   - Navigate to the folder containing `gaana.py`
   - Run the command above

2. **Enter Gaana URL**
   - Paste any Gaana song, album, or playlist URL
   - Supported URL types:
     - **Song**: `https://gaana.com/song/bekhayali-1`
     - **Album**: `https://gaana.com/album/kabir-singh`
     - **Playlist**: `https://gaana.com/playlist/gaana-dj-bollywood-top-50`

3. **Select Tracks**
   - Type specific track numbers: `1,3,5`
   - Type `all` to download all tracks
   - Press Enter to download all tracks

4. **Choose Quality**
   - `1` = 320 kbps (Highest Quality - Recommended)
   - `2` = 128 kbps (Medium Quality)
   - `3` = 64 kbps (Lower Quality)

5. **Download Progress**
   - Watch the real-time progress bar
   - Files save to: `downloads/[Collection Name]/`

### Example Session

```
  ▒▒▒▒▒▒╗  ▒▒▒▒▒╗  ▒▒▒▒▒╗ ▒▒▒╗   ▒▒╗ ▒▒▒▒▒╗ 
 ▒▒╔═══╝ ▒▒╔══▒▒╗▒▒╔══▒▒╗▒▒▒▒╗  ▒▒║▒▒╔══▒▒╗
 ▒▒║  ▒▒▒╗▒▒▒▒▒▒▒║▒▒▒▒▒▒▒║▒▒╔▒▒╗ ▒▒║▒▒▒▒▒▒▒║
 ▒▒║   ▒▒║▒▒╔══▒▒║▒▒╔══▒▒║▒▒║╚▒▒╗▒▒║▒▒╔══▒▒║
 ╚▒▒▒▒▒▒╔╝▒▒║  ▒▒║▒▒║  ▒▒║▒▒║ ╚▒▒▒▒║▒▒║  ▒▒║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
            DOWNLOADER v3.0

URL: https://gaana.com/song/bekhayali-1

✓ Fetched: Bekhayali (1 tracks)
   1. Bekhayali [Sachet Tandon]

Select: (1,3,5 or 'all' or Enter=all)
Choice: all

Quality:
  1. 320 kbps
  2. 128 kbps
  3. 64 kbps
Choice: 1

⟳ Downloading 1 track(s)...

⟳ Bekhayali: [██████████████████████████████] 100.0%
✓ Bekhayali

✓ Done! Saved to: downloads/Bekhayali
```

## 📂 Output Structure

Downloads are organized automatically:

```
downloads/
└── Kabir Singh/
    ├── Bekhayali - Sachet Tandon.mp3
    ├── Tujhe Kitna Chahne Lage - Arijit Singh.mp3
    └── Kaise Hua - Vishal Mishra.mp3
```

## 🛠️ Troubleshooting

### Windows Issues

#### "python is not recognized"
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python39\python.exe gaana.py`

#### "pip is not recognized"
- Use: `python -m pip install package_name`

#### FFmpeg not found
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add new entry: `C:\ffmpeg\bin`
   - Restart Command Prompt

#### Permission errors
- Run Command Prompt as Administrator
- Or install packages with `--user` flag:
  ```bash
  pip install --user requests pycryptodome
  ```

### macOS/Linux Issues

#### "command not found: python"
- Use `python3` instead of `python`
- Create alias: `alias python=python3`

#### "command not found: pip"
- Use `pip3` instead of `pip`
- Or: `python3 -m pip install package_name`

#### Permission denied
```bash
# Make script executable
chmod +x gaana.py

# Run with explicit python
python3 gaana.py
```

#### FFmpeg not found (macOS)
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install ffmpeg
brew install ffmpeg
```

#### FFmpeg not found (Linux)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Common Issues (All Platforms)

#### "No tracks found"
- Verify the URL is correct
- Check if song/album is available in your region
- Try a different Gaana link

#### Download fails
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
# or
pip3 install --upgrade yt-dlp

# Clear cache
yt-dlp --rm-cache-dir
```

#### "ModuleNotFoundError: No module named 'Crypto'"
```bash
# Uninstall old crypto packages
pip uninstall crypto pycrypto

# Install pycryptodome
pip install pycryptodome
```

#### Colors not showing on Windows
- Use Windows Terminal (modern) instead of Command Prompt
- Or use PowerShell
- Download Windows Terminal from Microsoft Store

## 💡 Tips & Tricks

### Batch Download Multiple Songs
1. Create a text file with URLs (one per line)
2. Run the script multiple times, or modify it to read from file

### Best Quality Settings
- Always choose option `1` (320 kbps) for best audio quality
- Ensure you have enough disk space

### Faster Downloads
- Use a stable internet connection
- Close other downloads/streaming apps
- Update yt-dlp regularly: `pip install --upgrade yt-dlp`

## ⚙️ requirements.txt

Create a file named `requirements.txt` with:

```
requests>=2.28.0
pycryptodome>=3.15.0
```

Then install all dependencies at once:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! 

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⚖️ Legal Disclaimer

⚠️ **IMPORTANT**: This tool is for **educational purposes only**.

- Only download content you have the legal right to download
- Respect copyright laws in your country
- This tool does not condone piracy
- Support artists by subscribing to legal streaming services
- The developers are not responsible for misuse of this tool

**Use responsibly and legally.**

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤖 Development

This project was developed with the assistance of AI technologies:
- **Primary AI Assistants**: Claude (Anthropic) and ChatGPT (OpenAI)
- The code, structure, and documentation were collaboratively created using various AI engines
- Human oversight and testing ensured functionality and reliability

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful media downloader
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing
- [PyCryptodome](https://github.com/Legrandin/pycryptodome) - Cryptography library
- **AI Development**: Claude (Anthropic) and ChatGPT (OpenAI) for code generation and documentation

## 📞 Support

Having issues? 

1. Check the **Troubleshooting** section above
2. Ensure all prerequisites are installed correctly
3. Update yt-dlp: `pip install --upgrade yt-dlp`
4. Open an issue on GitHub with:
   - Your operating system (Windows/macOS/Linux)
   - Python version (`python --version`)
   - Complete error message
   - Steps to reproduce the problem

## 🌟 Star this Repository

If you find this tool helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ for music lovers**

*This is an unofficial tool and is not affiliated with Gaana or Times Internet Limited.*