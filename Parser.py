class Parser:
    def parse(self, input_string):
        pass


class ParseName(Parser):
    def parse(self, input_string):
        # Check if the input string is a valid letter
        if not ParseLetter().parse(input_string[0]):
            return None

        # Check if the rest of the input string is a valid identifier
        if not ParseIdentifier().parse(input_string[1:]):
            return None

        # If both the letter and identifier are valid, return the input string
        return input_string


class ParseDuration(Parser):
    def parse(self, input_string):
        # Check if the input string is a valid integer
        if not input_string.isdigit():
            return None
        # If the input string is a valid integer, return it as an int
        return int(input_string)


class ParseDependencies:
    def parse(self, tokens):
        # Check if the first token is "none"
        if tokens[0] == "none":
            return []

        dependencies = []

        # Parse the first dependency
        dependency = ParseName().parse(tokens[0])
        if dependency is None:
            return None
        dependencies.append((dependency, None))

        # Parse the rest of the dependencies, if any
        i = 1
        while i < len(tokens):
            # Check if the current token is a dependency operator
            operator = ParseDependencyOperator().parse(tokens[i])
            if operator is None:
                return None

            # Parse the next token as a dependency
            dependency = ParseName().parse(tokens[i + 1])
            if dependency is None:
                return None
            dependencies.append((dependency, operator))

            # Skip the next token (the dependency) and move to the next token after that
            i += 2

        # Return the list of dependencies
        return dependencies



class ParseDependencyOperator(Parser):
    def parse(self, input_string: str) -> str:
        # Check if the input string is "and" or "or"
        if input_string == "and" or input_string == "or":
            return input_string
        else:
            return None


class ParseLetter(Parser):
    def parse(self, input_string: str) -> bool:
        # Check if the input string is a single character
        if len(input_string) != 1:
            return False

        # Check if the character is a letter
        return input_string.isalpha()


class ParseIdentifier(Parser):
    def parse(self, input_string: str) -> bool:
        # Check if the input string is empty
        if not input_string:
            return True

        # Check if the first character is a valid letter
        if not ParseLetter().parse(input_string[0]):
            return False

        # Check if the rest of the input string is a valid identifier or digit
        return ParseIdentifier().parse(input_string[1:]) or ParseDigit().parse(input_string[1:])


class ParseDigit(Parser):
    def parse(self, input_string: str) -> bool:
        # Check if the input string is a single digit
        if len(input_string) != 1:
            return False

        # Check if the character is a digit
        return input_string.isdigit()


class ParseTask(Parser):
    def parse(self, input_string):
        # Split the input string into a list of tokens
        tokens = input_string.split()

        # Check if the first token is a valid name
        name = ParseName().parse(tokens[0])
        if name is None:
            raise SyntaxError("Invalid name")

        # Check if the second token is "takes"
        if tokens[1] != "takes":
            raise SyntaxError("Expected 'takes'")

        # Parse the duration
        duration = ParseDuration().parse(tokens[2])
        if duration is None:
            raise SyntaxError("Invalid duration")

        # Check if the fourth token is "needs"
        if tokens[3] != "needs":
            raise SyntaxError("Expected 'needs'")

        # Parse the dependencies
        #dependencies = ParseDependencies().parse(tokens[4:])
        dependencies = tokens[4:]
        dependencies = " ".join(dependencies)
        if dependencies is None:
            raise SyntaxError("Invalid dependencies")

        # Return a Task object with the parsed name, duration, and dependencies
        return name, duration, dependencies
