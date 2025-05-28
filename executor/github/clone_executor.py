import os
import re
import subprocess

from github import Github


class CloneExecutor:
    def execute(self, **kwargs):
        (github_organization,
         github_token,
         target_directory) = self._load_check_args(kwargs)

        # Create github client instance
        github_client = Github(login_or_token=github_token)

        # Fetch all projects in the specified organization
        github_org = github_client.get_organization(org=github_organization)

        if github_org:
            projects = github_org.get_repos()
            os.makedirs(target_directory, exist_ok=True)
            for project in projects:
                print(f"Cloning project: {project.name} ({project.clone_url})")
                project_path = f"{target_directory}/{project.full_name}"
                # Clone the project repository
                os.makedirs(project_path, exist_ok=True)
                match = re.match(r'^(https?)://', project.clone_url)
                if match:
                    protocol = match.group(1)
                    new_url = re.sub(r'^https?://', f'{protocol}://oauth2:{github_token}@', project.clone_url)
                    subprocess.run(["git", "clone", new_url, project_path], check=True)

    def _load_check_args(self, kwargs):
        github_organization = kwargs['github_organization'] if 'github_organization' in kwargs else None
        github_token = kwargs['github_token'] if 'github_token' in kwargs else None
        target_directory = kwargs['target_directory'] if 'target_directory' in kwargs else None

        variables = {
            "github_organization": github_organization,
            "github_token": github_token,
            "target_directory": target_directory
        }

        if any(v is None for v in variables.values()):
            for key, value in variables.items():
                if value is None:
                    print(f"Missing required parameter: {key}")
            raise ValueError("Missing required parameters")

        return (github_organization,
                github_token,
                target_directory)
