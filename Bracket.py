#
#
#

from abc import ABC, abstractmethod
import math


class Bracket(ABC):


    def __init__(self, competitor_list):
        self.competitor_list = competitor_list
        self.num_competitors = len(competitor_list)

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
        return self.node_list

    def get_num_competitors(self):
        return self.num_competitors

    def get_num_nodes(self):
        return self.num_nodes

    @abstractmethod
    def get_num_levels(self):
        ...

    @abstractmethod
    def set_level_list(self):
        ...

    @abstractmethod
    def get_level_list(self):
        ...


