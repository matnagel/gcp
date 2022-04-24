import json
import base64
from typing import Set, Dict
from pytest import raises
import pytest
from main import AggregateException, check_billing

import random


@pytest.fixture
def projects() -> Dict[str, bool]:
    return {"project-1": True, "project-2": True, "project-5": True}


class FakeEnvironment:
    def get_billing_id(self):
        return "1234-5678"


class MockCloudBilling:
    def __init__(self, project_ids: Set[str], billing_enabled: Dict[str, bool]):
        self.billing_enabled: Dict[str, bool] = billing_enabled
        self.has_been_disabled: Dict[str, bool] = dict()
        self.project_ids = project_ids

    def get_projects(self, billing_id: str) -> Set[str]:
        if billing_id == "1234-5678":
            return self.project_ids
        return set()

    def is_billing_enabled(self, project_id: str) -> bool:
        if project_id not in self.billing_enabled:
            raise RuntimeError(f"Unable to get billing information for {project_id}")
        return self.billing_enabled[project_id]

    def disable_billing(self, project_id: str) -> None:
        self.billing_enabled[project_id] = False
        self.has_been_disabled[project_id] = True


def generate_data(cost_amount: int, budget_amount: int):
    data = dict()
    content = {"costAmount": cost_amount, "budgetAmount": budget_amount}
    json_content = json.dumps(content)
    data["data"] = base64.b64encode(json_content.encode())
    return data


def test_enough_budget(projects):
    data = generate_data(cost_amount=5, budget_amount=10)
    billing = MockCloudBilling(project_ids=projects.keys(), billing_enabled=projects)
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    enabled = [billing.billing_enabled[p_id] for p_id in projects.keys()]
    assert all(enabled)


def test_over_budget(projects):
    data = generate_data(cost_amount=10, budget_amount=5)
    billing = MockCloudBilling(project_ids=projects.keys(), billing_enabled=projects)
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    enabled = [billing.billing_enabled[p_id] for p_id in projects.keys()]
    assert not any(enabled)


def test_over_budget_with_disabled_billing(projects):
    data = generate_data(cost_amount=10, budget_amount=5)
    projects_ids = list(projects.keys())
    p_id = random.choice(projects_ids)
    projects[p_id] = False
    billing = MockCloudBilling(project_ids=set(projects_ids), billing_enabled=projects)
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    assert p_id not in billing.has_been_disabled


def test_unable_to_get_billing_information(projects):
    project_ids = list(projects.keys())
    p_id = random.choice(project_ids)
    del projects[p_id]

    with raises(
        AggregateException,
        match=f"Could not determine whether billing is enabled for {p_id}",
    ):
        data = generate_data(cost_amount=10, budget_amount=5)
        billing = MockCloudBilling(
            project_ids=set(project_ids), billing_enabled=projects
        )
        check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    enabled = [billing.billing_enabled[p_id] for p_id in project_ids]
    assert not any(enabled)
