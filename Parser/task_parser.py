from Parser.node import TaskNode, OperatorNode
from Parser.task_description import Task
from Parser.token import TokenType, Token
from Parser.tokenizer import Tokenizer


class TaskParser:
    def __init__(self, filename):
        self.tokenizer = Tokenizer(filename)

    def get_task_list(self):
        task_list = []
        try:
            while True:
                task = self.get_task()
                if task is None:
                    break
                task_list.append(task)
            return task_list
        except Exception as e:
            print("Parsing failed, because of:\n " + str(e))

    def get_task(self):
        token = self.tokenizer.next_token()
        if token is None:
            return None
        else:
            return Task(self.get_name(token), self.get_duration(), self.get_dependencies())

    def get_name(self, token):
        if token.is_name():
            return token.value
        raise Exception(f"Expected TokenType.NAME\nGot {token.type}")

    def get_duration(self):
        token = self.tokenizer.next_token()
        if not token.is_takes():
            raise Exception(f"Expected TokenType.TAKES\nGot {token.type}")
        token = self.tokenizer.next_token()
        if not token.is_number():
            raise Exception(f"Expected TokenType.NUMBER\nGot {token.type}")
        return int(token.value)

    def get_dependencies(self):
        token = self.tokenizer.next_token()
        if not token.is_needs():
            raise Exception(f"Expected TokenType.NEEDS\nGot {token.type}")
        else:
            dependencies = self.get_dependencies_list()
            if len(dependencies) == 1:
                return TaskNode(dependencies[0].value)
            else:
                return self.evaluate_dependencies(dependencies)[0].value

    def get_dependencies_list(self):
        def is_end_of_file():
            return self.tokenizer.peek_token() is None

        def is_end_of_dependencies():
            return token.is_name() and self.tokenizer.peek_token().is_name() or token.is_close_bracket() and self.tokenizer.peek_token().is_name()

        def is_valid_token_for_dependencies():
            return token.is_open_bracket() or token.is_close_bracket() or token.is_name() or token.is_and() or token.is_or()

        dependency_list = []
        # get tokens until end of file or end of dependency
        while True:
            token = self.tokenizer.next_token()
            if is_end_of_file() or is_end_of_dependencies():
                dependency_list.append(token)
                break
            elif is_valid_token_for_dependencies():
                dependency_list.append(token)
            else:
                raise Exception(f"Invalid Token in dependency: {token}")
        return dependency_list

    def evaluate_dependencies(self, dependencies):
        if len(dependencies) == 1:
            return dependencies
        if len(dependencies) % 2 == 0:
            raise Exception("Invalid syntax, even number of tokens")
        count_open_brackets, count_close_brackets = self.get_count_for_two_tokentype(TokenType.OPEN_BRACKET,
                                                                                     TokenType.CLOSE_BRACKET,
                                                                                     dependencies)
        if count_open_brackets != count_close_brackets:
            raise Exception("Missmatch of open and close brackets,check the dependencies")
        # use different evaluation method if brackets are present or not
        if count_open_brackets == 0:
            return self.evaluate_dependencies_without_brackets(dependencies)
        else:
            return self.evaluate_dependencies_with_brackets(dependencies)

    def evaluate_dependencies_without_brackets(self, dependencies):
        count_and, count_or = self.get_count_for_two_tokentype(TokenType.AND, TokenType.OR, dependencies)
        # simplify dependencies until no AND or OR is left
        while len(dependencies) > 1:
            if count_and > 0:
                dependencies = self.simplify(dependencies, TokenType.AND)
                count_and -= 1
            elif count_or > 0:
                dependencies = self.simplify(dependencies, TokenType.OR)
                count_or -= 1
        return dependencies

    def evaluate_dependencies_with_brackets(self, dependencies):
        def get_index_open_and_close_bracket():
            # index first open bracket
            open_bracket = -1
            for i, dependency in enumerate(dependencies):
                if dependency.is_open_bracket():
                    open_bracket = i
                    break
            # find matching close bracket
            index_matching_close_bracket = -1
            close_bracket = 0
            for i, dependency in enumerate(dependencies[open_bracket:]):
                if dependency.is_open_bracket():
                    close_bracket += 1
                if dependency.is_close_bracket():
                    close_bracket -= 1
                if close_bracket == 0:
                    index_matching_close_bracket = i + open_bracket
                    break
            return open_bracket, index_matching_close_bracket

        index_open_bracket, index_close_bracket = get_index_open_and_close_bracket()
        # evaluate bracket
        evaluated = self.evaluate_dependencies(dependencies[index_open_bracket + 1:index_close_bracket])
        # replace bracket with evaluated expression
        del dependencies[index_open_bracket:index_close_bracket + 1]
        dependencies.insert(index_open_bracket, evaluated[0])
        # evaluate dependencies
        return self.evaluate_dependencies(dependencies)

    def simplify(self, token_list, operator_token):
        # Find the index of the first occurrence of the operator in the tokens list
        operator_index = -1
        for token_index, current_token in enumerate(token_list):
            if current_token.type == operator_token:
                operator_index = token_index
                break
        # Check if the index is odd (syntax is valid)
        if operator_index & 1 == 1:
            # Determine the operation to be performed (And or Or)
            operation = "And" if operator_token == TokenType.AND else "Or"
            # Get the left and right operands
            left_operand = token_list[operator_index - 1].value
            right_operand = token_list[operator_index + 1].value
            # If the operands are strings, create TaskNode objects for them
            if isinstance(left_operand, str):
                left_operand = TaskNode(left_operand)
            if isinstance(right_operand, str):
                right_operand = TaskNode(right_operand)
            # Modify the original tokens in-place
            token_list[operator_index - 1] = Token(TokenType.EXPRESSION,
                                                   OperatorNode(operation, left_operand, right_operand))
            # Remove the right operand token
            del token_list[operator_index + 1]
            # Remove the operator token
            del token_list[operator_index]
            return token_list
        else:
            raise Exception("In dependencies, the operator must be preceded and followed by a task name")

    def get_count_for_two_tokentype(self, first_type, second_type, dependencies):
        first_type_count, second_type_count = 0, 0
        for dependency in dependencies:
            if dependency.is_type(first_type):
                first_type_count += 1
            if dependency.is_type(second_type):
                second_type_count += 1
        return first_type_count, second_type_count
