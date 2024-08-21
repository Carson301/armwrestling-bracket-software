#
#
#

from abc import ABC, abstractmethod
import math


class Bracket(ABC):


    def __init__(self, competitor_list, bracket_name):
        self.competitor_list = competitor_list
        self.num_competitors = len(competitor_list)
        self.bracket_name = bracket_name

    def add_competitor(self, competitor):
        self.competitor_list.append(competitor)
        self.num_competitors = len(self.competitor_list)

    @abstractmethod
    def create_bracket(self):
        ...

    @abstractmethod
    def get_bracket_name(self):
        ...

    @abstractmethod
    def fill_bracket(self):
        ...

    @abstractmethod
    def account_for_bys(self):
        ...

    @abstractmethod
    def match_winner(self, node_index):
        ...

    @abstractmethod
    def match_undo(self, node_index):
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


