import base64
import json
from typing import Optional
from wrapper.cloud_billing import CloudBilling
from wrapper.environment_variables import EnvVariables


class DataFormatException(Exception):
    pass


def read_billing_information(data):
    if "data" not in data:
        raise DataFormatException("Called without billing notification data.")
    pubsub_data = base64.b64decode(data["data"]).decode("utf-8")
    info = json.loads(pubsub_data)
    if not (("costAmount" in info) or ("budgetAmount" in info)):
        raise DataFormatException("Called without containing necessary billing fields")
    return info


def check_billing(
    data,
    _,
    environment: Optional[EnvVariables] = None,
    billing: Optional[CloudBilling] = None,
):

    print("Checking billing notification")
    info = read_billing_information(data)
    cost_amount = info["costAmount"]
    budget_amount = info["budgetAmount"]

    if not environment:
        environment = EnvVariables()

    billing_id = environment.get_billing_id()

    if not billing:
        billing = CloudBilling(billing_id)

    projects = billing.get_projects(billing_id)

    if cost_amount > budget_amount:
        print(f"Current costs: {cost_amount} are larger than budget {budget_amount}")
        for project_id in projects:
            disable_billing(project_id, billing)
        return

    if "alertThresholdExceeded" in info:
        alert = info["alertThresholdExceeded"]
        print(f"Alert threshold {alert} with costs {cost_amount} exceeded")
        for project_id in projects:
            disable_billing(project_id, billing)
        return

    print(f"No action necessary. Current cost are {cost_amount}.")
    for project_id in projects:
        billing_status = billing.is_billing_enabled(project_id)
        print(f"{project_id} has billing enable: {billing_status}")


def disable_billing(project_id: str, billing: CloudBilling):
    try:
        is_enabled = billing.is_billing_enabled(project_id)
    except Exception as exception:
        print(
            f"Unable to determine if billing is enabled on project {project_id}. Trying to disabling anyways."
        )
        billing.disable_billing(project_id)
        raise RuntimeError(
            "Could not determine whether billing is enabled, while trying to disable billing"
        ) from exception

    if is_enabled:
        billing.disable_billing(project_id)
    else:
        print(f"Billing already disabled for {project_id}")
