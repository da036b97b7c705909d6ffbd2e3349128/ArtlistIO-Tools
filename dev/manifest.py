import hashlib
import os

def generate_manifest(suffix):
    base_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.normpath(os.path.join(base_path, ".."))
    hashes = []

    files_to_hash = [
        os.path.join(root_path, "src", "artlistio-vid.py"),
        os.path.join(root_path, "src", "artlistio-sfx.py"),
        os.path.join(root_path, "src", "updater.py"),
        os.path.join(root_path, "src", "integrity.py"),
        os.path.join(root_path, "Pipfile.lock"),
        os.path.join(root_path, "Pipfile"),
        os.path.join(root_path, "start.bat"),
        os.path.join(root_path, "LICENSE"),
    ]
    
    for file_path in files_to_hash:
        if os.path.exists(file_path):
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    md5.update(chunk)
            hashes.append(f"{md5.hexdigest()} {file_path}")

    with open(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dev", "manifests", f"manifest.{suffix}.md5")), "w") as f:
        f.write("\n".join(hashes))
        f.close()
    print(f"[SUCCESS] Created manifest.{suffix}.md5 in root directory.")

    with open(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "manifest.md5")), "w") as f:
        f.write("\n".join(hashes))
        f.close
    print(f"[SUCCESS] Created manifest.md5 in root directory.")

def get_platform():
    versionpath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "version"))
    try:
        with open(versionpath, 'r') as file:
            lines = file.readlines()
            return lines[1]
    except Exception as e:
        print(e)

if __name__ == "__main__":
    generate_manifest(get_platform())