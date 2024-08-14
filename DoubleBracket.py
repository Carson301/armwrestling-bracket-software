#
#
#

from Bracket import Bracket

import math
import Node
import random


class DoubleBracket(Bracket):

    competitors = []
    nodes = []
    num_competitors = 0
    num_nodes = 0
    num_source_nodes = 0
    winners_bracket_indexes = []
    losers = []


    def __init__(self, competitors):
        self.competitors = competitors
        self.num_competitors = len(competitors)
        self.num_source_nodes = (self.num_competitors * 4)
        print(self.num_source_nodes, "here")

    def set_loser_starts(self):
        for node in self.nodes:
            if node.get_value() == "":
                self.losers.append(self.nodes.index(node))

    def set_winner_indexes(self):
        levels = self.get_levels()
        for level in levels:
            for i in range(math.ceil(len(level) / 2)):
                self.winners_bracket_indexes.append(self.nodes.index(level[i]))

    def get_winner_indexes(self):
        return self.winners_bracket_indexes


    def create_bracket(self):
        # Calculates the number of nodes for a complete bracket given a number of competitors
        self.num_nodes = (2 ** (math.ceil(math.log(self.num_source_nodes, 2)) + 1) - 1)
        # Add that many empty nodes to a list
        for i in range(self.num_nodes):
            self.nodes.append(Node.Node(i))
        # Calculate the index of the first node on the next level of the bracket
        current_node = math.ceil(self.num_nodes / 2)
        # Has nodes point to one another to create a bracket structure
        for i in range(self.num_nodes - 1):
            self.nodes[i].set_next(self.nodes[math.floor(current_node)])
            current_node += 0.5  # NOTE: 2 nodes point to a node or a parent
        # Set every node's value to None
        for i in range(len(self.nodes)):
            self.nodes[i].set_value(None)
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
                self.nodes[i * 2].set_value(self.competitors[i])  # Fills in one competitor for each pairing
            else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                if i % 2 == 0:
                    self.nodes[midpoint + math.ceil(offset_value) * 2].set_value(self.competitors[i])
                else:
                    self.nodes[midpoint - math.ceil(offset_value) * 2].set_value(self.competitors[i])
                offset_value = offset_value + 0.5
        offset_value = 0

        for i in range(self.num_competitors):
            if i < num_comp_nodes / 2:
                self.nodes[num_comp_nodes + (i * 2)].set_value("Loser")  # Fills in one competitor for each pairing
            else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                if i % 2 == 0:
                    self.nodes[midpoint + num_comp_nodes + math.ceil(offset_value) * 2].set_value("Loser")
                else:
                    self.nodes[midpoint + num_comp_nodes - math.ceil(offset_value) * 2].set_value("Loser")
                offset_value = offset_value + 0.5



    def account_for_bys(self):
        pass
        # for i in range(0, self.num_nodes - 2, 2):  # Go through all nodes and check for instances of bys. Update bracket accordingly.
        #     current_node = self.nodes[i]
        #     partner_node = self.nodes[i + 1]
        #     if current_node.get_value() == None and partner_node.get_value() == None:
        #         current_node.set_value(-1)
        #         partner_node.set_value(-1)
        #         current_node.get_next().set_value(-1)
        #     elif current_node.get_value() != None and partner_node.get_value() == None:
        #         partner_node.set_value(-1)
        #         current_node.get_next().set_value(current_node.get_value())
        #     elif current_node.get_value() == None and partner_node.get_value() != None:
        #         current_node.set_value(-1)
        #         partner_node.get_next().set_value(partner_node.get_value())
        #     else:
        #         current_node.get_next().set_value(-1)
        # for i in range(self.num_nodes - 2):  # Set empty nodes not due to bys back to None
        #     current_node = self.nodes[i]
        #     if current_node.get_value() != -1:
        #         current_node.get_next().set_value(None)
        # for i in range(self.num_nodes - 2):  # Automatically advance node in bracket if paired with a by node
        #     current_node = self.nodes[i]
        #     partner_node = self.nodes[i + 1]
        #     if current_node.get_value() != -1 and partner_node.get_value() == -1:
        #         partner_node.get_next().set_value(current_node.get_value())
        #         current_node.set_value(-1)
        # for i in range(self.num_nodes):
        #     if self.nodes[i].get_value() == "Loser":
        #         self.nodes[i].set_value("")
        # self.set_loser_starts()
        # print(self.get_num_levels())


    def find_pair(self, node_index):
        node_pair = 0
        if node_index % 2 == 0:  # Determine if node has a partner node has a competitor node ready
            node_pair = node_index + 1
        else:
            node_pair = node_index - 1
        return node_pair

    def reverse_bracket(self):
        self.nodes[self.num_nodes - 1].set_next([])
        for i in range(self.num_nodes - 2, -1, -1):
            node_list = []
            for j in range(len(self.nodes[i].get_next().get_next())):
                node_list.append(self.nodes[i].get_next().get_next()[j])
            node_list.append(self.nodes[i])
            self.nodes[i].get_next().set_next(node_list)
            self.nodes[i].set_next([])
        for i in range(int((self.num_nodes + 1) / 2)):
            self.nodes[i].set_next(None)


    def reverse_back(self):
        for i in range(int((self.num_nodes + 1) / 2), self.num_nodes, 1):
            for node in self.nodes[i].get_next():
                node.set_next(self.nodes[i])
        self.nodes[self.num_nodes - 1].set_next(None)

    def length_checker(self, node_list):
        count = 0
        for node in node_list:
            if node.get_value() != -1:
                count += 1
        return count

    def find_next(self, node_index):
        return self.nodes[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]


    def match_winner(self, node_index):
        print("winner")
        no_pair = False
        if node_index % 2 == 0:  # Determine if node has a partner node has a competitor node ready
            if self.nodes[node_index + 1].get_value() == None or self.nodes[node_index + 1].get_value() == "":
                no_pair = True
        else:
            if self.nodes[node_index - 1].get_value() == None or self.nodes[node_index - 1].get_value() == "":
                no_pair = True
        if no_pair == False:  # As long as there is competitor node ready
            node_pair = self.find_pair(node_index)
            next_node = self.nodes[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]
            while next_node != None and next_node.get_value() != None:
                if self.nodes.index(next_node) in self.losers:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes:
                    next_node = self.nodes[math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]
            next_node = self.nodes[node_index].get_next()
            while next_node != None and next_node.get_value() != None:
                if self.nodes.index(next_node) in self.losers:
                    next_node.set_value("")
                else:
                    next_node.set_value(None)
                if math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes:
                    next_node = self.nodes[math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]

            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.nodes[i].get_value() == None or self.nodes[i].get_value() == "":
                    self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.nodes[i])
                    self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.nodes[i])
            for val in self.losers:
                tester = False
                for val2 in self.winners_bracket_indexes:
                    if self.nodes[val2].get_next() == self.nodes[val]:
                        tester = True
                if tester == False:
                    self.nodes[val].set_value("")
            for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
                if self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == None or self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == "" or self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == None or self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == "":
                    if i in self.losers:
                        self.nodes[i].set_value("")
                    else:
                        self.nodes[i].set_value(None)
                    self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.nodes[i])
                    self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.nodes[i])

            self.nodes[node_index].set_next(self.nodes[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)])
            self.nodes[node_index].get_next().set_value(self.nodes[node_index].get_value())
            if node_pair in self.winners_bracket_indexes and node_pair != self.num_nodes - 3:
                if node_index % 2 == 0:
                    loser_index = 0
                    count = 0
                    while loser_index == 0:
                        if self.nodes[count].get_value() == "":
                            loser_index = count
                        else:
                            count += 1
                else:
                    loser_index = 0
                    count = 0
                    while loser_index == 0:
                        if self.nodes[count].get_value() == "":
                            loser_index = count
                        else:
                            count += 1
                self.nodes[node_pair].set_next(self.nodes[loser_index])
                self.nodes[loser_index].set_value(self.nodes[node_pair].get_value())





    def match_undo(self, node_index):
        print("undo")
        self.nodes[node_index].set_next(self.nodes[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)])
        next_node = self.nodes[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]
        while next_node != None and next_node.get_value() != None:
            if self.nodes.index(next_node) in self.losers:
                next_node.set_value("")
            else:
                next_node.set_value(None)
            if math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes:
                next_node = self.nodes[math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]
        next_node = self.nodes[self.find_pair(node_index)].get_next()
        while next_node != None and next_node.get_value() != None:
            if self.nodes.index(next_node) in self.losers:
                next_node.set_value("")
            else:
                next_node.set_value(None)
            if math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2) + 1 < self.num_nodes:
                next_node = self.nodes[math.floor(self.nodes.index(next_node) / 2) + int((self.num_nodes + 1) / 2)]

        for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
            if self.nodes[i].get_value() == None or self.nodes[i].get_value() == "":
                self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.nodes[i])
                self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.nodes[i])
        for val in self.losers:
            tester = False
            for val2 in self.winners_bracket_indexes:
                if self.nodes[val2].get_next() == self.nodes[val]:
                    tester = True
            if tester == False:
                self.nodes[val].set_value("")
        for i in range(self.num_nodes - 1, int((self.num_nodes + 1) / 2), -1):
            if self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].get_value() == None or self.nodes[
                (i - int((self.num_nodes + 1) / 2)) * 2].get_value() == "" or self.nodes[
                ((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == None or self.nodes[
                ((i - int((self.num_nodes + 1) / 2)) * 2) + 1].get_value() == "":
                if i in self.losers:
                    self.nodes[i].set_value("")
                else:
                    self.nodes[i].set_value(None)
                self.nodes[(i - int((self.num_nodes + 1) / 2)) * 2].set_next(self.nodes[i])
                self.nodes[((i - int((self.num_nodes + 1) / 2)) * 2) + 1].set_next(self.nodes[i])


    def check_done(self):
        if self.nodes[len(self.nodes) - 1].get_value() != None:
            return True
        else:
            return False

    def get_num_levels(self):
        return (math.ceil(math.log(self.num_competitors * 2, 2)) * 2) + 1  # Returns the number of levels the bracket has

    def get_levels(self):
        levels = []
        level = []
        current_node = 0
        node_range = math.floor(self.num_nodes / 2)
        level_count = math.ceil(self.num_nodes / 2)
        for node in self.nodes:  # Separate the nodes into a series of levels as is the structure of the bracket
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
        for node in self.nodes:  # Create a string representation of the graph for review purposes
            if current_node <= node_range:
                nodes_string += str(node.get_value()) + " "
            else:
                nodes_string += "\n"
                level_count = level_count / 2
                node_range = current_node + level_count
                nodes_string += str(node.get_value()) + " "
            current_node += 1
        return nodes_string