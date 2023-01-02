from enum import Enum


class TokenType(Enum):
    NAME = 1
    TAKES = 2
    NEEDS = 3
    NUMBER = 4
    OPEN_BRACKET = 5
    CLOSE_BRACKET = 6
    AND = 7
    OR = 8
    EXPRESSION = 9


class Token:
    def __init__(self, token_type: TokenType, value=None):
        self.type = token_type
        self.value = value

    def is_type(self, token_type: TokenType):
        return self.type == token_type

    def is_name(self):
        return self.type == TokenType.NAME

    def is_takes(self):
        return self.type == TokenType.TAKES

    def is_needs(self):
        return self.type == TokenType.NEEDS

    def is_number(self):
        return self.type == TokenType.NUMBER

    def is_open_bracket(self):
        return self.type == TokenType.OPEN_BRACKET

    def is_close_bracket(self):
        return self.type == TokenType.CLOSE_BRACKET

    def is_and(self):
        return self.type == TokenType.AND

    def is_or(self):
        return self.type == TokenType.OR

    def is_expression(self):
        return self.type == TokenType.EXPRESSION

    def __str__(self):
        return f"Token: {self.type} {self.value}"
