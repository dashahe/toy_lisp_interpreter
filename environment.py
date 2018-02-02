# 2018-02-02
# by xvvx

"""
class of environment table, which is a dictionary actually.
"""
class Environment:
    def __init__(self, parent):
        self.parent = parent
        self.frame = {}

    def add_variable(self, name, value):
        self.frame[name] = value
    
    def get_variable(self, name):
        if self.frame.get(name, False):
            return self.frame[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            return False
