import os
import json
from github import Github, UnknownObjectException

from configurator import load_config


config = load_config("../config/config_from_env.json")
access_key = config['github']['pat']
org_name = config['github']['org']
backup_dir = "../backup_data/teams/"

g = Github(access_key)

# Restore teams
print("Restoring teams...")

# Read teams backup file
teams_file = os.path.join(backup_dir, "teams_backup.json")
with open(teams_file, "r") as file:
    teams_data = json.load(file)

# Iterate over each team data
for team_info in teams_data:
    team_name = team_info["name"]
    team_slug = team_info["slug"]
    team_id = team_info["id"]
    settings = team_info["settings"]
    team_settings = {}
    for key, value in settings.items():
        if value is not None:
            team_settings[key] = value

    print("team_data: ",team_name,team_slug, team_id, team_settings)

    try:
     # Check if the team already exists
        existing_team = g.get_organization(org_name).get_team_by_slug(team_slug)
        # existing_team = g.get_organization(org_name).get_team(team_id)
        print(existing_team)
        # Update team settings
        print(f"Updating team settigs: {team_name}")
        existing_team.edit(**team_settings)

        # Update team members
        print(f"Updating team members list: {team_name}")
        for member_login in team_info["members"]:
            member = g.get_user(member_login)
            print("member: ", member)
            # Add member to the team TODOOOO:COMPARE LISTS OF MEMBERS
            existing_team.add_membership(member)

    except UnknownObjectException:
        # Team doesn't exist, create it
        print(f"Creating team: {team_name}")
        new_team = g.get_organization(org_name).create_team(team_name)

        # Restre team settings
        print(f"Restoring team settigs: {team_name}")
        new_team.edit(**team_settings)

        # Restore team members
        print(f"Restring team members list: {team_name}")
        for member_login in team_info["members"]:
            member = g.get_user(member_login)
            print("member: ", member)
            new_team.add_membership(member)

print("Teams restoration completed!")