import os
import json
from github import Github
from configurator import load_config


config = load_config("../config/config_from_env.json")
access_key = config['github']['pat']
org_name = config['github']['org']
backup_dir = "../backup_data/repos/"

g = Github(access_key)

def restore_repository(repo_data, org):
    # Extract repository settings
    repo_settings = repo_data["settings"]
    repo_name = repo_settings["name"]

    try:
        repo = org.get_repo(repo_name)
        print(f"Repository '{repo_name}' already exists, skipping...")
        return
    except:
        pass

    # Create the repository
    new_repo = org.create_repo(
        name=repo_name,
        description=repo_settings["description"],
        private=repo_settings["private"],
        has_issues=repo_settings["has_issues"],
        has_projects=repo_settings["has_projects"],
        has_wiki=repo_settings["has_wiki"],
        allow_rebase_merge=repo_settings["allow_rebase_merge"],
        allow_squash_merge=repo_settings["allow_squash_merge"],
        allow_merge_commit=repo_settings["allow_merge_commit"],
        auto_init=False
    )

    # Restore collaborators
    for collaborator in repo_data["collaborators"]:
        new_repo.add_to_collaborators(collaborator)

    # Restore webhooks
    for webhook in repo_data["webhooks"]:
        new_repo.create_hook(name="web", config=webhook["config"], events=webhook["events"])

    print(f"Repository '{repo_settings['name']}' restored successfully.")

# Restore repositories
print("Restoring repositories...")

# Get the organization
org = g.get_organization(org_name)

# Iterate over each saved repos
for root, dirs, files in os.walk(backup_dir):
    for file_name in files:
        if file_name.endswith(".json"):
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as file:
                repo_data = json.load(file)
                restore_repository(repo_data, org)

print("Repositories restoration completed")