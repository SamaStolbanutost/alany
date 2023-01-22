from typing import Dict
# from .error import Error
from .functions import add_str, check_type


class Memory(object):
    def __init__(self):
        self.variables: Dict[Data] = {}

    def in_memory(self, variable: str):
        if variable in self.variables:
            return True

    def get(self, variable: str):
        return self.variables[variable]

    def set(self, variable: str, value):
        self.variables[variable] = value


class Data(object):
    def __init__(self, memory: Memory, type: str, value: any = None):
        self.memory: Memory = memory
        self.type: str = type
        self.set_value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if check_type(value, self.type):
            self.value: any = value
        else:
            raise ValueError(f'Not {self.type}')

    def __eq__(self, other):
        if isinstance(other, Data):
            return self.value == other.value
        return NotImplemented

    def __str__(self):
        if self.type == 'str':
            return self.get_value()
        elif self.type == 'int' or self.type == 'float':
            return str(self.get_value())
        elif self.type == 'bool':
            return 'true' if self.value else 'false'
        elif self.type == 'list':
            return NotImplemented
        elif self.type == 'node':
            return NotImplemented
        elif self.type == 'class':
            return NotImplemented

    def __repr__(self):
        return str(self)


def to_value(value: any):
    if isinstance(value, Data):
        return to_value(value.value)
    else:
        return value


def parse_string(value: any, memory: Memory) -> str:
    value = to_value(value)
    escape_symbols = {'\\0': '\0', '\\n': '\n', '\\r': '\r', '\\t': '\t',
                      '\\v': '\v', '\\\\': '\\',  "\'": "\'", '\"': '\"',
                      '\\a': '\a'}

    try:
        if value == 'input':
            value = add_str(input())
        elif value == 'space':
            value = add_str(' ')
        elif value == 'none':
            value = add_str('')
        elif value in escape_symbols:
            value = add_str(escape_symbols[value])
    except Exception:
        pass
    finally:
        value = Data(value=value, memory=memory, skip_unknown=True,
                     type='str').value
    return value
