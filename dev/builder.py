import hashlib
import os
import zipfile

def generate_manifest(target_dir, platform):
    print(f"--- Generating Manifest: {platform} ---")
    exclude_items = {'manifest.md5', '.setup_done', 'update_temp', '__pycache__', '.git', 'output'}
    if platform == "windows":
        exclude_items.add('dependencies')

    target_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in exclude_items]
        for file in files:
            if file in exclude_items:
                continue
            target_files.append(os.path.join(root, file))

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

def create_zip(target_dir, platform, builds_dir):
    zip_name = os.path.join(builds_dir, f"{platform}.zip")
    print(f"--- Zipping: {zip_name} ---")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            if any(ex in root.replace("\\", "/") for ex in ['__pycache__', '.git', 'output', 'update_temp']):
                continue
            for file in files:
                if platform == "windows" and "src/dependencies" in root.replace("\\", "/"):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, arcname)
    print(f"[OK] Build saved to {zip_name}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    builds_dir = os.path.join(root_dir, "builds")
    os.makedirs(builds_dir, exist_ok=True)

    choice = input("Select platform to build (1: Linux, 2: Windows, 3: Both): ").strip()
    platforms = []
    if choice == "1": platforms.append("linux")
    elif choice == "2": platforms.append("windows")
    elif choice == "3": platforms = ["linux", "windows"]
    else: return print("Invalid choice.")

    for p in platforms:
        target_path = os.path.abspath(os.path.join(root_dir, p))
        if os.path.exists(target_path):
            generate_manifest(target_path, p)
            create_zip(target_path, p, builds_dir)
        else:
            print(f"Error: {target_path} not found.")

if __name__ == "__main__":
    main()