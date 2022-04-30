import base64
import json
from typing import Optional
from wrapper.cloud_billing import CloudBilling, Project
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

    projects = cloud_billing.get_projects()

    if cost_amount > budget_amount:
        print(
            f"Current costs of {cost_amount} are larger than the budget of {budget_amount}"
        )
        execute_on_projects(lambda p: disable_billing(cloud_billing, p), projects)
        return

    print(f"No action necessary. Current cost are {cost_amount}.")
    for p in projects:
        print_billing_status(p)


def print_billing_status(project: Project):
    print(f"{project.project_id} has billing enable: {project.is_billing}")


def execute_on_projects(f, project_ids):
    exceptions = []
    for project_id in project_ids:
        try:
            f(project_id)
        except Exception as exc:
            exceptions.append(exc)
    if exceptions:
        raise AggregateException(exceptions)


def disable_billing(billing: CloudBilling, project: Project):
    if project.is_billing:
        billing.disable_billing(project)
    else:
        print(f"Billing already disabled for {project.project_id}")
