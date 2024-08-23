#
#
#

from Bracket import Bracket

import math
import Node
import random


class SingleBracket(Bracket):

    competitor_list = []
    bracket_name = ""
    node_list = []
    level_list = []
    num_competitors = 0
    num_nodes = 0

    # ================================================================================================================ #
    # Bracket Set-Up Methods

    def get_bracket_name(self):
        return self.bracket_name

    def create_bracket(self):
        self.node_list = []
        # Calculates the number of nodes for a complete bracket given a number of competitors
        self.num_nodes = (2 ** (math.ceil(math.log(self.num_competitors, 2)) + 1) - 1)
        # Add empty nodes to node_list
        for i in range(self.num_nodes):
            self.node_list.append(Node.Node(None))
        # Calculate the index of the first node on the next level of the bracket
        current_node = math.ceil(self.num_nodes / 2)
        # Has nodes point to one another to create a bracket structure
        for i in range(self.num_nodes - 1):
            self.node_list[i].set_next(self.node_list[math.floor(current_node)])
            current_node += 0.5  # NOTE: 2 nodes point to a node or a parent

        self.set_level_list()


    def fill_bracket(self):
        # Value to offset the placement of competitors in the bracket
        offset_value = 0
        # Number of source nodes in bracket/starting nodes/potential competitors
        num_comp_nodes = int(math.ceil(self.num_nodes / 2))
        # Value representing a midpoint to begin adding to within the bracket
        midpoint = int(num_comp_nodes / 2) + 1
        # Set both competitor starts and the initial loser starts to there base values
        if self.num_competitors == 2:
            self.node_list[0].set_value(self.competitor_list[0])
            self.node_list[1].set_value(self.competitor_list[1])
        else:
            for i in range(self.num_competitors):
                if i < num_comp_nodes / 2:
                    self.node_list[i * 2].set_value(self.competitor_list[i])
                else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                    if i % 2 == 0:
                        self.node_list[midpoint + math.ceil(offset_value) * 2].set_value(self.competitor_list[i])
                    else:
                        self.node_list[midpoint - math.ceil(offset_value) * 2].set_value(self.competitor_list[i])
                    offset_value = offset_value + 0.5

    def account_for_bys(self):
        # Set each nodes next node to what it equals
        for i in range(self.num_nodes - 1):
            current_node = self.node_list[i]
            if self.node_list.index(current_node.get_next()) != self.num_nodes - 1:
                if current_node.get_value() is None:
                    current_node.set_value(-1)
                else:
                    current_node.get_next().set_value(current_node.get_value())
        # Set empty nodes not due to bys back to None
        for i in range(self.num_nodes - 2):
            current_node = self.node_list[i]
            if current_node.get_value() != -1:
                current_node.get_next().set_value(None)
        # Automatically advance node in bracket if paired with a by node
        for i in range(self.num_nodes - 2):
            current_node = self.node_list[i]
            partner_node = self.node_list[self.find_pair(i)]
            if current_node.get_value() != -1 and partner_node.get_value() == -1:
                partner_node.get_next().set_value(current_node.get_value())
                current_node.set_value(-1)
        print("jo")
        for node in self.node_list:
            print(node.get_value())
        print("Shmo")



    # ================================================================================================================ #
    # Bracket Altering Methods

    def reset_nodes(self, node_index):
        # Get the node that this node points to/This is where the winner of the match is stored
        next_node = self.node_list[node_index].get_next()
        # Adjust bracket if declaration of a winner requires previous decisions to be undone
        while next_node is not None and next_node.get_value() is not None:
            next_node.set_value(None)
            next_node = next_node.get_next()

    def match_winner(self, node_index):
        self.reset_nodes(node_index)
        # Set the node both nodes point to as the given node/setting a winner
        self.node_list[node_index].get_next().set_value(self.node_list[node_index].get_value())

    def match_undo(self, node_index):
        self.reset_nodes(node_index)

    # ================================================================================================================ #
    # Helper Functions

    def find_index(self, node):
        return self.node_list.index(node)

    def find_pair(self, node_index):
        if node_index % 2 == 0:
            return node_index + 1
        else:
            return node_index - 1

    def find_pair_node(self, node):
        node_index = self.find_index(node)
        if node_index % 2 == 0:
            return self.node_list[node_index + 1]
        else:
            return self.node_list[node_index - 1]

    def check_if_pair(self, node_index):
        if self.node_list[self.find_pair(node_index)].get_value() is None:
            return False
        else:
            return True

    def find_default_next(self, node_index):
        return self.node_list[math.floor(node_index / 2) + int((self.num_nodes + 1) / 2)]

    def check_done(self):
        if self.node_list[self.num_nodes - 1].get_value() is not None:
            return True
        else:
            return False

    # ================================================================================================================ #
    # Setters and Getters

    def get_num_levels(self):
        if self.num_competitors == 0:
            return 0
        else:
            return math.ceil(math.log(self.num_competitors, 2)) + 1

    def begin_bracket(self):
        if self.num_competitors != 0:
            self.create_bracket()
            self.fill_bracket()
            self.account_for_bys()

    def set_level_list(self):
        self.level_list, level = [], []
        # Index of the current node being evaluated
        current_node = 0
        # The current range of nodes for the current level
        current_node_range = math.floor(self.num_nodes / 2)
        # The number of nodes that the current level has
        nodes_per_level = math.ceil(self.num_nodes / 2)
        for node in self.node_list:  # Separate the nodes into a series of levels as is the structure of the bracket
            # If the current node is within the node range add it to the level
            if current_node <= current_node_range:
                level.append(node)
            else:
                # Add finished level to levels
                self.level_list.append(level)
                # Halve the level_count for the next level
                nodes_per_level = nodes_per_level / 2
                # Update the node range by adding the new level count
                current_node_range = current_node_range + nodes_per_level
                # Reset level and add the newest node to it
                level = [node]
            current_node += 1
        # Add the final level to levels
        self.level_list.append(level)

    def get_level_list(self):
        return self.level_list

    # ================================================================================================================ #
    # To String Method

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

