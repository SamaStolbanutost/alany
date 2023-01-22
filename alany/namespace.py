from error import Error


class Namespace(object):
    def __init__(self, parent=None):
        self.parent: Namespace = parent
        self.variables = {}
        self.globals = []

    def get_variable(self, name: str):
        if name in self.globals:
            return self.get_global().get_variable(name)
        elif name in self:
            return self.variables[name]
        elif self.is_in(name):
            return self.parent.get_variable(name)
        else:
            Error.Runtime.not_existing_variable(name)

    def get_global(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_global()

    def set_variable(self, name: str, value: any):
        self.variables[name] = value

    def is_in(self, name: str):
        p = self.parent is not None and self.parent.is_in(name)
        return name in self or p

    def __contains__(self, name):
        return name in self.variables


class Cell(object):
    pass


g = Namespace()
local = Namespace(parent=g)

local.set_variable('a', 'Hello, ')
g.set_variable('b', 'world!')
