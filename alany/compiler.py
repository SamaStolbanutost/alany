import math
import time
from .memory import Memory, Data, parse_value
from typing import List

class Error:
    class Runtime:
        def not_a_number(value_1: any, value_2: any=None, fun: str='') -> None:
            if value_1 is not None:
                print(f'RuntimeError: Not a number {value_1} {fun} {value_2}')
            else:
                print(f'RuntimeError: Not a number {fun}({value_1})')
                
        def unknow_type(value: any) -> None:
            print(f'RuntimeError: Unknow type {value}')
    
    class Programm:
        def stop() -> None:
            print('Program: Stopped with error')
  
class Result(object):
    def __init__(self, status=1, value=None):
        self.status = status
        self.value = value
        
    def is_success(self) -> bool:
        if self.status in [1, 2]:
            return True
        else:
            return False

class Node(object):
    def __init__(self, command: str='', children=None, index: int=0, memory: Memory=None):
        self.command = command.replace('  ', ' ')
        if children is not None:
            self.children: List[Node] = children
        else:
            self.children: List[Node] = []
        self.index = index
        self.memory = memory
        
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
                
def remove_space(string: str):
    if string and string[0] == ' ':
        string = string[1:]
        return remove_space(string)
    else:
        return string
                
class Parser(object):
    def __init__(self, code: str, memory: Memory):
        self.code: str = code
        self.memory: Memory = memory
        
    def parse(self, i=-1) -> List[Node]:
        main_node = Node(memory=self.memory)
        code = self.code.split(';')
        
        con_to = i
        con = True
        for i, command in enumerate(code):
            if con and i <= con_to:
                continue
            if con and i > con_to:
                con = False
            command = remove_space(command)
            if command.split(' ')[0] in ['if', 'repeat', 'while', 'def']:
                #print(1)
                self.memory = Memory(parent=self.memory)
                node = Node(command, index=i, memory=self.memory)
                result = self.parse(i)
                node.children = result[0].children
                main_node.children.append(node)
                con = True
                con_to = result[1]
            elif command.split(' ')[0] == 'endblock':
                self.memory = self.memory.parent
                return [main_node, i]
            else:
                main_node.children.append(Node(command, index=i, memory=self.memory))
                
        return [main_node, i]
    
class Lexer(object):
    def __init__(self, code: str):
        self.code: str = code
        
    def parse(self) -> str:
        self.code = self.code.replace('\n', '')
        self.code = self.code.replace('    ', '').replace('   ', '').replace('  ', '')
        self.code = self.code.replace(' {', ';').replace('{', ';').replace('}', 'endblock;')
        self.code = self.code.replace(' == ', '==').replace(' != ', '!=').replace(' > ', '>').replace(' < ', '<')
        return self.code
        
class Main(object):
    def __init__(self, code: str):
        self.code: str = code
        self.lexer = Lexer(self.code)
        
    def run(self, file: str) -> Result:
        self.memory = Memory()
        self.lexer.parse()
        self.code = self.lexer.code
        self.parser = Parser(self.code, self.memory)
        self.node = self.parser.parse()[0]
        return self.node.run(file)
    
    

# parser = Parser()
# main_node = parser.parse(code)[0]
# for node in main_node.children:
#     print(1)
#     print(node.children, node.command)
#     for child in node.children:
#         print(2)
#         print(child.children, child.command)
#         for chil in child.children:
#             print(3)
class Compiler():
    def __init__(self):
        pass
    
    def run_file(self, file) -> None:
        with open(file, 'r') as fl:
            self.run(fl.read(), file=file)

    def run(self, code, file) -> None:
        tm = time.time()
        main = Main(code)
        result = main.run(file)
        if result.is_success():
            print(f'Program: Completed in {time.time()-tm} seconds')
        else:
            Error.Programm.stop()
            

# c = Compiler()
# c.run_file('examples/return.aln')