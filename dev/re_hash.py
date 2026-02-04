import subprocess
import os

def update_version_and_push():
    commit_msg = input("commit name: ")
    version_path = os.path.join("src", "version")

    subprocess.run(["git", "add", "."], check=True)

    with open(version_path, "r") as f:
        lines = f.readlines()

    while len(lines) < 3:
        lines.append("\n")

    lines[2] = "TEMP_HASH\n"

    with open(version_path, "w") as f:
        f.writelines(lines)

    subprocess.run(["git", "add", version_path], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    actual_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    lines[2] = actual_hash + "\n"

    with open(version_path, "w") as f:
        f.writelines(lines)

    subprocess.run(["git", "add", version_path], check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], check=True)
    subprocess.run(["git", "push", "origin", "main", "--force"], check=True)

if __name__ == "__main__":
    update_version_and_push()