import os
from typing import Optional


class EnvironmentException(Exception):
    pass


class EnvVariables:
    def get_env(self, name: str) -> Optional[str]:
        return os.getenv(name)

    def get_project_id(self) -> str:
        project_id = self.get_env("PROJECT_ID")

        if project_id is None:
            raise EnvironmentException(
                "No project specified in environment variable GCP_PROJECT"
            )
        return project_id
