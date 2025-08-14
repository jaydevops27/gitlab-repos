import gitlab
import requests

# Initialize GitLab connection
gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_token')

# Get project
project = gl.projects.get('project_id')

# Get all repositories (if it's a group)
group = gl.groups.get('group_id')
projects = group.projects.list(all=True)

# Get commits from each project
for proj in projects:
    print(f"=== Repository: {proj.name} ===")
    project_obj = gl.projects.get(proj.id)
    commits = project_obj.commits.list(per_page=50)
    
    for commit in commits:
        print(f"{commit.short_id} - {commit.title} - {commit.author_name}")
