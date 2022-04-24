import base64
import json
from typing import Optional
from wrapper.cloud_billing import CloudBilling
from wrapper.environment_variables import EnvVariables


class DataFormatException(Exception):
    pass


class AggregateException(Exception):
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
    cloud_billing: Optional[CloudBilling] = None,
):

    print("Checking billing notification")
    info = read_billing_information(data)
    cost_amount = info["costAmount"]
    budget_amount = info["budgetAmount"]

    if not environment:
        environment = EnvVariables()

    billing_id = environment.get_billing_id()

    if not cloud_billing:
        cloud_billing = CloudBilling(billing_id)

    project_ids = cloud_billing.get_projects()

    if cost_amount > budget_amount:
        print(f"Current costs: {cost_amount} are larger than budget {budget_amount}")
        execute_on_projects(
            lambda p_id: disable_billing(cloud_billing, p_id), project_ids
        )
        return

    if "alertThresholdExceeded" in info:
        alert = info["alertThresholdExceeded"]
        print(f"Alert threshold {alert} with costs {cost_amount} exceeded")
        execute_on_projects(
            lambda p_id: disable_billing(cloud_billing, p_id), project_ids
        )
        return

    print(f"No action necessary. Current cost are {cost_amount}.")
    execute_on_projects(
        lambda p_id: print_billing_status(cloud_billing, p_id), project_ids
    )


def print_billing_status(billing: CloudBilling, project_id: str):
    billing_status = billing.is_billing_enabled(project_id)
    print(f"{project_id} has billing enable: {billing_status}")


def execute_on_projects(f, project_ids):
    exceptions = []
    for project_id in project_ids:
        try:
            f(project_id)
        except Exception as exc:
            exceptions.append(exc)
    if exceptions:
        raise AggregateException(exceptions)


def disable_billing(billing: CloudBilling, project_id: str):
    try:
        is_enabled = billing.is_billing_enabled(project_id)
    except Exception as exception:
        print(
            f"Unable to determine if billing is enabled on project {project_id}. Trying to disabling anyways."
        )
        billing.disable_billing(project_id)
        raise RuntimeError(
            f"Could not determine whether billing is enabled for {project_id}, while trying to disable billing"
        ) from exception

    if is_enabled:
        billing.disable_billing(project_id)
    else:
        print(f"Billing already disabled for {project_id}")
