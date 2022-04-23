import json
import base64
from pytest import raises
from unittest.mock import Mock, patch
from main import check_billing


class FakeEnvironment:
    def get_project_id(self):
        return "project-test"


class MockCloudBilling:
    def __init__(self, billing_enabled: bool, no_billing_info: bool = False):
        self.billing_enabled = billing_enabled
        self.has_been_disabled = False
        self.no_billing_info = no_billing_info

    def is_billing_enabled(self, project_id: str) -> bool:
        if self.no_billing_info:
            raise RuntimeError("Unable to get billing information")
        return (project_id == "project-test") and self.billing_enabled

    def disable_billing(self, project_id: str) -> None:
        if project_id == "project-test":
            self.billing_enabled = False
            self.has_been_disabled = True


def generate_data(cost_amount: int, budget_amount: int):
    data = dict()
    content = {"costAmount": cost_amount, "budgetAmount": budget_amount}
    json_content = json.dumps(content)
    data["data"] = base64.b64encode(json_content.encode())
    return data


suppress_prints = patch("builtins.print", Mock())


def test_enough_budget():
    with suppress_prints:
        data = generate_data(cost_amount=5, budget_amount=10)
        billing = MockCloudBilling(billing_enabled=True)
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        assert billing.is_billing_enabled("project-test")


def test_over_budget():
    with suppress_prints:
        data = generate_data(cost_amount=10, budget_amount=5)
        billing = MockCloudBilling(billing_enabled=True)
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        assert not billing.is_billing_enabled("project-test")


def test_over_budget_with_disabled_billing():
    with suppress_prints:
        data = generate_data(cost_amount=10, budget_amount=5)
        billing = MockCloudBilling(billing_enabled=False)
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
        assert not billing.has_been_disabled


def test_unable_to_get_billing_information():
    with suppress_prints, raises(
        RuntimeError, match="Could not determine whether billing is enabled"
    ):
        data = generate_data(cost_amount=10, budget_amount=5)
        billing = MockCloudBilling(billing_enabled=True, no_billing_info=True)
        check_billing(data, None, environment=FakeEnvironment(), billing=billing)
    assert billing.has_been_disabled
