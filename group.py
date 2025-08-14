import csv
from datetime import datetime

def export_group_commits_to_csv(gitlab_url, token, group_id, filename='commits_export.csv'):
    headers = {'PRIVATE-TOKEN': token}
    
    # Get all projects
    projects_url = f"{gitlab_url}/api/v4/groups/{group_id}/projects"
    projects_response = requests.get(projects_url, headers=headers, verify=False)
    projects = projects_response.json()
    
    # Prepare CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['project_name', 'commit_id', 'short_id', 'title', 'author_name', 'author_email', 'created_at', 'web_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for project in projects:
            project_name = project['name']
            project_id = project['id']
            
            # Get commits
            commits_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
            commits_response = requests.get(commits_url, headers=headers, params={'per_page': 50}, verify=False)
            
            if commits_response.status_code == 200:
                commits = commits_response.json()
                
                for commit in commits:
                    writer.writerow({
                        'project_name': project_name,
                        'commit_id': commit['id'],
                        'short_id': commit['short_id'],
                        'title': commit['title'],
                        'author_name': commit['author_name'],
                        'author_email': commit['author_email'],
                        'created_at': commit['created_at'],
                        'web_url': commit['web_url']
                    })
    
    print(f"✅ Commits exported to {filename}")

# Usage
export_group_commits_to_csv('https://gitlab.yourcompany.com', 'your_token', 'your_group_id')
