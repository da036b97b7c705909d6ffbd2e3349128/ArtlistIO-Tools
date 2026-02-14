# ArtlistIO Tools
ArtlistIO is a simple tool to extract and convert `.m3u8` streams from websites to MP4 using FFmpeg and Playwright.

> [!NOTE]
> While this may/may not work for ArtlistIO, most stock-footage sites follow the same format, so it should theoretically work for other sites.

> [!CAUTION]
> If you dont want to be held responsible for pirating stock footage, buy an artlist.io (or any provider) license at [their plans and pricing page](https://artlist.io/page/pricing/max).
> You are adviced to  [terms of service](https://artlist.io/help-center/privacy-terms/terms-of-use/) and understand how you are violating them.

> [!WARNING]
> This is for educational purposes only.
> By continuing to use this, you accept the risks, and acknowledge that you have been warned.


&nbsp;

## Usage

- **Windows**
To start the application, run the provided `start.bat`.

- **Linux/MacOS**

# Curl (Recommended)
Run this command in your terminal:
```bash
mkdir artlist-tools && cd artlist-tools && curl -LJO $(curl -s https://api.github.com/repos/da036b97b7c705909d6ffbd2e3349128/ArtlistIO-Tools/releases/latest | grep -o "https://.*linux.zip") && unzip linux.zip && chmod +x start.sh && ./start.sh
```

# Downloading zip file
If you have already downloaded the ZIP file, open the terminal inside the file's directory and run:
Run `mkdir artlist-tools && cd artlist-tools && unzip linux.zip && chmod +x start.sh && ./start.sh`


&nbsp;

## Features

- ArtlistIO Stock Footage Downloader (4k, HD, 720p, 380p, 240p).
- ArtlistIO SFX/Music Footage Downloader (custom bitrate supported).
- Update option in UI.


&nbsp;

---

[License](LICENSE)

Mu_rpy © 2026









