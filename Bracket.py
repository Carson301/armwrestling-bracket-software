#
#
#

from abc import ABC, abstractmethod
import math


class Bracket(ABC):

    @abstractmethod
    def __init__(self, competitors):
        ...

    @abstractmethod
    def create_bracket(self):
        ...

    @abstractmethod
    def fill_bracket(self):
        ...

    @abstractmethod
    def account_for_bys(self):
        ...

    @abstractmethod
    def match_winner(self):
        ...

    @abstractmethod
    def match_undo(self):
        ...

    @abstractmethod
    def check_done(self):
        ...

    #==================================================================#

    def get_bracket(self):
        return self.nodes

    def get_num_competitors(self):
        return self.num_competitors

    def get_num_nodes(self):
        return self.num_nodes

    @abstractmethod
    def get_num_levels(self):
        ...

    @abstractmethod
    def get_levels(self):
        ...


