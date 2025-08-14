import requests
import csv
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def export_nested_group_commits_to_csv(gitlab_url, token, root_group_id, filename='all_commits_export.csv'):
    headers = {'PRIVATE-TOKEN': token}
    
    try:
        # Get all projects including subgroups recursively
        print(f"🔍 Searching for all projects under root group ID: {root_group_id}")
        
        projects_url = f"{gitlab_url}/api/v4/groups/{root_group_id}/projects"
        
        # Use include_subgroups=true to get projects from nested groups
        all_projects = []
        page = 1
        
        while True:
            params = {
                'include_subgroups': 'true',  # This is the key parameter!
                'per_page': 100,
                'page': page
            }
            
            projects_response = requests.get(projects_url, headers=headers, params=params, verify=False)
            
            if projects_response.status_code != 200:
                print(f"Error getting projects: {projects_response.status_code} - {projects_response.text}")
                return
            
            projects = projects_response.json()
            if not projects:  # No more projects
                break
                
            all_projects.extend(projects)
            page += 1
        
        print(f"📊 Found {len(all_projects)} total projects (including nested ones)")
        
        # Group projects by their namespace for better organization
        projects_by_group = {}
        for project in all_projects:
            group_name = project['namespace']['full_path']
            if group_name not in projects_by_group:
                projects_by_group[group_name] = []
            projects_by_group[group_name].append(project)
        
        print(f"📁 Projects organized across {len(projects_by_group)} groups/namespaces")
        
        # Prepare CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['group_path', 'project_name', 'project_path', 'commit_id', 'short_id', 'title', 'author_name', 'author_email', 'created_at', 'web_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            total_commits = 0
            
            for group_path, projects in projects_by_group.items():
                print(f"\n{'='*80}")
                print(f"📂 GROUP: {group_path}")
                print(f"{'='*80}")
                
                for project in projects:
                    project_name = project['name']
                    project_id = project['id']
                    project_path = project['path_with_namespace']
                    
                    print(f"  🔍 Processing: {project_name}")
                    
                    # Get commits for this project/repository
                    commits_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
                    commits_response = requests.get(
                        commits_url, 
                        headers=headers, 
                        params={'per_page': 100}, 
                        verify=False
                    )
                    
                    if commits_response.status_code == 200:
                        commits = commits_response.json()
                        
                        for commit in commits:
                            writer.writerow({
                                'group_path': group_path,
                                'project_name': project_name,
                                'project_path': project_path,
                                'commit_id': commit['id'],
                                'short_id': commit['short_id'],
                                'title': commit['title'],
                                'author_name': commit['author_name'],
                                'author_email': commit['author_email'],
                                'created_at': commit['created_at'],
                                'web_url': commit['web_url']
                            })
                        
                        print(f"    ✅ {len(commits)} commits from {project_name}")
                        total_commits += len(commits)
                    else:
                        print(f"    ❌ Error getting commits from {project_name}: {commits_response.status_code}")
            
            print(f"\n🎯 TOTAL: {total_commits} commits exported to {filename}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Usage
export_nested_group_commits_to_csv('https://your-gitlab-url.com', 'your_token', 'your_root_group_id')
