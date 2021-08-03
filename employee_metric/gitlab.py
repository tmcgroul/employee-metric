import os
from datetime import datetime, timedelta

from employee_metric import Issue, leaderboard

import gitlab
from gitlab.v4 import objects


class GitlabIssue(Issue):

    def __init__(self, source: objects.Issue) -> None:
        self._source = source
        self.estimate_time = source.time_stats['time_estimate']
        self.spent_time = source.time_stats['total_time_spent']

    def __str__(self):
        return '{title} {estimate}/{spent} {link}'.format(
            title=self._source.title,
            estimate=self._source.time_stats['human_time_estimate'],
            spent=self._source.time_stats['human_total_time_spent'],
            link=self._source.web_url,
        )


def display_previous_month_leaderboard():
    end_of_first_day = datetime.now().replace(day=1, hour=23, minute=59,
                                              second=59, microsecond=999999)
    updated_before = end_of_first_day - timedelta(days=1)
    updated_after = updated_before.replace(day=1, hour=0, minute=0, second=0,
                                           microsecond=0)
    gl = gitlab.Gitlab(os.environ['GITLAB_URL'], os.environ['GITLAB_TOKEN'])
    users = gl.users.list(all=True, blocked=False)
    users_issues = {}
    for user in users:
        issues = gl.issues.list(all=True, assignee_id=user.id, state='closed',
                                scope='all', updated_after=updated_after,
                                updated_before=updated_before)
        if len(issues):
            users_issues[user] = [GitlabIssue(issue) for issue in issues]
    metrics = leaderboard(users_issues)
    for metric in metrics:
        print(metric['employee'].name, metric['overdue_percentage'])
        if metric['issues']:
            print('Issues:')
            for issue in metric['issues']:
                print(issue)
        if metric['overdue_issues']:
            print('Overdue issues:')
            for issue in metric['overdue_issues']:
                print(issue)
        print('######################')
