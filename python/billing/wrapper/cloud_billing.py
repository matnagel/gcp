from dataclasses import dataclass
import json
from typing import List
import googleapiclient.discovery as gdiscovery


@dataclass
class Project:
    project_id: str
    is_billing: bool


class CloudBilling:
    def __init__(self, billing_id: str):
        self.billing_id = billing_id
        billing_api = gdiscovery.build("cloudbilling", "v1", cache_discovery=False)
        self.projects_api = billing_api.projects()
        self.billing_accounts_api = billing_api.billingAccounts()

    def get_projects(self) -> List[Project]:
        billing_projects_api = self.billing_accounts_api.projects()
        billing_id = f"billingAccounts/{self.billing_id}"

        projects: List[Project] = []

        nextToken = ""
        pages = 0
        is_unfinished = True

        while is_unfinished and pages < 10:
            request = billing_projects_api.list(
                name=billing_id, pageToken=nextToken
            ).execute()
            for res in request["projectBillingInfo"]:
                project = Project(res["projectId"], res["billingEnabled"])
                projects.append(project)
            nextToken = request["nextPageToken"]
            print(f"Token: {nextToken}")
            if not nextToken:
                is_unfinished = False
            pages += 1

        return projects

    def disable_billing(self, project: Project) -> None:
        project_name = f"projects/{project.project_id}"
        body = {"billingAccountName": ""}  # Body to disable billing
        try:
            res = self.projects_api.updateBillingInfo(
                name=project_name, body=body
            ).execute()
            print(f"Billing disabled: {json.dumps(res)}")
        except Exception as exception:
            raise RuntimeError(
                "Failed to disable billing, possibly check permissions"
            ) from exception
