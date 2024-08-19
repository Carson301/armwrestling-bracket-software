#
#
#
import DoubleBracket
import SingleBracket


class Tournament:

    brackets = []

    def __init__(self):
        self.brackets = []

    def add_bracket(self, bracket):
        self.brackets.append(bracket)

    def get_tournament(self):
        return self.brackets

