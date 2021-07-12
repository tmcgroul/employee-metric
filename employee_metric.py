from dataclasses import dataclass
from typing import Sequence, TypedDict


@dataclass
class Issue:
    estimate_time: int
    spend_time: int


class EmployeeMetric(TypedDict):
    issues: list
    overtime_issues: list


def get_employee_metric(issues: Sequence[Issue]) -> EmployeeMetric:
    issues_ = []
    overtime_issues = []
    for issue in issues:
        if issue.estimate_time < issue.spend_time:
            overtime_issues.append(issue)
        else:
            issues_.append(issue)
    return {
        'issues': issues_,
        'overtime_issues': overtime_issues,
    }
