class TaskExpression:
    def __init__(self, task_name):
        self.task_name = task_name

    def __str__(self):
        return self.task_name


class AndExpression(TaskExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({str(self.left)} and {str(self.right)})"


class OrExpression(TaskExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({str(self.left)} or {str(self.right)})"


def parse_dependency(dependency_string: str) -> TaskExpression:
    """Parses a dependency string and returns a task expression instance."""
    # Remove leading and trailing whitespace
    dependency_string = dependency_string.strip()

    # Find the first "and" or "or" keyword in the string, ignoring keywords inside parentheses
    or_index = -1
    and_index = -1
    paren_count = 0
    for i, c in enumerate(dependency_string):
        if c == "(":
            paren_count += 1
        elif c == ")":
            paren_count -= 1
        elif c == "o" and dependency_string[i:i + 2] == "or" and paren_count == 0:
            or_index = i
            break
        elif c == "a" and dependency_string[i:i + 3] == "and" and paren_count == 0:
            and_index = i
            break

    # If no keyword was found, return a TaskExpression instance
    if or_index == -1 and and_index == -1:
        return TaskExpression(dependency_string)

    # Split the string at the first keyword and recursively parse the left and right operands
    left_operand = dependency_string[:max(or_index, and_index)].strip()
    right_operand = dependency_string[max(or_index, and_index) + 3:].strip()
    left_expression = parse_dependency(left_operand)
    right_expression = parse_dependency(right_operand)

    # Create an AndExpression or OrExpression instance depending on the keyword
    if or_index != -1:
        return OrExpression(left_expression, right_expression)
    else:
        return AndExpression(left_expression, right_expression)


# dependency_string = "Task1 or Task2 and (Task3 or Task4 and Task5)"
dependency_string_list = [
    "Task1 and Task2",
    "Task1 or Task2 or Task3",
    "Task1 and Task2 or Task3",
    "(Task1 and Task2) or Task3",
    "Task1 or (Task2 and Task3)",
    "Task1 and (Task2 or Task3)",
    "(Task1 and Task2) and (Task3 or Task4)",
    "Task1 and Task2 or Task3 and Task4",
    "(Task1 or Task2) and (Task3 or Task4)",
    "Task1 and (Task2 or (Task3 and Task4))"
]
for string in dependency_string_list:
    expression = parse_dependency(string)
    print(string, "->", expression)
