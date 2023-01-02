class WordParser:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.buffer = False

    def next_word(self):
        word = ""
        if self.buffer:
            self.buffer = False
            word = ")"
        else:
            while True:
                c = self.file.read(1)
                if len(c) == 0:
                    if word == "":
                        return None
                    else:
                        return word
                    break
                if c == '(':
                    word += c
                    break
                elif c == ')':
                    if word == "":
                        return ")"
                    else:
                        self.buffer = True
                        break
                if c == ' ' or c == '\n' or c == '\t':
                    if word == "":
                        continue
                    else:
                        break
                else:
                    word += c
        if word:
            return word
        else:
            return None