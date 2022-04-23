import googleapiclient as gac
import json


class CloudBilling:
    def __init__(self):
        self.billing_api = gac.discovery.build(
            "cloudbilling", "v1", cache_discovery=False
        )
        self.projects = self.billing_api.get_projects()

    def disable_billing(self, project_id: str) -> None:
        project_name = f"projects/{project_id}"
        body = {"billingAccountName": ""}  # Body to disable billing
        try:
            res = self.projects.updateBillingInfo(
                name=project_name, body=body
            ).execute()
            print(f"Billing disabled: {json.dumps(res)}")
        except Exception as exception:
            raise RuntimeError(
                "Failed to disable billing, possibly check permissions"
            ) from exception

    def is_billing_enabled(self, project_id: str) -> bool:
        project_name = f"projects/{project_id}"
        res = self.projects.getBillingInfo(name=project_name).execute()

        if "billingEnabled" in res:
            return bool(res["billingEnabled"])
        else:
            # If billingEnabled isn't part of the return, billing is not enabled
            return False
