import json
import base64
from typing import List, Dict
import pytest
from main import check_billing
from wrapper.cloud_billing import Project

import random


@pytest.fixture
def projects() -> List[Project]:
    return [
        Project("project-1", True),
        Project("project-2", True),
        Project("project-5", True),
    ]


class FakeEnvironment:
    def get_billing_id(self):
        return "1234-5678"


class MockCloudBilling:
    def __init__(self, billing_id: str, projects: List[Project]):
        self.billing_id = billing_id
        self.has_been_disabled: Dict[str, bool] = dict()
        self.projects = projects

    def get_projects(
        self,
    ) -> List[Project]:
        if self.billing_id == "1234-5678":
            return self.projects
        return []

    def disable_billing(self, project: Project) -> None:
        project.is_billing = False
        self.has_been_disabled[project.project_id] = True


def generate_data(cost_amount: int, budget_amount: int):
    data = dict()
    content = {"costAmount": cost_amount, "budgetAmount": budget_amount}
    json_content = json.dumps(content)
    data["data"] = base64.b64encode(json_content.encode())
    return data


def test_enough_budget(projects: List[Project]):
    data = generate_data(cost_amount=5, budget_amount=10)
    env = FakeEnvironment()
    billing = MockCloudBilling(
        billing_id=env.get_billing_id(),
        projects=projects,
    )
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    enabled = [p.is_billing for p in projects]
    assert all(enabled)


def test_over_budget(projects: List[Project]):
    data = generate_data(cost_amount=10, budget_amount=5)
    env = FakeEnvironment()
    billing = MockCloudBilling(
        billing_id=env.get_billing_id(),
        projects=projects,
    )
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    enabled = [p.is_billing for p in projects]
    assert not any(enabled)


def test_over_budget_with_disabled_billing(projects: List[Project]):
    data = generate_data(cost_amount=10, budget_amount=5)
    p = random.choice(list(projects))
    p.is_billing = False
    env = FakeEnvironment()
    billing = MockCloudBilling(billing_id=env.get_billing_id(), projects=projects)
    check_billing(data, None, environment=FakeEnvironment(), cloud_billing=billing)
    assert p.project_id not in billing.has_been_disabled
