import requests
from datetime import datetime

base_url = # Kullanıcı adı ve şifrenizi girin
auth = # Kullanıcı adı ve şifrenizi girin

# Tüm projeleri al
projects_response = requests.get(f"{base_url}/projects", auth=auth)
projects = projects_response.json()["values"]

# Depo ve commit bilgilerini saklamak için bir liste
repo_commit_data = []

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
            if commits:
                last_commit = commits[0]
                # authorTimestamp'i okunabilir formata dönüştür
                timestamp = last_commit['authorTimestamp'] // 1000  # Milisaniyeden saniyeye çevir
                readable_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                author_name = last_commit['author']['name']  # Commit'i yapan kişi
                repo_commit_data.append({
                    "repo_name": repo["name"],
                    "project_name": project["name"],
                    "last_commit_date": readable_date,
                    "author": author_name,
                    "timestamp": timestamp
                })
            else:
                repo_commit_data.append({
                    "repo_name": repo["name"],
                    "project_name": project["name"],
                    "last_commit_date": "No Commits Found",
                    "author": "Unknown",
                    "timestamp": 0
                })
        else:
            repo_commit_data.append({
                "repo_name": repo["name"],
                "project_name": project["name"],
                "last_commit_date": "No Commit Data Returned",
                "author": "Unknown",
                "timestamp": 0
            })

# Depoları en son güncellenme tarihine göre sıralama
repo_commit_data.sort(key=lambda x: x["timestamp"], reverse=True)

# Sıralanmış sonuçları yazdırma
for data in repo_commit_data:
    print(f"Project: {data['project_name']}, Repo: {data['repo_name']}, Last Commit Date: {data['last_commit_date']}, Author: {data['author']}")
