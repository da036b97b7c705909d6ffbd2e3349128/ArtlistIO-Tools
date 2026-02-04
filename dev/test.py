import subprocess
import os

def test_version_logic():
    v_num = input("version: ")
    
    version_path = "VERSION"
    old_version_path = os.path.join("src", "version")

    if os.path.exists(version_path):
        os.remove(version_path)
    if os.path.exists(old_version_path):
        os.remove(old_version_path)

    # Use 'rev-parse' on the current state just to simulate the hash
    current_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    with open(version_path, "w") as f:
        f.write(f"{v_num}\nwindows\n{current_hash}\n")
    
    print(f"\n--- TEST COMPLETE ---")
    print(f"File '{version_path}' created with content:")
    with open(version_path, "r") as f:
        print(f.read())
    print("No git commands were pushed.")

if __name__ == "__main__":
    test_version_logic()