#
#
#

class Division:

    competitors = []
    bracket = [[]]

#==========================================================#
    # Constructors

    def __init__(self, competitors):
        self.set_competitors(competitors)

#==========================================================#
    # Setters

    def set_competitors(self, competitors):
        self.competitors = competitors

#==========================================================#
    # Getters

    def get_competitors(self, competitors):
        return self.competitors



#==========================================================#
    # Additional Methods

    def add_competitor(self, competitor):
        self.competitors.append(competitor)

    def remove_competitor(self, competitor):
        try:
            self.competitors.remove(competitor)
        except ValueError:

            if self.nodes[node_index].get_next().get_value() != None:
                checker = False
                loser_index = 0
                for i in range(int((self.num_nodes + 1) / 4), self.num_nodes):
                    if checker == False and (
                            self.nodes[i].get_value() == self.nodes[self.find_pair(node_index)].get_value() or
                            self.nodes[i].get_value() == self.nodes[node_index].get_value()):
                        checker = True
                        loser_index = i
                next_pair = self.nodes[loser_index].get_next()  # Get the next node
                while next_pair != None and next_pair.get_value() != None:  # Adjust graph to account for undoing of this match result
                    next_pair.set_value(None)
                    next_pair = next_pair.get_next()
                self.nodes[loser_index].set_value("")
            pass

    def empty_division(self):
        self.competitors.clear()

        node_pair = self.find_pair(node_index)
        next_node = self.nodes[node_pair].get_next()  # Get the next node
        # current pairs next
        while next_node != None and next_node.get_value() != None:  # Adjust graph to account for undoing of this match result
            if self.nodes.index(next_node) not in self.winners_bracket_indexes:
                next_node.set_value("")
            else:
                next_node.set_value(None)
            next_node = next_node.get_next()
        next_node = self.nodes[node_pair].get_next()
        if self.nodes.index(next_node) < self.num_nodes - 3:
            self.nodes[self.nodes.index(next_node)].set_next(self.nodes[math.floor(self.nodes.index(next_node) / 2) + 8])
        next_node = next_node.get_next()
        # Next node correct
        while next_node != None and next_node.get_value() != None:  # Adjust graph to account for undoing of this match result
            if self.nodes.index(next_node) not in self.winners_bracket_indexes:
                next_node.set_value("")
            else:
                next_node.set_value(None)
            next_node = next_node.get_next()
        # Loser node
        next_node = self.nodes[node_index].get_next()  # Get the next node
        while next_node != None and next_node.get_value() != None:  # Adjust graph to account for undoing of this match result
            if self.nodes.index(next_node) not in self.winners_bracket_indexes:
                next_node.set_value("")
            else:
                pass
            next_node.set_value(None)
            next_node = next_node.get_next()
        self.nodes[node_index].set_next(self.nodes[math.floor(node_index / 2) + 8])
        self.nodes[node_index].get_next().set_value(
            self.nodes[node_index].get_value())  # Set the node both nodes point to as the given node/setting a winner

    def create_bracket(self):
        pass

    def __str__(self):
        division_string = ""
        for competitor in self.competitors:
            division_string += str(competitor) + "\n"
        return division_string

