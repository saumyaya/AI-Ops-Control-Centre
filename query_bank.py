# A dictionary mapping common natural language queries to their Jira JQL equivalents.
QUERY_MAP = {
    # Status-based queries
    "show me open tickets": 'statusCategory != Done',
    "show open tickets": 'statusCategory != Done',
    "open tickets": 'statusCategory != Done',

    "show me closed tickets": 'statusCategory = Done',
    "show closed tickets": 'statusCategory = Done',
    "closed tickets": 'statusCategory = Done',

    "show all tickets": '',
    "all tickets": '',

    # Assignment queries
    "show me unassigned tickets": 'assignee IS EMPTY',
    "unassigned tickets": 'assignee IS EMPTY',
    "tickets assigned to me": 'assignee = currentUser()',
    "my tickets": 'assignee = currentUser()',

    # Priority queries
    "high priority tickets": 'priority = High',
    "medium priority tickets": 'priority = Medium',
    "low priority tickets": 'priority = Low',
    "critical tickets": 'priority = Critical',

    # Date-based queries
    "tickets created today": 'created >= startOfDay()',
    "tickets updated today": 'updated >= startOfDay()',
    "tickets created this week": 'created >= startOfWeek()',
    "tickets updated this week": 'updated >= startOfWeek()',
    "tickets created in last 7 days": 'created >= -7d',
    "tickets updated in last 7 days": 'updated >= -7d',

    # Reporter queries
    "tickets reported by me": 'reporter = currentUser()',

    # Sprint queries
    "tickets in current sprint": 'Sprint in openSprints()',
}
