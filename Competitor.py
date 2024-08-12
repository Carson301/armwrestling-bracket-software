#
#
#

class Competitor:
    name = "John Doe"
    weight = 0
    divisions = []

#==========================================================#
    # Constructors

    def __init__(self, name, weight, divisions):
        self.set_name(name)
        self.set_weight(weight)
        self.set_divisions(divisions)

#==========================================================#
    # Setters
    def set_name(self, name):
        self.name = name

    def set_weight(self, weight):
        self.weight = weight

    def set_divisions(self, divisions):
        self.divisions = divisions

#==========================================================#
    # Getters
    def get_name(self):
        return self.name

    def get_weight(self):
        return self.weight



    def get_divisions(self):
        return self.divisions

#==========================================================#
    # Additional Methods

    def __str__(self):
        competitor_string = ""
        competitor_string += self.name + "\n" + str(self.weight) + "\n"
        for division in self.divisions:
            competitor_string += division + " "
        return competitor_string



