import subprocess
import os

def update_version_and_push():
    v_num = input("version: ")
    commit_msg = input("commit name: ")
    
    target_dir = os.path.join("src", "data")
    version_path = os.path.join(target_dir, "VERSION")
    
    # Paths to clean up
    old_paths = [
        "VERSION",
        os.path.join("src", "version"),
        os.path.join("src", "VERSION"),
        os.path.join("VERSION"),
        os.path.join("version"),
    ]

    for path in old_paths:
        if os.path.exists(path):
            os.remove(path)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    actual_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    os.makedirs(target_dir, exist_ok=True)
    with open(version_path, "w") as f:
        f.write(f"{v_num}\nwindows\n{actual_hash}\n")

    subprocess.run(["git", "add", version_path], check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], check=True)
    subprocess.run(["git", "push", "origin", "main", "--force"], check=True)

if __name__ == "__main__":
    update_version_and_push()