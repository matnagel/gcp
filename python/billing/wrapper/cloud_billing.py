import json
from typing import Set
import googleapiclient.discovery as gdiscovery


class CloudBilling:
    def __init__(self, billing_id: str):
        self.billing_id = billing_id
        billing_api = gdiscovery.build("cloudbilling", "v1", cache_discovery=False)
        self.projects_api = billing_api.projects()
        self.billing_accounts_api = billing_api.billingAccounts()

    def get_projects(self) -> Set[str]:
        billing_projects_api = self.billing_accounts_api.projects()
        billing_id = f"billingAccounts/{self.billing_id}"

        projects: Set[str] = set()

        request = billing_projects_api.list(name=billing_id, pageToken="").execute()
        nextToken = request["nextPageToken"]

        print(f"Request: {request}")
        print(f"nextToken: {nextToken}")

        return projects

    def disable_billing(self, project_id: str) -> None:
        project_name = f"projects/{project_id}"
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

    def is_billing_enabled(self, project_id: str) -> bool:
        project_name = f"projects/{project_id}"
        res = self.projects_api.getBillingInfo(name=project_name).execute()

        if "billingEnabled" in res:
            return bool(res["billingEnabled"])
        else:
            # If billingEnabled isn't part of the return, billing is not enabled
            return False
