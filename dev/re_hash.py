import subprocess
import os

def update_version_and_push():
    commit_msg = input("commit name: ")
    
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    
    version_path = os.path.join("src", "version")
    
    with open(version_path, "r") as f:
        lines = f.readlines()
    
    while len(lines) < 3:
        lines.append("\n")
    
    lines[2] = commit_hash + "\n"
        
    with open(version_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    update_version_and_push()