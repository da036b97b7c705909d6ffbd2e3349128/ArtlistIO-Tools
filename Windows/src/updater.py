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
            lines = f.readlines()
            return lines[0].strip() if lines else ""
    return ""

def check_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("tag_name"), data.get("zipball_url")
    except Exception as e:
        print(f"Connection error: {e}")
    return None, None

def run_update(zip_url, new_tag):
    r = requests.get(zip_url)
    if r.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall("update_temp")
        
        internal_dir = os.path.join("update_temp", os.listdir("update_temp")[0])
        
        version_path = os.path.join("src", "data", "version")
        full_version_path = os.path.join(internal_dir, version_path)
        
        if os.path.exists(full_version_path):
            with open(full_version_path, "r") as f:
                content = f.readlines()
            content[0] = f"{new_tag}\n"
            with open(full_version_path, "w") as f:
                f.writelines(content)

        with open("finish_update.bat", "w") as f:
            f.write(f"""@echo off
timeout /t 2 /nobreak > nul
xcopy /s /y "{internal_dir}\\*" "."
rd /s /q "update_temp"
start start.bat
del "%~f0"
""")
        
        subprocess.Popen(["finish_update.bat"], shell=True)
        sys.exit()

if __name__ == "__main__":
    OWNER = 'da036b97b7c705909d6ffbd2e3349128'
    REPO = 'ArtlistIO-Tools'
    
    remote_tag, zip_url = check_latest_release(OWNER, REPO)
    local_tag = get_local_version()

    if remote_tag and remote_tag != local_tag:
        print(f"New version found: {remote_tag} (Current: {local_tag})")
        run_update(zip_url, remote_tag)
    else:
        print("ArtlistIO Tools are up to date.")