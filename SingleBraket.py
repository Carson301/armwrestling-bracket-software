#
#
#

import math
import Node
import random


class SingleBraket:

    competitors = []
    num_competitors = 0
    num_nodes = 0
    nodes = []

    def __init__(self, competitors):
        self.competitors = competitors  # List of competitors
        self.num_competitors = len(competitors)  # Number of competitors
        self.create_bracket()  # Call helper function to create bracket structure
        self.fill_bracket()  # Call helper function to fill in the bracket
        self.account_for_bys()  # Call helper function to adjust for bys in the bracket

    def create_bracket(self):
        self.num_nodes = 2 ** (math.ceil(math.log(self.num_competitors, 2)) + 1) - 1  # Calculates number of nodes for bracket
        for i in range(self.num_nodes):
            self.nodes.append(Node.Node(i))  # Add num_nodes of node empty objects
        current_node = math.ceil(self.num_nodes / 2)  # Calculate the index of the first node on the next level of the bracket
        for i in range(self.num_nodes - 1):
            self.nodes[i].set_next(self.nodes[math.floor(current_node)]) # Has nodes point to one another to create a bracket structure
            current_node += 0.5  # NOTE: 2 nodes point to a node or a parent
        for i in range(len(self.nodes)):
            self.nodes[i].set_value(None)  # Set every node's value to None
        random.shuffle(self.competitors)  # Randomizes the competitor list

    def fill_bracket(self):
        offset_value = 0  # Value to offset the placement of competitors in the bracket
        num_source_nodes = int(math.ceil(self.num_nodes / 2))  # Number of source nodes in bracket/starting nodes/potential competitors
        midpoint = int(num_source_nodes / 2) + 1  # Value representing a midpoint to begin adding to within the bracket
        for i in range(self.num_competitors):
            if i < num_source_nodes / 2:
                self.nodes[i * 2].set_value(self.competitors[i])  # Fills in one competitor for each pairing
            else:  # Then fills in competitors beginning at the midpoint and alternating directions per addition
                if i % 2 == 0:
                    self.nodes[midpoint + math.ceil(offset_value) * 2].set_value(self.competitors[i])
                else:
                    self.nodes[midpoint - math.ceil(offset_value) * 2].set_value(self.competitors[i])
                offset_value = offset_value + 0.5

    def account_for_bys(self):
        for i in range(0, self.num_nodes - 2, 2):  # Go through all nodes and check for instances of bys. Update bracket accordingly.
            current_node = self.nodes[i]
            partner_node = self.nodes[i + 1]
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
        for i in range(self.num_nodes - 2):  # Set empty nodes not due to bys back to None
            current_node = self.nodes[i]
            if current_node.get_value() != -1:
                current_node.get_next().set_value(None)
        for i in range(self.num_nodes - 2):  # Automatically advance node in bracket if paired with a by node
            current_node = self.nodes[i]
            partner_node = self.nodes[i + 1]
            if current_node.get_value() != -1 and partner_node.get_value() == -1:
                partner_node.get_next().set_value(current_node.get_value())
                current_node.set_value(-1)

    def match_winner(self, node_index):
        no_pair = False
        if node_index % 2 == 0:  # Determine if node has a partner node has a competitor node ready
            if self.nodes[node_index + 1].get_value() == None:
                no_pair = True
        else:
            if self.nodes[node_index - 1].get_value() == None:
                no_pair = True
        if no_pair == False:  # As long as there is competitor node ready
            next_node = self.nodes[node_index].get_next()  # Get the node that this node points to/This is where the winner of the match is stored
            while next_node != None and next_node.get_value() != None:  # Adjust bracket if declaration of a winner requires previous decisions to be undone
                next_node.set_value(None)
                next_node = next_node.get_next()
            self.nodes[node_index].get_next().set_value(self.nodes[node_index].get_value())  # Set the node both nodes point to as the given node/setting a winner
    def undo_match(self, node_index):
        next_node = self.nodes[node_index].get_next()  # Get the next node
        while next_node != None and next_node.get_value() != None:  # Adjust graph to account for undoing of this match result
            next_node.set_value(None)
            next_node = next_node.get_next()

    def get_bracket(self):
        return self.nodes

    def get_num_competitors(self):
        return self.num_competitors

    def get_num_nodes(self):
        return self.num_nodes

    def get_num_levels(self):
        return math.ceil(math.log(self.num_competitors, 2)) + 1  # Returns the number of levels the bracket has

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







