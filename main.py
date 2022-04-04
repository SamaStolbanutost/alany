import math

class Error:
    class Runtime:
        def not_a_number(value_1: any, value_2: any=None, fun: str=''):
            if value_1 is not None:
                print(f'RuntimeError: Not a number {value_1}{fun}{value_2}')
            else:
                print(f'RuntimeError: Not a number {fun}({value_1})')
    
    class Programm:
        def stop():
            print('Programm: Stopped with error')

class Node():
    def __init__(self, command: str='', children=None, index: int=0, ):
        self.command = command.replace('  ', ' ')
        if children is not None:
            self.children = children
        else:
            self.children = []
        self.index = index
    
    def get_value(self, variable: str):
        #print(memory)
        if variable in memory:
            return memory[variable]
        elif variable.split('[')[0] in memory:
            return memory[variable.split('[')[0]][math.floor(float(self.get_value(variable.split('[')[1][:-1])))]
        elif variable == 'input':
            return input()
        elif variable == 'space':
            return ' '
        elif variable == 'none':
            return ''
        else:
            return variable
        
    def set_value(self, variable: str, value: any):
        if variable in memory:
            memory[variable] = value
        elif variable[-1] == ']':
            # print(len(memory[variable.split('[')[0]]))
            # print(float(self.get_value(variable.split('[')[1][:-1])))
            memory[variable.split('[')[0]][math.floor(float(self.get_value(variable.split('[')[1][:-1])))] = value
        else:
            memory[variable] = value
        
    def get_bool_value(self, expression: str):
        if '==' in expression:
            expression = expression.replace('==', ' ').split(' ')
            try:
                return float(self.get_value(expression[0])) == float(self.get_value(expression[1]))
            except:
                return self.get_value(expression[0]) == self.get_value(expression[1])
        elif '!=' in expression:
            expression = expression.replace('!=', ' ').split(' ')
            try:
                return not float(self.get_value(expression[0])) == float(self.get_value(expression[1]))
            except:
                return not self.get_value(expression[0]) == self.get_value(expression[1])
        elif '>' in expression:
            expression = expression.replace('>', ' ').split(' ')
            return float(self.get_value(expression[0])) > float(self.get_value(expression[1]))
        elif '<' in expression:
            expression = expression.replace('<', ' ').split(' ')
            return float(self.get_value(expression[0])) < float(self.get_value(expression[1]))
    
    def run(self):
        commands = self.command.split(' ')
        commands_w = self.command.replace('=', '').replace('  ', ' ').split(' ')
        commands_c = self.command.replace('(', '').replace(')', '').split(' ')
        if commands[0] == 'print':
            print(self.get_value(' '.join(commands[1:])), end='')
        if commands[0] == 'putchar':
            print(chr(int(float(self.get_value(' '.join(commands[1:]))))), end='')
        elif commands_w[0] == 'var':
            self.set_value(commands_w[1], self.get_value(' '.join(commands_w[2:])))
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
            try:
                a = float(a)
                b = float(b)
                self.set_value(commands[1], a+b)
            except ValueError:
                Error.Runtime.not_a_number(a, b, fun='+')
                return False
        elif commands[0] == 'sub':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            try:
                a = float(a)
                b = float(b)
                self.set_value(commands[1], a-b)
            except ValueError:
                Error.Runtime.not_a_number(a, b, fun='-')
                return False
        elif commands[0] == 'div':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            try:
                a = float(a)
                b = float(b)
                self.set_value(commands[1], a/b)
            except ValueError:
                Error.Runtime.not_a_number(a, b, fun='/')
                return False
        elif commands[0] == 'rdiv':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            try:
                a = float(a)
                b = float(b)
                self.set_value(commands[1], a%b)
            except ValueError:
                Error.Runtime.not_a_number(a, b, fun='%')
                return False
        elif commands[0] == 'sin':
            a = self.get_value(commands[2])
            try:
                a = float(a)
                self.set_value(commands[1], math.sin(a))
            except ValueError:
                Error.Runtime.not_a_number(a, fun='sin')
                return False
        elif commands[0] == 'cos':
            a = self.get_value(commands[2])
            try:
                a = float(a)
                self.set_value(commands[1], math.cos(a))
            except ValueError:
                Error.Runtime.not_a_number(a, fun='cos')
                return False
        elif commands[0] == 'run':
            self.set_value(commands[1], eval(''.join(commands[2:])))
        elif commands[0] == 'break':
            return False
        elif commands[0] == 'mul':
            try:
                a = float(self.get_value(commands[2]))
                b = float(self.get_value(commands[3]))
                self.set_value(commands[1], a*b)
            except ValueError:
                Error.Runtime.not_a_number(a, b, '*')
                return False
        elif commands_c[0] == 'if':
            #print(1)
            #print(self.get_value(commands[1]))
            #print(self.get_value(commands[2]))
            if self.get_bool_value(commands_c[1]):
                return self.run_children()
        elif commands_c[0] == 'repeat':
            for i in range(int(self.get_value(commands_c[1]))):
                result = self.run_children()
                if not result:
                    return False
        elif commands_c[0] == 'while':
            while self.get_bool_value(commands_c[1]):
                result = self.run_children()
                if result == 'break':
                    break
                elif not result:
                    return False
        elif commands[0] == 'append':
            memory[commands[1]].append(self.get_value(commands[2]))
        else:
            return self.run_children()
        return True
                
    def run_children(self):
        for child in self.children:
            result = child.run()
            if not result:
                return False
        return True
                
def remove_space(string):
    if string and string[0] == ' ':
        string = string[1:]
        return remove_space(string)
    else:
        return string
                
class Parser():
    def __init__(self, code: str):
        self.code: str = code
        
    def parse(self, i=-1) -> list[Node, int]:
        main_node = Node()
        code = self.code.split(';')
        
        con_to = i
        con = True
        for i, command in enumerate(code):
            if con and i <= con_to:
                continue
            if con and i > con_to:
                con = False
            command = remove_space(command)
            if command.split(' ')[0] in ['if', 'repeat', 'while']:
                #print(1)
                node = Node(command, index=i)
                result = self.parse(i)
                node.children = result[0].children
                main_node.children.append(node)
                con = True
                con_to = result[1]
            elif command.split(' ')[0] == 'endblock':
                #print(2)
                return [main_node, i]
            else:
                main_node.children.append(Node(command, index=i))
                
        return [main_node, i]
    
class Lexer():
    def __init__(self, code: str):
        self.code: str = code
        
    def parse(self):
        self.code = self.code.replace('\n', '')
        self.code = self.code.replace('    ', '').replace('   ', '').replace('  ', '')
        self.code = self.code.replace(' {', ';').replace('{', ';').replace('}', 'endblock;')
        self.code = self.code.replace(' == ', '==').replace(' != ', '!=').replace(' > ', '>').replace(' < ', '<')
        self.code = self.code.replace('\\x1b', '\x1b')
        self.code = self.code.replace('\\n', '\n')
        
class Main():
    def __init__(self, code: str):
        self.code: str = code
        self.lexer = Lexer(self.code)
        
    def run(self):
        self.lexer.parse()
        self.code = self.lexer.code
        self.parser = Parser(self.code)
        self.node = self.parser.parse()[0]
        self.node.run()
    
    

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
def run_file(file):
    with open(file, 'r') as file:
        run(file.read())

def run(code):
    global memory
    memory = {}
    main = Main(code)
    result = main.run()
    if not result:
        Error.Programm.stop()