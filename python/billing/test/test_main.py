import json
import base64
from typing import Set, Dict
from pytest import raises
import pytest
from unittest.mock import Mock, patch
from main import check_billing


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
            raise RuntimeError("Unable to get billing information")
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


suppress_prints = patch("builtins.print", Mock())


def test_enough_budget(projects):
    with suppress_prints:
        data = generate_data(cost_amount=5, budget_amount=10)
        billing = MockCloudBilling(
            project_ids=projects.keys(), billing_enabled=projects
        )
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        enabled = [billing.billing_enabled[p_id] for p_id in projects.keys()]
        assert all(enabled)


def test_over_budget(projects):
    with suppress_prints:
        data = generate_data(cost_amount=10, budget_amount=5)
        billing = MockCloudBilling(
            project_ids=projects.keys(), billing_enabled=projects
        )
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        enabled = [billing.billing_enabled[p_id] for p_id in projects.keys()]
        assert not any(enabled)


def test_over_budget_with_disabled_billing(projects):
    with suppress_prints:
        data = generate_data(cost_amount=10, budget_amount=5)
        p_id = "project-5"
        projects[p_id] = False
        billing = MockCloudBilling(
            project_ids=projects.keys(), billing_enabled=projects
        )
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        assert p_id not in billing.has_been_disabled


def test_unable_to_get_billing_information(projects):
    with suppress_prints, raises(
        RuntimeError, match="Could not determine whether billing is enabled"
    ):
        data = generate_data(cost_amount=10, budget_amount=5)
        project_ids = set(projects.keys())
        p_id = "project-5"
        del projects["project-5"]
        billing = MockCloudBilling(project_ids=project_ids, billing_enabled=projects)
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
    assert billing.has_been_disabled[p_id]
