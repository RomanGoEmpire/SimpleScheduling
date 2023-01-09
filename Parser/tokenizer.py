from Parser.token import Token, TokenType
from Parser.word_parser import WordParser


class Tokenizer:
    def __init__(self, filename):
        self.word_parser = WordParser(filename)
        self.buffer = None

    def next_token(self):
        # return the buffer if it is set, otherwise return the next token
        if self.buffer:
            token = self.buffer
            self.buffer = None
            return token
        return self.get_token()

    def peek_token(self):
        # fill the buffer if it is empty and return the buffer
        if not self.buffer:
            self.buffer = self.get_token()
        return self.buffer

    def get_token(self):
        # get the next word from the word parser
        word = self.word_parser.next_word()
        # return a token based on the word
        if word is None:
            return None
        if word == "and":
            return Token(TokenType.AND)
        if word == "or":
            return Token(TokenType.OR)
        if word == "needs":
            return Token(TokenType.NEEDS)
        if word == "takes":
            return Token(TokenType.TAKES)
        if word == "(":
            return Token(TokenType.OPEN_BRACKET)
        if word == ")":
            return Token(TokenType.CLOSE_BRACKET)
        if word[0].isdigit():
            if word[0] == "0" or not word.isdigit():
                raise Exception(f"Illegal Number: {word}")
            return Token(TokenType.NUMBER, word)
        if word[0].isalpha():
            for c in word:
                if not c.isdigit() and not c.isalpha():
                    raise Exception(f"Illegal Name: {word}")
            return Token(TokenType.NAME, word)
        raise Exception(f"Illegal Token: {word}")
