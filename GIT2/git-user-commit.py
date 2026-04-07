import requests
from datetime import datetime, timedelta

# CONFIGURATION
# base_url = "https://your-bitbucket-url/rest/api/1.0"
# auth = ("your-username", "your-password")
# target_user = "target.username"

base_url = "http://bitbucket.bilisim.com.tr/rest/api/1.0"
auth = ("eneskaraoglu", "4321QWER")  # or use personal access token
target_user = "msedat"  # replace with the user you're tracking
project_key = "ERP"  # Only this project

# DATE RANGE: 1–2 years ago
now = datetime.now()
two_years_ago = now - timedelta(days=730)

user_commits = []

print(f"\n--- Fetching repositories from project: {project_key} ---")

# Get repositories only for project_key='ERP'
repos_response = requests.get(f"{base_url}/projects/{project_key}/repos", auth=auth)
repos = repos_response.json().get("values", [])

for repo in repos:
    repo_slug = repo["slug"]
    print(f"Checking repo: {repo_slug}")
    start = 0
    is_last_page = False

    while not is_last_page:
        commits_url = (
            f"{base_url}/projects/{project_key}/repos/{repo_slug}/commits?start={start}"
        )
        commits_response = requests.get(commits_url, auth=auth)

        if commits_response.status_code != 200:
            print(f"Failed to get commits from {repo_slug}")
            break

        commits_data = commits_response.json()
        commits = commits_data.get("values", [])

        print(f"  {len(commits)} commits fetched...")

        for commit in commits:
            author_name = commit["author"]["name"]
            if author_name != target_user:
                continue

            timestamp = commit["authorTimestamp"] // 1000
            commit_date = datetime.fromtimestamp(timestamp)

            if two_years_ago <= commit_date:
                print(f"    ✅ Match: {commit_date.strftime('%Y-%m-%d')} - {commit['message'][:50]}")
                user_commits.append({
                    "date": commit_date.strftime('%Y-%m-%d'),
                    "repo": repo["name"],
                    "message": commit["message"]
                })

        is_last_page = commits_data.get("isLastPage", True)
        if not is_last_page:
            start = commits_data.get("nextPageStart", 0)

# Final output
print(f"\n--- FOUND {len(user_commits)} COMMITS in project {project_key} ---")
for commit in user_commits:
    print(f"[{commit['date']}] Repo: {commit['repo']} | Message: {commit['message']}")
