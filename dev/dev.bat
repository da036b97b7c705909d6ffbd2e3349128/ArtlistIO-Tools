import subprocess
import os

def update_version_and_push():
    v_num = input("version: ")
    commit_msg = input("commit name: ")
    
    version_path = "VERSION"
    old_version_path = os.path.join("src", "version")

    if os.path.exists(version_path):
        os.remove(version_path)
    if os.path.exists(old_version_path):
        os.remove(old_version_path)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    actual_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    with open(version_path, "w") as f:
        f.write(f"{v_num}\nwindows\n{actual_hash}\n")

    subprocess.run(["git", "add", version_path], check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], check=True)
    subprocess.run(["git", "push", "origin", "main", "--force"], check=True)

if __name__ == "__main__":
    update_version_and_push()