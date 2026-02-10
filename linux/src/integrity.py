import hashlib
import os

def check_integrity(manifest_name):
    manifest_path = os.path.normpath(manifest_name)
    if not os.path.exists(manifest_path):
        print(f"[ERROR] Manifest {manifest_path} does not exist.")
        return False

    with open(manifest_path, "r") as f:
        saved_hashes = f.readlines()

    all_passed = True
    for line in saved_hashes:
        expected_hash, file_path = line.split(maxsplit=1)
        file_path = os.path.normpath(file_path.strip())
        
        if os.path.exists(file_path):
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    md5.update(chunk)
            current_hash = md5.hexdigest()

            if current_hash == expected_hash:
                print(f"[SUCCESS] {file_path}")
            else:
                print(f"[FAIL] {file_path} (Hash Mismatch)")
                all_passed = False
        else:
            print(f"[WARNING] {file_path} missing.")
            all_passed = False
    return all_passed

if __name__ == "__main__":
    manifest = os.path.join("src", "data", "manifest.md5")
    if not check_integrity(manifest):
        exit(1)