import pytest

from employee_metric import Issue, get_employee_metric


@pytest.mark.parametrize(
    ('spend_time', 'expected_overtime'),
    [(10, True), (5, False)]
)
def test_overtime_issues(spend_time, expected_overtime):
    issue = Issue(5, spend_time)
    metric = get_employee_metric([issue])
    assert (issue in metric['overtime_issues']) == expected_overtime
