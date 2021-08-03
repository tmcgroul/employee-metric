from typing import Sequence, TypedDict, TypeVar, Protocol

T = TypeVar('T')


class Issue(Protocol):
    estimate_time: int  # sec
    spent_time: int  # sec


class EmployeeMetric(TypedDict):
    employee: T
    issues: list[Issue]
    overdue_issues: list[Issue]
    overdue_percentage: float


def get_employee_metric(
    employee: T,
    issues: Sequence[Issue]
) -> EmployeeMetric:
    issues_ = []
    overdue_issues = []
    for issue in issues:
        if issue.estimate_time < issue.spent_time:
            overdue_issues.append(issue)
        else:
            issues_.append(issue)

    return EmployeeMetric(
        employee=employee,
        issues=issues_,
        overdue_issues=overdue_issues,
        overdue_percentage=100 / len(issues) * len(overdue_issues)
    )


def leaderboard(
    employees_issues: dict[T, list[Issue]]
) -> list[EmployeeMetric]:
    employees_metric: list[EmployeeMetric] = []
    for employee, issues in employees_issues.items():
        employee_metric = get_employee_metric(employee, issues)
        employees_metric.append(employee_metric)
    employees_metric.sort(key=lambda metric: -metric['overdue_percentage'])
    return employees_metric
