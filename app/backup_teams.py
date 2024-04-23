import os
import json
from github import Github
from configurator import load_config


config = load_config("../config/config_from_env.json")
access_key = config['github']['pat']
org_name = config['github']['org']
backup_dir = "../backup_data/teams/"

g = Github(access_key)

# Backup teams
print("Backing up teams...")
os.makedirs(backup_dir, exist_ok=True)
# Initialize list to store team data
teams_data = []

# Retrieve teams and their members/settings
for team in g.get_organization(org_name).get_teams():
    team_name = team.name
    team_slug = team.slug
    team_id = team.id


    # Get team members
    members = [member.login for member in team.get_members()]

    # Get team settings
    settings = {
        "name": team.name,
        "description": team.description or "",
        "notification_setting": team.notification_setting,
        "parent": team.parent,
        "privacy": team.privacy,
        "permission": team.permission
    }

    # Append team data to list
    teams_data.append({
        "name": team_name,
        "slug": team_slug,
        "id": team_id,
        "members": members,
        "settings": settings
    })

# Save teams data to a JSON file
teams_file = os.path.join(backup_dir, "teams_backup.json")
with open(teams_file, "w") as file:
    json.dump(teams_data, file, indent=4)

print("Teams backup completed")
