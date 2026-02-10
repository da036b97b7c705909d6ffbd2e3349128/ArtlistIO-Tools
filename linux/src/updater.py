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
                if "linux" in asset.get("name").lower():
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

        finish_script = "finish_update.sh"
        content = f"""#!/bin/bash
sleep 3
cp -rf update_temp/* .
rm -rf update_temp
chmod +x start.sh
echo "Update complete. Restarting..."
rm src/data/.setup_done
./start.sh
rm -- "$0"
"""
        
        with open(finish_script, "w") as f:
            f.write(content)
        
        os.chmod(finish_script, 0o755)
        
        subprocess.Popen(["nohup", "/bin/bash", f"./{finish_script}"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         start_new_session=True)
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