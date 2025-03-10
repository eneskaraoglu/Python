import requests
from datetime import datetime

base_url = # Kullanıcı adı ve şifrenizi girin
auth =  # Kullanıcı adı ve şifrenizi girin

# Tüm projeleri al
projects_response = requests.get(f"{base_url}/projects", auth=auth)
projects = projects_response.json()["values"]

# Kullanıcıların en son commit bilgilerini saklamak için bir sözlük
user_last_commit = {}

# Her projedeki depoları sorgula
for project in projects:
    project_key = project["key"]
    repos_response = requests.get(f"{base_url}/projects/{project_key}/repos", auth=auth)
    repos = repos_response.json()["values"]
    
    for repo in repos:
        repo_slug = repo["slug"]
        # Her depo için commit bilgisi al
        commits_response = requests.get(f"{base_url}/projects/{project_key}/repos/{repo_slug}/commits", auth=auth)
        
        if commits_response.status_code == 200 and "values" in commits_response.json():
            commits = commits_response.json()["values"]
            for commit in commits:
                author = commit["author"]["name"]
                timestamp = commit["authorTimestamp"] // 1000  # Milisaniyeden saniyeye çevir
                readable_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                # Kullanıcı daha önce kaydedilmiş mi kontrol et
                if author not in user_last_commit or user_last_commit[author]["timestamp"] < timestamp:
                    user_last_commit[author] = {
                        "project_name": project["name"],
                        "repo_name": repo["name"],
                        "last_commit_date": readable_date,
                        "timestamp": timestamp
                    }

# Kullanıcıları en son commit zamanına göre sıralama
sorted_users = sorted(user_last_commit.items(), key=lambda x: x[1]["timestamp"], reverse=True)

# Sıralanmış sonuçları yazdırma
for user, data in sorted_users:
    print(f"User: {user}, Project: {data['project_name']}, Repo: {data['repo_name']}, Last Commit Date: {data['last_commit_date']}")
