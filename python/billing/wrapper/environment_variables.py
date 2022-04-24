import os


class EnvironmentException(Exception):
    pass


class EnvVariables:
    def get_env(self, name: str) -> str:
        env = os.getenv(name)
        if env is None:
            raise EnvironmentException(f"No environment variable {name}")
        return env

    def get_project_id(self) -> str:
        return self.get_env("PROJECT_ID")

    def get_billing_id(self) -> str:
        return self.get_env("BILLING_ID")
