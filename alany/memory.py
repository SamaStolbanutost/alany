from typing import List, Dict
from .error import Error
from .functions import add_str, remove_start_spaces, is_string, to_len


class Memory(object):
    def __init__(self, parent=None, children=[]):
        self.parent: Memory = parent
        self.children: List[Memory] = children
        self.variables: Dict[str, Data] = {}

    def add_var(self, value: any, var_name: str):
        self.variables[var_name] = Data(memory=self,
                                        value=clear_parse_value(value, self),
                                        var_name=var_name)

    def add_global_var(self, value: any, var_name: str):
        if self.parent is not None:
            self.parent.add_global_var(value=value, var_name=var_name)
        else:
            self.add_var(value=value, var_name=var_name)

    def set_var(self, value: any, var_name: str):
        if var_name in self.variables:
            self.variables[var_name]._value = clear_parse_value(value, self)
        elif self.parent is not None:
            self.parent.set_var(value=value, var_name=var_name)

    def in_memory(self, var_name: str):
        if var_name in self.variables:
            return True
        elif self.parent is not None:
            return self.parent.in_memory(var_name)
        else:
            return False

    def get_var(self, var_name: str):
        if var_name in self.variables:
            return self.variables[var_name]
        elif self.parent is not None:
            return self.parent.get_var(var_name=var_name)
        else:
            return parse_value(var_name, self)

    def get_value(self, variable: str, file: str = None) -> any:
        from .node import Node

        try:
            ends = variable[-1]
        except Exception:
            ends = ''
        if self.in_memory(variable.split('(')[0]) and ends == ')':
            node: Node = self.get_var(variable.split('(')[0]).value

            args_names = node.get_args()
            args = variable.split('(')[1][:-1].split(',')
            for i in range(len(args)):
                value = self.get_value(args[i])
                var_name = args_names[i]
                node.memory.add_var(value=value, var_name=var_name)

            return node.run_children(file).value
        elif self.in_memory(variable.split('[')[0]) and ends == ']':
            var = self.get_var(variable.split('[')[0])
            val = self.get_value(variable.split('[')[1][:-1])
            var = var.get_list_value(val)
            if isinstance(var, Data):
                return var.value
            else:
                return var
        else:
            val = parse_value(variable, self)
            return val


class Data(object):
    def __init__(self, memory, value: any = None, var_name: str = None):
        from .node import Node

        self.var_name = str(var_name)
        self.memory: Memory = memory
        self._value = None

        self.type = None
        try:
            if is_string(value):
                value = str(value[1:-1])
                self.type = 'str'
            else:
                raise 'Not str'
        except Exception:
            try:
                if isinstance(value, float):
                    raise 'Not int'
                value = int(value)
                self.type = 'int'
            except Exception:
                try:
                    value = float(value)
                    self.type = 'float'
                except Exception:
                    if isinstance(value, list):
                        self.type = 'list'
                        for i, dat in enumerate(value):
                            if not isinstance(dat, Data):
                                value[i] = Data(memory=self.memory, value=dat)
                    elif isinstance(value, Node):
                        self.type = 'node'

        if self.type is None:
            value = remove_start_spaces(value)
            if self.memory.in_memory(value) and self.memory is not None:
                var = self.memory.get_var(value)
                self._value = var._value
                self.type = var.type
                self.var_name = var.var_name
            else:
                Error.Runtime.unknow_type(value)
        else:
            self._value: any = value

    def get_value(self):
        if self.type == 'list':
            return self._value
        elif self.type == 'str':
            value = to_value(self._value)
            return "'" + value + "'"
        else:
            value = self._value
            return to_value(value)

    def set_value(self, value):
        if isinstance(value, Data):
            self._value = value.value
        else:
            self._value = value
        if self.memory is not None:
            data = Data(value=self._value, memory=self.memory)
            self.memory.set_var(data, self.var_name)

    def get_list_value(self, index):
        if isinstance(index, Data):
            index = index.value
        vl = to_value(self)
        index = int(index)
        index = to_len(index, len(vl))

        var = vl[index]
        if isinstance(var, Data):
            return var.value
        else:
            return var

    def set_list_value(self, index, value):
        if isinstance(index, Data):
            index = index.value
        vl = to_value(self)
        vl[int(index)] = value
        if self.memory is not None:
            self.memory.set_var(self._value, self.var_name)

    def __eq__(self, other):
        if isinstance(other, Data):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self):
        return to_string(self)

    value = property(get_value, set_value)


def parse_value(value: any, memory: Memory):
    return clear_parse_value(value, memory)


def to_string(value: Data):
    if not isinstance(value, Data):
        return value
    else:
        if not value.type == 'list':
            res = str(value._value)
            return res
        else:
            arr = []
            for i in value._value:
                arr.append(to_string(i))
            return f'[{",".join(arr)}]'


def to_value(value: any):
    if isinstance(value, Data):
        return to_value(value.value)
    else:
        return value


def clear_parse_value(value: any, memory):
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
        value = Data(value=value, memory=memory).value
    return value
