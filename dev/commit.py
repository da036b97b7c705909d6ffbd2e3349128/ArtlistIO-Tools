import subprocess
import os

def get_next_version(debug=False):
    version_path = os.path.join("src", "data", "version")
    if os.path.exists(version_path) and not debug:
        with open(version_path, "r") as f:
            current = f.readline().strip()
            if current.startswith('v'):
                parts = current[1:].split('.')
                parts[-1] = str(int(parts[-1]) + 1)
                return f"v{'.'.join(parts)}"
    return "developement"

def update_version_and_push():
    new_v = get_next_version(True)

    commit_msg = input(f"New version will be {new_v}. Commit message: ").strip()
    
    target_dir = os.path.join("src", "data")
    version_path = os.path.join(target_dir, "version")
    
    os.makedirs(target_dir, exist_ok=True)
    with open(version_path, "w") as f:
        f.write(f"{new_v}\nwindows\n")

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"{new_v}: {commit_msg}"], check=True)
        subprocess.run(["git", "tag", "-f", "-a", new_v, "-m", f"Release {new_v}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "--force", new_v], check=True)
        print(f"\nSuccessfully deployed {new_v}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_version_and_push()
