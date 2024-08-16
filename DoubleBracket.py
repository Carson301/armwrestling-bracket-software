# Carson J. King
# Double Bracket Class
# 2024

from Bracket import Bracket

import math
import Node


class DoubleBracket(Bracket):

    competitor_list = []
    node_list = []
    num_competitors = 0
    num_nodes = 0
    num_source_nodes = 0
    winners_bracket_indexes = []
    losers_bracket_indexes = []


    def __init__(self, competitor_list):
        self.competitor_list = competitor_list
        self.num_competitors = len(competitor_list)
        self.num_source_nodes = (self.num_competitors * 4)

    def set_loser_starts(self):
        for node in self.node_list:
            if node.get_value() == "":
                self.losers_bracket_indexes.append(self.node_list.index(node))
        self.losers_bracket_indexes.append(self.num_nodes - 2)

    def set_winner_indexes(self):
        levels = self.get_levels()
        for level in levels:
            for i in range(math.ceil(len(level) / 4)):
                self.winners_bracket_indexes.append(self.node_list.index(level[i]))

    def get_winner_indexes(self):
        return self.winners_bracket_indexes


    def create_bracket(self):
        # Calculates the number of nodes for a complete bracket given a number of competitors
        self.num_nodes = (2 ** (math.ceil(math.log(self.num_source_nodes, 2)) + 1) - 1)
        # Add that many empty nodes to a list
        for i in range(self.num_nodes):
            self.node_list.append(Node.Node(i))
        # Calculate the index of the first node on the next level of the bracket
        current_node = math.ceil(self.num_nodes / 2)
        # Has nodes point to one another to create a bracket structure
        for i in range(self.num_nodes - 1):
            self.node_list[i].set_next(self.node_list[math.floor(current_node)])
            current_node += 0.5  # NOTE: 2 nodes point to a node or a parent
        # Set every node's value to None
        for i in range(len(self.node_list)):
            self.node_list[i].set_value(None)
        self.set_winner_indexes()

    def fill_bracket(self):
        # Value to offset the placement of competitors in the bracket
        offset_value = 0
        # Number of source nodes in bracket/starting nodes/potential competitors
        num_comp_nodes = int(math.ceil(self.num_nodes / 8))
        # Value representing a midpoint to begin adding to within the bracket
        midpoint = int(num_comp_nodes / 2) + 1
        for i in range(self.num_competitors):
            if i < num_comp_nodes / 2:
                self.node_list[i * 2].set_value(self.competitor_list[i])  # Fills in one competitor for each pairing
            else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                if i % 2 == 0:
                    self.node_list[midpoint + math.ceil(offset_value) * 2].set_value(self.competitor_list[i])
                else:
                    self.node_list[midpoint - math.ceil(offset_value) * 2].set_value(self.competitor_list[i])
                offset_value = offset_value + 0.5
        offset_value = 0

        for i in range(self.num_competitors - 1):
            if i < num_comp_nodes / 2:
                self.node_list[num_comp_nodes + (i * 2)].set_value("Loser")  # Fills in one competitor for each pairing
            else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                if i % 2 == 0:
                    self.node_list[midpoint + num_comp_nodes + math.ceil(offset_value) * 2].set_value("Loser")
                else:
                    self.node_list[midpoint + num_comp_nodes - math.ceil(offset_value) * 2].set_value("Loser")
                offset_value = offset_value + 0.5
        self.node_list[self.num_nodes - 2].set_value("Loser")



    def account_for_bys(self):
        pass
        for i in range(0, self.num_nodes - 2, 2):  # Go through all nodes and check for instances of bys. Update bracket accordingly.
            current_node = self.node_list[i]
            partner_node = self.node_list[self.find_pair(i)]
            if self.node_list.index(current_node.get_next()) != self.num_nodes - 2:
                if current_node.get_value() == None and partner_node.get_value() == None:
                    current_node.set_value(-1)
                    partner_node.set_value(-1)
                    current_node.get_next().set_value(-1)
                elif current_node.get_value() != None and partner_node.get_value() == None:
                    partner_node.set_value(-1)
                    current_node.get_next().set_value(current_node.get_value())
                elif current_node.get_value() == None and partner_node.get_value() != None:
                    current_node.set_value(-1)
                    partner_node.get_next().set_value(partner_node.get_value())
                else:
                    current_node.get_next().set_value(-1)
        self.node_list[self.num_nodes - 1].set_value(None)
        for i in range(self.num_nodes - 2):  # Set empty nodes not due to bys back to None
            current_node = self.node_list[i]
            if current_node.get_value() != -1:
                current_node.get_next().set_value(None)
        for i in range(self.num_nodes - 2):  # Automatically advance node in bracket if paired with a by node
            current_node = self.node_list[i]
            partner_node = self.node_list[self.find_pair(i)]
            if current_node.get_value() != -1 and partner_node.get_value() == -1:
                partner_node.get_next().set_value(current_node.get_value())
                current_node.set_value(-1)
        for i in range(self.num_nodes):
            if self.node_list[i].get_value() == "Loser":
                self.node_list[i].set_value("")
        self.set_loser_starts()


    def find_pair(self, node_index):
        node_pair = 0
        if node_index % 2 == 0:  # Determine if node has a partner node has a competitor node ready
            node_pair = node_index + 1
        else:
            node_pair = node_index - 1
        return node_pair

    def reverse_bracket(self):
        self.node_list[self.num_nodes - 1].set_next([])
        for i in range(self.num_nodes - 2, -1, -1):
            node_list = []
            for j in range(len(self.node_list[i].get_next().get_next())):
                node_list.append(self.node_list[i].get_next().get_next()[j])
            node_list.append(self.node_list[i])
            self.node_list[i].get_next().set_next(node_list)
            self.node_list[i].set_next([])
        for i in range(int((self.num_nodes + 1) / 2)):
            self.node_list[i].set_next(None)


    def reverse_back(self):
        for i in range(int((self.num_nodes + 1) / 2), self.num_nodes, 1):
            for node in self.node_list[i].get_next():
                node.set_next(self.node_list[i])
        self.node_list[self.num_nodes - 1].set_next(None)

    def length_checker(self, node_list):
        count = 0
        for node in node_list:
            if node.get_value() != -1:
                count += 1
        return count

    def find_next(self, node_index):
        return self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]


    def match_winner(self, node_index):
        no_pair = False
        if self.node_list[self.find_pair(node_index)].get_value() == None or self.node_list[self.find_pair(node_index)].get_value() == "":
            no_pair = True
        if self.node_list[node_index].get_value() == "X" or self.node_list[self.find_pair(node_index)].get_value() == "X":
            no_pair = True
        if no_pair == False:  # As long as there is competitor node ready
            node_pair = self.find_pair(node_index)
            next_node = self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]
            while next_node != None and next_node.get_value() != None:
                if self.node_list.index(next_node) in self.losers_bracket_indexes:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes + 1:
                    next_node = self.node_list[math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]
            next_node = self.node_list[node_index].get_next()
            while next_node != None and next_node.get_value() != None:
                if self.node_list.index(next_node) in self.losers_bracket_indexes:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes + 1:
                    next_node = self.node_list[math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]

            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.node_list[i].get_value() == None or self.node_list[i].get_value() == "":
                    self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.node_list[i])
                    self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.node_list[i])
            for val in self.losers_bracket_indexes:
                tester = False
                for val2 in self.winners_bracket_indexes:
                    if self.node_list[val2].get_next() == self.node_list[val]:
                        tester = True
                if tester == False:
                    self.node_list[val].set_value("")
            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == None or self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == "" or self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == None or self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == "":
                    if i in self.losers_bracket_indexes:
                        self.node_list[i].set_value("")
                    else:
                        self.node_list[i].set_value(None)
                    self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.node_list[i])
                    self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.node_list[i])

            self.node_list[node_index].set_next(self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)])
            self.node_list[node_index].get_next().set_value(self.node_list[node_index].get_value())
            if node_pair in self.winners_bracket_indexes and node_pair != self.num_nodes - 3:
                if node_index % 2 == 0:
                    loser_index = 0
                    count = 0
                    while loser_index == 0:
                        if self.node_list[count].get_value() == "":
                            loser_index = count
                        else:
                            count += 1
                else:
                    loser_index = 0
                    count = 0
                    while loser_index == 0:
                        if self.node_list[count].get_value() == "":
                            loser_index = count
                        else:
                            count += 1
                self.node_list[node_pair].set_next(self.node_list[loser_index])
                self.node_list[loser_index].set_value(self.node_list[node_pair].get_value())
            if node_index == self.num_nodes - 7 and node_index in self.winners_bracket_indexes and self.find_pair(node_index) not in self.winners_bracket_indexes:
                self.node_list[node_index].get_next().get_next().set_value(self.node_list[node_index].get_value())
                self.node_list[self.num_nodes - 2].set_value("X")




    def match_undo(self, node_index):
        no_pair = False
        if self.node_list[node_index].get_value() == "X" or self.node_list[self.find_pair(node_index)].get_value() == "X":
            no_pair = True
        if no_pair == False:
            self.node_list[node_index].set_next(self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)])
            next_node = self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]
            while next_node != None and next_node.get_value() != None:
                if self.node_list.index(next_node) in self.losers_bracket_indexes:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes + 1:
                    next_node = self.node_list[math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]
            next_node = self.node_list[self.find_pair(node_index)].get_next()
            while next_node != None and next_node.get_value() != None:
                if self.node_list.index(next_node) in self.losers_bracket_indexes:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes + 1:
                    next_node = self.node_list[math.floor(self.node_list.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]

            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.node_list[i].get_value() == None or self.node_list[i].get_value() == "":
                    self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.node_list[i])
                    self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.node_list[i])
            for val in self.losers_bracket_indexes:
                tester = False
                for val2 in self.winners_bracket_indexes:
                    if self.node_list[val2].get_next() == self.node_list[val]:
                        tester = True
                if tester == False:
                    self.node_list[val].set_value("")
            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == None or self.node_list[
                    (i - int((self.num_nodes + 1) / 2)) * 2].get_value() == "" or self.node_list[
                    ((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == None or self.node_list[
                    ((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == "":
                    if i in self.losers_bracket_indexes:
                        self.node_list[i].set_value("")
                    else:
                        self.node_list[i].set_value(None)
                    self.node_list[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.node_list[i])
                    self.node_list[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.node_list[i])


    def check_done(self):
        if self.node_list[len(self.node_list) - 1].get_value() != None:
            return True
        else:
            return False

    def get_num_levels(self):
        return (math.ceil(math.log(self.num_competitors * 2, 2)) * 2) + 1  # Returns the number of levels the bracket has

    def get_num_nodes(self):
        return self.num_nodes

    def get_levels(self):
        levels = []
        level = []
        current_node = 0
        node_range = math.floor(self.num_nodes / 2)
        level_count = math.ceil(self.num_nodes / 2)
        for node in self.node_list:  # Separate the nodes into a series of levels as is the structure of the bracket
            if current_node <= node_range:
                level.append(node)
            else:
                levels.append(level)
                level = []
                level_count = level_count / 2
                node_range = node_range + level_count
                level.append(node)
            current_node += 1
        levels.append(level)
        return levels

    def __str__(self):
        nodes_string = ""
        current_node = 0
        node_range = math.ceil(self.num_nodes / 2) - 1
        level_count = math.ceil(self.num_nodes / 2) - 1
        for node in self.node_list:  # Create a string representation of the graph for review purposes
            if current_node <= node_range:
                nodes_string += str(node.get_value()) + " "
            else:
                nodes_string += "\n"
                level_count = level_count / 2
                node_range = current_node + level_count
                nodes_string += str(node.get_value()) + " "
            current_node += 1
        return nodes_string