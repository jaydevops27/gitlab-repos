import requests
import json

def get_commits(gitlab_url, token, project_id):
    headers = {'PRIVATE-TOKEN': token}
    url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            print(f"{commit['short_id']} - {commit['title']} - {commit['author_name']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Usage
get_commits('https://gitlab.com', 'your_token', 'your_project_id')
