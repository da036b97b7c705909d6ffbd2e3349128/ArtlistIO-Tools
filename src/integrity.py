import hashlib
import os

def check_integrity(manifest_name):
    """Check the integrity of files against the existing MD5 manifest."""
    if not os.path.exists(manifest_name):
        print(f"[ERROR] Manifest {manifest_name} does not exist.")
        return

    with open(manifest_name, "r") as f:
        saved_hashes = f.readlines()

    for line in saved_hashes:
        expected_hash, file_path = line.split(maxsplit=1)
        file_path = file_path.strip()
        
        if os.path.exists(file_path):
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    md5.update(chunk)
            current_hash = md5.hexdigest()

            if current_hash == expected_hash:
                print(f"[SUCCESS] {file_path} [{current_hash}]")
            else:
                print(f"[FAIL] {file_path} [{current_hash}]")
        else:
            print(f"[WARNING] {file_path} does not exist.")

def get_platform():
    versionpath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "version"))
    try:
        with open(versionpath, 'r') as file:
            lines = file.readlines()
            return lines[1]
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_integrity(f"manifest.{get_platform()}.md5")