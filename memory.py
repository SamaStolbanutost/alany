class Memory(object):
    def __init__(self, parent=None, children=[], defs: dict[str]={}):
        self.parent: Memory = parent
        self.children: list[Memory] = children
        self.variables: dict[str, Data] = {}
        self.defs = defs
        
    def add_var(self, value: any, var_name: str):
        self.variables[var_name] = Data(memory=self, value=clear_parse_value(value, self), var_name=var_name)
        
    def set_var(self, value: any, var_name: str):
        self.variables[var_name]._value = clear_parse_value(value, self)
        
    def get_var(self, var_name: str):
        try:
            return self.variables[var_name]
        except:
            return parse_value(var_name, self)
        
class Data(object):
    def __init__(self, memory=None, value: any=None, var_name: str=None):
        self.var_name = str(var_name)
        self.memory: Memory = memory
        self._value = None
        
        self.type = None
        try:
            if (value[0] == "'" and value[-1] == "'") or (value[0] == '"' and value[-1] == '"'):
                value = str(value[1:-1])
                self.type = 'str'
            else:
                raise 'Not str'
        except:
            try:
                value = int(value)
                self.type = 'int'
            except:
                try:
                    value = float(value)
                    self.type = 'float'
                except:
                    if isinstance(value, list):
                        self.type = 'list'
                        for i, dat in enumerate(value):
                            if not isinstance(dat, Data):
                                value[i] = Data(None, dat)
        
        if self.type is None:
            if value in self.memory.variables and not self.memory is None:
                self._value = self.memory.variables[value]._value
                self.type = self.memory.variables[value].type
                self.var_name = self.memory.variables[value].var_name
            else:
                from compiler import Error
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
        if not self.memory is None:
            self.memory.set_var(Data(value=self._value, memory=self.memory), self.var_name)
        
    def get_list_value(self, index):
        if isinstance(index, Data):
            index = index.value
        vl = to_value(self)
        var = vl[int(index)]
        if isinstance(var, Data):
            return var.value
        else:
            return var
    
    def set_list_value(self, index, value):
        if isinstance(index, Data):
            index = index.value
        vl = to_value(self)
        vl[int(index)] = value
        if not self.memory is None:
            self.memory.set_var(self._value, self.var_name)
    
    def __eq__(self, other):
        if isinstance(other, Data):
            return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __repr__(self):
        return to_string(self)
        # if not self.type == 'list':
        #     return str(self._value)
        # else:
        #     arr = []
        #     for i in self._value:
        #         if isinstance(i, Data):
        #             arr.append(i._value)
        #         else:
        #             arr.append(i)
        #     return f'[{",".join(arr)}]'
        
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
    if value == 'input':
        value = "'" + input() + "'"
    elif value == 'space':
        value = "'" + ' ' +  "'"
    elif value == 'none':
        value = "'" + '' +  "'"
    elif value == '\\n':
        value = "'" + '\n' +  "'"
    elif value == '\\x1b':
        value = "'" + '\x1b' +  "'"
    value = Data(value=value, memory=memory).value
    return value