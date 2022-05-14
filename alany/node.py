from typing import List
import math
from .memory import Memory, Data, parse_value
from .error import Error
from .result import Result

class Node(object):
    def __init__(self, command: str='', children=None, index: int=0, memory: Memory=None, is_interpreter: bool=False):
        self.command = command.replace('  ', ' ')
        if children is not None:
            self.children: List[Node] = children
        else:
            self.children: List[Node] = []
        self.index = index
        self.memory = memory
        self.is_interpreter = is_interpreter
        
    def get_args(self):
        args = remove_all_space(self.command).split('(')[1].split(')')[0].split(',')
        return args   
    
    def get_value(self, variable: str, file: str=None) -> any:
        if self.memory.in_memory(variable.split('(')[0]) and variable[-1] == ')':
            node: Node = self.memory.get_var(variable.split('(')[0]).value
            
            args_names = node.get_args()
            args = variable.split('(')[1][:-1].split(',')
            for i in range(len(args)):
                node.memory.add_var(value=args[i], var_name=args_names[i])
                
            return node.run_children(file).value
            
        elif self.memory.in_memory(variable.split('[')[0]) and variable[-1] == ']':
            var = self.memory.get_var(variable.split('[')[0]).get_list_value(self.get_value(variable.split('[')[1][:-1]))
            if isinstance(var, Data):
                return var.value
            else:
                return var
        else:
            val = parse_value(variable, self.memory)
            return val
        
    def set_value(self, variable: str, value: any, g=True) -> None:
        if isinstance(value, Data):
            value = value.value
        if self.memory.in_memory(variable):
            self.memory.get_var(variable).value = value
        elif variable[-1] == ']':
            var = self.memory.get_var(variable.split('[')[0])
            var.set_list_value(self.get_value(variable.split('[')[1][:-1]), value)
        else:
            if not g:
                self.memory.add_var(value, variable)
            else: 
                self.memory.add_global_var(value, variable)
        
    def get_bool_value(self, expression: str) -> bool:
        if '==' in expression:
            expression = expression.replace('==', ' ').split(' ')
            try:
                return self.get_value(expression[0]) == self.get_value(expression[1])
            except:
                return self.get_value(expression[0]) == self.get_value(expression[1])
        elif '!=' in expression:
            expression = expression.replace('!=', ' ').split(' ')
            try:
                return not self.get_value(expression[0]) == self.get_value(expression[1])
            except:
                return not self.get_value(expression[0]) == self.get_value(expression[1])
        elif '>' in expression:
            expression = expression.replace('>', ' ').split(' ')
            return self.get_value(expression[0]) > self.get_value(expression[1])
        elif '<' in expression:
            expression = expression.replace('<', ' ').split(' ')
            return self.get_value(expression[0]) < self.get_value(expression[1])
    
    def run(self, file: str) -> Result:
        commands = self.command.split(' ')
        commands_w = self.command.replace('=', '').replace('  ', ' ').split(' ')
        commands_c = self.command.replace('(', '').replace(')', '').split(' ')
        
        if commands[0] == 'print':
            values = commands[1:]
            for i, value in enumerate(values):
                val = str(self.get_value(value))
                if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
                    val = val[1:-1]
                values[i] = val
            print(' '.join(values), end='')
        elif commands[0] == 'putchar':
            print(chr(int(float(self.get_value(' '.join(commands[1:]))))), end='')
        elif commands_w[0] == 'var':
            if commands_w[1] == 'local':
                self.set_value(commands_w[2], self.get_value(' '.join(commands_w[3:])), g=False)
            else:
                self.set_value(commands_w[1], self.get_value(' '.join(commands_w[2:])), file) 
        elif commands_w[0] == 'len':
            self.set_value(commands_w[1], len(self.memory.get_var(commands_w[2]).value))
        elif commands_w[0] == 'array':
            if not commands_w[2] == 'none':
                values = []
                if commands_w[1] == 'local':
                    for value in commands_w[3:]:
                        values.append(self.get_value(value))
                    self.set_value(commands_w[2], values, g=False)
                else:
                    for value in commands_w[2:]:
                        values.append(self.get_value(value))
                    self.set_value(commands_w[1], values)
            else:
                if commands_w[1] == 'local':
                    self.set_value(commands_w[2], [], g=False)
                else:
                    self.set_value(commands_w[1], [])
        elif commands[0] == 'add':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if (not isinstance(a, int) and not isinstance(a, float)) or (not isinstance(b, int) and not isinstance(b, float)):
                Error.Runtime.not_a_number(a, b, fun='+')
                return Result(status=0)
            self.set_value(commands[1], a+b)
        elif commands[0] == 'sub':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='-')
                return Result(status=0)
            self.set_value(commands[1], a-b)
        elif commands[0] == 'div':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='/')
                return Result(status=0)
            self.set_value(commands[1], a/b)
        elif commands[0] == 'rdiv':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='%')
                return Result(status=0)
            self.set_value(commands[1], a%b)
        elif commands[0] == 'sin':
            a = self.get_value(commands[2])
            if not isinstance(a, int) and not isinstance(a, float):
                Error.Runtime.not_a_number(a, fun='sin')
                return Result(status=0)
            self.set_value(commands[1], math.sin(a))
        elif commands[0] == 'cos':
            a = self.get_value(commands[2])
            if not isinstance(a, int) and not isinstance(a, float):
                Error.Runtime.not_a_number(a, fun='cos')
                return Result(status=0)
            self.set_value(commands[1], math.cos(a))
        elif commands[0] == 'run':
            self.set_value(commands[1], eval(''.join(commands[2:])))
        elif commands[0] == 'break':
            return Result(status=2)
        elif commands[0] == 'mul':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, '*')
                return Result(status=0)
            self.set_value(commands[1], a*b)
        elif commands_c[0] == 'if':
            if self.get_bool_value(commands_c[1]):
                return self.run_children(file)
        elif commands_c[0] == 'repeat':
            for i in range(int(self.get_value(commands_c[1]))):
                result = self.run_children(file)
                if result.status == 2:
                    return result
                if not result.is_success():
                    return Result(status=0)
        elif commands_c[0] == 'while':
            while self.get_bool_value(commands_c[1]):
                result: Result = self.run_children(file)
                if result.status == 2:
                    return result
                elif not result.is_success():
                    return Result(status=0)
        elif commands_c[0] == 'def':
            var_name = commands[1].split('(')[0]
            self.memory.add_global_var(value=self, var_name=var_name)
        elif commands[0] == 'append':
            self.memory.get_var(commands[1])._value.append(self.get_value(commands[2]))
        elif commands[0] == 'runfun':
            node: Node = self.memory.get_var(commands[1]).value
            
            try:
                args_names = node.get_args()
                args = commands[2:]
                for i in range(len(args)):
                    node.memory.add_var(value=args[i], var_name=args_names[i])
            except:
                pass
            
            res = node.run_children(file)
            return res
        elif commands[0] == 'convert':
            if commands[1] == 'int':
                self.memory.get_var(commands[2]).type = 'int'
                self.memory.get_var(commands[2]).value = int(self.memory.get_var(commands[2]).value)
        elif commands[0] == 'type':
            print(self.memory.get_var(commands[1]).type)
        elif commands[0] == 'import':
            from .parser import Lexer, Parser
            path = commands[1]
            if not path[0] == '/':
                path = "/".join(file.split("/")[:-1]) + "/" + path + ".aln"
            with open(path, 'r') as fl:
                code = fl.read()
            lexer = Lexer(code)
            lexer.parse()
            code = lexer.code
            parser = Parser(code=code, memory=self.memory)
            node = parser.parse()[0]
            node.run(path)
        elif commands[0] == 'return':
            value = self.get_value(' '.join(commands[1:]))
            return Result(status=2, value=value)
        elif self.is_interpreter == True:
            values = []
            for i in commands:
                if not i == '':
                    values.append(i)
            for i, value in enumerate(values):
                val = str(self.get_value(value))
                if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
                    val = val[1:-1]
                values[i] = val
            if len(values) > 0:
                print(' '.join(values))
        else:
            return self.run_children(file)
        return Result(status=1)
                
    def run_children(self, file) -> Result:
        for child in self.children:
            result: Result = child.run(file)
            if not result.is_success():
                return result
            if result.status == 2:
                return result
        return Result(status=1)
    
def remove_all_space(string: str):
    return string.replace(' ', '')