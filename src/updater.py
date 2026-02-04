import requests

def check_remote_updates(owner, repo_name, branch='main'):
    """Checks the latest commit SHA of a remote GitHub repository."""
    url = f"https://api.github.com{owner}/{repo_name}/commits/{branch}"

    response = requests.get(url)

    if response.status_code == 200:
        latest_commit_sha = response.json().get("sha")
        print(f"Latest commit SHA on {branch} is: {latest_commit_sha}")
        return latest_commit_sha
    else:
        print(f"Failed to retrieve information: Status code {response.status_code}")
        return None

if __name__ == "main":
    check_remote_updates('da036b97b7c705909d6ffbd2e3349128', 'ArtlistIO-Tools')
    