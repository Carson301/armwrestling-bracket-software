# Node Class
# Carson J. King
# 6-27-24


class Node:

    def __init__(self, data=None, next=None):
        self.dataval = data
        self.nextval = next

    def set_next(self, nextval):
        self.nextval = nextval

    def set_value(self, val):
        self.dataval = val

    def get_next(self):
        return self.nextval

    def get_value(self):
        return self.dataval