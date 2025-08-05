import re

def handle_natural_query(user_input):
    user_input = user_input.lower()

    if "unassigned" in user_input:
        return 'assignee is EMPTY'

    elif "high priority" in user_input:
        return 'priority = High'

    elif "open" in user_input and "assigned to" in user_input:
        name_match = re.search(r'assigned to (\w+)', user_input)
        if name_match:
            name = name_match.group(1)
            return f'statusCategory != Done AND assignee = {name}'

    elif "assigned to" in user_input:
        name_match = re.search(r'assigned to (\w+)', user_input)
        if name_match:
            name = name_match.group(1)
            return f'assignee = {name}'

    elif "status" in user_input:
        status_match = re.search(r'status is (\w+)', user_input)
        if status_match:
            status = status_match.group(1)
            return f'status = {status}'

    elif "health check" in user_input:
        return 'summary ~ "health check"'

    elif "login" in user_input:
        return 'summary ~ "login" OR description ~ "login"'

    return None
