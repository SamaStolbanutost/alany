import math
import time
from memory import Memory, Data, parse_value

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
  


class Node(object):
    def __init__(self, command: str='', children=None, index: int=0, memory: Memory=None):
        self.command = command.replace('  ', ' ')
        if children is not None:
            self.children: list[Node] = children
        else:
            self.children: list[Node] = []
        self.index = index
        self.memory = memory
    
    def get_value(self, variable: str) -> any:
        # print(memory)
        # if variable in self.memory.variables:
        #     var = self.memory.get_var(variable).value
        #     if isinstance(var, Data):
        #         return var.value
        #     else:
        #         return var
        if variable.split('[')[0] in self.memory.variables and variable[-1] == ']':
            var = self.memory.get_var(variable.split('[')[0]).get_list_value(self.get_value(variable.split('[')[1][:-1]))
            if isinstance(var, Data):
                return var.value
            else:
                return var
        else:
            val = parse_value(variable, self.memory)
            return val
        
    def set_value(self, variable: str, value: any) -> None:
        if isinstance(value, Data):
            value = value.value
        if variable in self.memory.variables:
            self.memory.get_var(variable).value = value
        elif variable[-1] == ']':
            # print(len(memory[variable.split('[')[0]]))
            # print(float(self.get_value(variable.split('[')[1][:-1])))
            var = self.memory.get_var(variable.split('[')[0])
            var.set_list_value(self.get_value(variable.split('[')[1][:-1]), value)
        else:
            self.memory.add_var(value, variable)
        
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
    
    def run(self, file: str) -> any:
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
        if commands[0] == 'putchar':
            print(chr(int(float(self.get_value(' '.join(commands[1:]))))), end='')
        elif commands_w[0] == 'var':
            self.set_value(commands_w[1], self.get_value(' '.join(commands_w[2:])))
        elif commands_w[0] == 'len':
            self.set_value(commands_w[1], len(self.memory.variables[commands_w[2]].value))
        elif commands_w[0] == 'array':
            if not commands_w[2] == 'none':
                values = []
                for value in commands_w[2:]:
                    values.append(self.get_value(value))
                self.set_value(commands_w[1], values)
            else:
                self.set_value(commands_w[1], [])
        elif commands[0] == 'add':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if (not isinstance(a, int) and not isinstance(a, float)) or (not isinstance(b, int) and not isinstance(b, float)):
                Error.Runtime.not_a_number(a, b, fun='+')
                return False
            self.set_value(commands[1], a+b)
        elif commands[0] == 'sub':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='-')
                return False
            self.set_value(commands[1], a-b)
        elif commands[0] == 'div':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='/')
                return False
            self.set_value(commands[1], a/b)
        elif commands[0] == 'rdiv':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, fun='%')
                return False
            self.set_value(commands[1], a%b)
        elif commands[0] == 'sin':
            a = self.get_value(commands[2])
            if not isinstance(a, int) and not isinstance(a, float):
                Error.Runtime.not_a_number(a, fun='sin')
                return False
            self.set_value(commands[1], math.sin(a))
        elif commands[0] == 'cos':
            a = self.get_value(commands[2])
            if not isinstance(a, int) and not isinstance(a, float):
                Error.Runtime.not_a_number(a, fun='cos')
                return False
            self.set_value(commands[1], math.cos(a))
        elif commands[0] == 'run':
            self.set_value(commands[1], eval(''.join(commands[2:])))
        elif commands[0] == 'break':
            return 'break'
        elif commands[0] == 'mul':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            if not isinstance(a, int) and not isinstance(a, float) or not isinstance(b, int) and not isinstance(b, float):
                Error.Runtime.not_a_number(a, b, '*')
                return False
            self.set_value(commands[1], a*b)
        elif commands_c[0] == 'if':
            #print(1)
            #print(self.get_value(commands[1]))
            #print(self.get_value(commands[2]))
            if self.get_bool_value(commands_c[1]):
                return self.run_children(file)
        elif commands_c[0] == 'repeat':
            for i in range(int(self.get_value(commands_c[1]))):
                result = self.run_children(file)
                if result == 'break':
                    break
                if (not result) and (not result == 'break'):
                    return False
        elif commands_c[0] == 'while':
            while self.get_bool_value(commands_c[1]):
                result = self.run_children(file)
                if result == 'break':
                    break
                if (not result) and (not result == 'break'):
                    return False
        elif commands_c[0] == 'def':
            self.memory.defs[commands_c[1]] = self
        elif commands[0] == 'append':
            self.memory.get_var(commands[1])._value.append(self.get_value(commands[2]))
        elif commands[0] == 'runfun':
            return self.memory.defs[commands[1]].run_children(file)
        elif commands[0] == 'convert':
            if commands[1] == 'int':
                self.memory.variables[commands[2]].type = 'int'
                self.memory.variables[commands[2]].value = int(self.memory.variables[commands[2]].value)
        elif commands[0] == 'type':
            print(self.memory.variables[commands[1]].type)
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
        else:
            return self.run_children(file)
        return True
                
    def run_children(self, file) -> bool:
        for child in self.children:
            result = child.run(file)
            if result == False:
                return False
            if result == 'break':
                return 'break'
        return True
                
def remove_space(string):
    if string and string[0] == ' ':
        string = string[1:]
        return remove_space(string)
    else:
        return string
                
class Parser(object):
    def __init__(self, code: str, memory: Memory):
        self.code: str = code
        self.memory: Memory = memory
        
    def parse(self, i=-1) -> list[Node]:
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
                node = Node(command, index=i, memory=self.memory)
                result = self.parse(i)
                node.children = result[0].children
                main_node.children.append(node)
                con = True
                con_to = result[1]
            elif command.split(' ')[0] == 'endblock':
                #print(2)
                return [main_node, i]
            else:
                main_node.children.append(Node(command, index=i, memory=self.memory))
                
        return [main_node, i]
    
class Lexer(object):
    def __init__(self, code: str):
        self.code: str = code
        
    def parse(self) -> None:
        self.code = self.code.replace('\n', '')
        self.code = self.code.replace('    ', '').replace('   ', '').replace('  ', '')
        self.code = self.code.replace(' {', ';').replace('{', ';').replace('}', 'endblock;')
        self.code = self.code.replace(' == ', '==').replace(' != ', '!=').replace(' > ', '>').replace(' < ', '<')
        
class Main(object):
    def __init__(self, code: str):
        self.code: str = code
        self.lexer = Lexer(self.code)
        
    def run(self, file) -> None:
        self.memory = Memory()
        self.lexer.parse()
        self.code = self.lexer.code
        self.parser = Parser(self.code, self.memory)
        self.node = self.parser.parse()[0]
        self.node.run(file)
    
    

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
        if result==False:
            Error.Programm.stop()
        else:
            print(f'Program: Completed in {time.time()-tm} seconds')
            
# c = Compiler()
# c.run_file('examples/fun.aln')