import hashlib
import os
import json
import platform

def check_integrity(manifest_name):
    """Check the integrity of files against the existing manifest."""
    if not os.path.exists(manifest_name):
        print(f"[ERROR] Manifest {manifest_name} does not exist.")
        return

    with open(manifest_name, "r") as f:
        saved_hashes = json.load(f)

    for file_path, expected_hash in saved_hashes.items():
        if os.path.exists(file_path):
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha256.update(chunk)
            current_hash = sha256.hexdigest()

            if current_hash == expected_hash:
                print(f"[SUCCESS] {file_path} integrity verified.")
            else:
                print(f"[WARNING] {file_path} integrity check failed: "
                      f"expected {expected_hash}, found {current_hash}.")
        else:
            print(f"[WARNING] {file_path} does not exist.")

if __name__ == "__main__":
    generate_manifest()
    suffix = get_platform_suffix()
    manifest_name = f"manifest-{suffix}.json"
    check_integrity(manifest_name)
