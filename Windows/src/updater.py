import requests
import os
import subprocess
import zipfile
import io
import sys

def get_local_version():
    version_path = os.path.join("src", "data", "version")
    if os.path.exists(version_path):
        with open(version_path, "r") as f:
            return f.read().strip()
    return ""

def check_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            tag = data.get("tag_name")
            assets = data.get("assets", [])
            for asset in assets:
                if "win" in asset.get("name").lower():
                    return tag, asset.get("browser_download_url")
    except Exception:
        pass
    return None, None

def run_update(dl_url, new_tag):
    r = requests.get(dl_url)
    if r.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall("update_temp")
        
        v_dir = os.path.join("update_temp", "src", "data")
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "version"), "w") as f:
            f.write(new_tag)

        with open("finish_update.bat", "w") as f:
            f.write(f"""@echo off
timeout /t 3 /nobreak > nul
del /f /q "src\\data\\.setup_done"
xcopy /s /y "update_temp\\*" "."
rd /s /q "update_temp"
echo Update complete.
start start.bat
del "%~f0"
""")
        
        subprocess.Popen(["finish_update.bat"], shell=True)
        sys.exit()

if __name__ == "__main__":
    OWNER = 'da036b97b7c705909d6ffbd2e3349128'
    REPO = 'ArtlistIO-Tools'
    
    remote_tag, dl_url = check_latest_release(OWNER, REPO)
    local_tag = get_local_version()

    if remote_tag and remote_tag != local_tag:
        print(f"Updating: {local_tag} -> {remote_tag}")
        run_update(dl_url, remote_tag)
    else:
        print("ArtlistIO Tools are up to date.")