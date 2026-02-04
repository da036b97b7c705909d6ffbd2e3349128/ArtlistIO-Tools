import hashlib
import os
import json
import platform

def get_platform_suffix():
    system = platform.system().lower()
    if system == "windows": return "win"
    if system == "darwin": return "mac"
    if system == "linux": return "ubuntu"
    return "unknown"

def generate_manifest():
    suffix = get_platform_suffix()
    manifest_name = f"manifest-{suffix}.json"
    hashes = {}
    
    files_to_hash = [
        "src/artlistio-vid.py", 
        "src/artlistio-sfx.py", 
        "src/updater.py",
        "start.bat"
    ]
    
    for file_path in files_to_hash:
        if os.path.exists(file_path):
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha256.update(chunk)
            hashes[file_path] = sha256.hexdigest()

    with open(manifest_name, "w") as f:
        json.dump(hashes, f, indent=4)
    print(f"[SUCCESS] Created {manifest_name} in root directory.")

if __name__ == "__main__":
    generate_manifest()