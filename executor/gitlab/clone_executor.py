import os
import re
import subprocess

from gitlab import Gitlab


class CloneExecutor:
    def execute(self, **kwargs):
        (gitlab_host,
         gitlab_group_id,
         gitlab_token,
         target_directory) = self._load_check_args(kwargs)

        # Create gitlab client instance
        gitlab_client = Gitlab(url=gitlab_host,
                               private_token=gitlab_token)

        # Fetch all projects in the specified group
        gitlab_group = gitlab_client.groups.get(gitlab_group_id)

        if gitlab_group:
            projects = gitlab_group.projects.list(include_subgroups=True,
                                                  all=True)
            for project in projects:
                print(
                    f"Cloning project: {project.name} ({project.http_url_to_repo}) into {project.path_with_namespace}")
                project_path = f"{target_directory}/{project.path_with_namespace}"
                # Clone the project repository
                os.makedirs(project_path, exist_ok=True)
                match = re.match(r'^(https?)://', project.http_url_to_repo)
                if match:
                    protocol = match.group(1)
                    new_url = re.sub(r'^https?://', f'{protocol}://oauth2:{gitlab_token}@', project.http_url_to_repo)
                    subprocess.run(["git", "clone", new_url, project_path], check=True)

    def _load_check_args(self, kwargs):
        gitlab_host = kwargs['gitlab_host'] if 'gitlab_host' in kwargs else None
        gitlab_group_id = kwargs['gitlab_group_id'] if 'gitlab_group_id' in kwargs else None
        gitlab_token = kwargs['gitlab_token'] if 'gitlab_token' in kwargs else None
        target_directory = kwargs['target_directory'] if 'target_directory' in kwargs else None

        variables = {
            "gitlab_host": gitlab_host,
            "gitlab_group_id": gitlab_group_id,
            "gitlab_token": gitlab_token,
            "target_directory": target_directory
        }

        if any(v is None for v in variables.values()):
            for key, value in variables.items():
                if value is None:
                    print(f"Missing required parameter: {key}")
            raise ValueError("Missing required parameters")

        return (gitlab_host,
                gitlab_group_id,
                gitlab_token,
                target_directory)
