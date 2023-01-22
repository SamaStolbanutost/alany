from .memory import Data

class Str(Data):
    def __str__(self):
        return self.get()

class Int(Data):
    def __str__(self):
        return str(self.get())

class Float(Data):
    def __str__(self):
        return str(self.get())

class Bool(Data):
    def __str__(self):
        return self.get()

class List(Data):
    def __str__(self):
        return NotImplemented

class Node(Data):
    def __str__(self):
        return NotImplemented

class Class(Data):
    def __str__(self):
        return NotImplemented
