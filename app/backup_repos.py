import os
import json
import logging
import requests
from github import Github
from configurator import load_config

# Load configuration
config = load_config("../config/config_from_env.json")
access_key = config['github']['pat']
org_name = config['github']['org']
backup_dir = config.get('backup_dir', "../backup_data/repos/")  # Backup directory from config

# Initialize GitHub instance
g = Github(access_key)
org = g.get_organization(org_name)

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

def backup_repository(repo, repo_dir):
    """Backup repository settings, collaborators, webhooks, and download ZIP archive."""
    try:
        # Backup repository settings
        repo_settings = {
            "name": repo.name,
            "description": repo.description,
            "private": repo.private,
            "has_issues": repo.has_issues,
            "has_projects": repo.has_projects,
            "has_wiki": repo.has_wiki,
            "allow_rebase_merge": repo.allow_rebase_merge,
            "allow_squash_merge": repo.allow_squash_merge,
            "allow_merge_commit": repo.allow_merge_commit,
            "default_branch": repo.default_branch
        }

        # Backup collaborators
        collaborators = [collab.login for collab in repo.get_collaborators()]
        
        # Backup webhooks
        webhooks = [{"config": webhook.config, "events": webhook.events} for webhook in repo.get_hooks()]

        # Save repository data to JSON file
        repo_data = {
            "settings": repo_settings,
            "collaborators": collaborators,
            "webhooks": webhooks
        }
        with open(os.path.join(repo_dir, f"{repo.name}.json"), "w") as file:
            json.dump(repo_data, file, indent=4)
        logging.info(f"Repository '{repo.name}' backed up successfully.")

        # Download repository ZIP archive
        zip_url = repo.get_archive_link("zipball")
        zip_response = requests.get(zip_url)
        zip_file_path = os.path.join(repo_dir, f"{repo.name}.zip")
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(zip_response.content)
        logging.info(f"Repository '{repo.name}' ZIP archive downloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to backup repository '{repo.name}': {str(e)}")

# Backup repositories
logging.info("Backing up repositories...")
os.makedirs(backup_dir, exist_ok=True)

for repo in org.get_repos():
    # Create directory for repository
    repo_dir = os.path.join(backup_dir, repo.name)
    os.makedirs(repo_dir, exist_ok=True)

    # Backup repository and download ZIP archive
    backup_repository(repo, repo_dir)

print("Repositories backup completed")
