import hashlib
import os

def generate():
    print("--- Automatic Manifest Generator (Linux) ---")
    target_dir = "../linux"
    exclude_items = {'manifest.md5', '.setup_done', 'update_temp', '__pycache__', '.git', 'output'}
    target_files = []

    if not os.path.exists(target_dir):
        print(f"Error: Target directory {target_dir} not found.")
        return

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in exclude_items]
        for file in files:
            if file in exclude_items:
                continue
            file_path = os.path.join(root, file)
            target_files.append(file_path)

    if not target_files:
        print("No files found. Exiting.")
        return

    output_path = os.path.join(target_dir, "src", "data", "manifest.md5")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        for file_path in sorted(target_files):
            md5 = hashlib.md5()
            with open(file_path, "rb") as rb:
                while chunk := rb.read(4096):
                    md5.update(chunk)
            hash_val = md5.hexdigest()
            clean_path = os.path.relpath(file_path, target_dir).replace("\\", "/")
            f.write(f"{hash_val} {clean_path}\n")
            print(f"Hashed: {clean_path}")

    print(f"\n[OK] Manifest saved to {output_path} ({len(target_files)} files indexed)")

if __name__ == "__main__":
    generate()
