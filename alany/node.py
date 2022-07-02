from typing import List
import math
import random
import os
from .memory import Memory, Data
from .error import Error
from .result import Result
from .functions import remove_all_space, is_string, remove_s, to_s, \
                       remove_start_spaces, parse_args, add_str


class Node(object):
    def __init__(self, command: str = '', children=None, index: int = 0,
                 memory: Memory = None, is_interpreter: bool = False):
        self.command = command.replace('  ', ' ')
        if children is not None:
            self.children: List[Node] = children
        else:
            self.children: List[Node] = []
        self.index = index
        self.memory = memory
        self.is_interpreter = is_interpreter

    def get_args(self):
        args = remove_all_space(self.command)
        args = args.split('(')[1]
        args = args.split(')')[0].split(',')
        return parse_args(args)

    def get_value(self, variable: str, file: str = '') -> any:
        return self.memory.get_value(variable, file)

    def set_value(self, variable: str, value: any, g=True) -> None:
        if isinstance(value, Data):
            value = value.value
        if self.memory.in_memory(variable):
            var = self.memory.get_var(variable)
            if var is not None:
                var.value = value
            else:
                self.memory.add_var(var_name=variable, value=value)
        elif variable[-1] == ']':
            var = self.memory.get_var(variable.split('[')[0])
            index = self.get_value(variable.split('[')[1][:-1])
            var.set_list_value(value=value, index=index)
        else:
            if not g:
                self.memory.add_var(value, variable)
            else:
                self.memory.add_global_var(value, variable)

    def get_bool_value(self, expression: str) -> bool:
        return self.memory.get_bool_value(expression)

    def run(self, file: str) -> Result:
        commands = self.command.split(' ')
        commands_w = self.command.replace('=', '').replace('  ', ' ')
        commands_w = commands_w.split(' ')
        commands_c = self.command.replace('(', '').replace(')', '').split(' ')

        if commands[0] == 'print':
            values = commands[1:]

            for i, value in enumerate(values):
                val = str(self.get_value(value))
                if is_string(val):
                    val = val[1:-1]
                values[i] = val

            tp = ' '.join(values)
            print(tp, end='')
        elif commands[0] == 'putchar':
            char = chr(int(float(self.get_value(' '.join(commands[1:])))))
            print(char, end='')
        elif commands[0] == 'var':
            if commands[1] == 'local':
                var_name = commands[2].split('=')[0]
                value = self.get_value(' '.join(commands[3:]))
                self.set_value(var_name, value, g=False)
            else:
                var_name = commands[1].split('=')[0]
                val = '='.join(self.command.split('=')[1:])
                val = remove_start_spaces(val)
                value = self.get_value(val)
                self.set_value(var_name, value, file)
        elif commands_w[0] == 'len':
            var_name = commands_w[1]
            ln = len(self.memory.get_var(commands_w[2]).value)
            self.set_value(var_name, ln)
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
            a = remove_s(self.get_value(commands[2]))
            b = remove_s(self.get_value(commands[3]))
            val = a + b

            if isinstance(val, str):
                val = to_s(val)

            self.set_value(commands[1], val)
        elif commands[0] == 'sub':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            is_a_int = isinstance(a, int) or isinstance(a, float)
            is_b_int = isinstance(b, int) or isinstance(b, float)
            if not (is_a_int and is_b_int):
                Error.Runtime.not_a_number(a, b, fun='-')
                return Result(status=0)
            self.set_value(commands[1], a-b)
        elif commands[0] == 'div':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            is_a_int = isinstance(a, int) or isinstance(a, float)
            is_b_int = isinstance(b, int) or isinstance(b, float)
            if not (is_a_int and is_b_int):
                Error.Runtime.not_a_number(a, b, fun='/')
                return Result(status=0)
            self.set_value(commands[1], a/b)
        elif commands[0] == 'rdiv':
            a = self.get_value(commands[2])
            b = self.get_value(commands[3])
            is_a_int = isinstance(a, int) or isinstance(a, float)
            is_b_int = isinstance(b, int) or isinstance(b, float)
            if not (is_a_int and is_b_int):
                Error.Runtime.not_a_number(a, b, fun='%')
                return Result(status=0)
            self.set_value(commands[1], a % b)
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
            is_a_int = isinstance(a, int) or isinstance(a, float)
            is_b_int = isinstance(b, int) or isinstance(b, float)
            if not (is_a_int and is_b_int):
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
        elif commands_c[0] == 'class':
            var_name = commands[1].split('(')[0]

            self.memory.block = True
            self.run_children(file)

            value = self.memory.variables
            value = {'vars': value, 'node': self}
            self.memory.block = False

            self.memory.add_global_var(value=value, var_name=var_name)
        elif commands[0] == 'append':
            value = self.get_value(commands[2])
            self.memory.get_var(commands[1])._value.append(value)
        elif commands[0] == 'convert':
            if commands[1] == 'int':
                value = self.memory.get_var(commands[2]).value
                if is_string(value):
                    value = value[1:-1]
                self.memory.get_var(commands[2]).type = 'int'
                self.memory.get_var(commands[2]).value = int(value)
            elif commands[1] == 'float':
                value = self.memory.get_var(commands[2]).value
                if is_string(value):
                    value = value[1:-1]
                self.memory.get_var(commands[2]).type = 'float'
                self.memory.get_var(commands[2]).value = float(value)
            elif commands[1] == 'str':
                value = self.memory.get_var(commands[2]).value
                self.memory.get_var(commands[2]).type = 'str'
                self.memory.get_var(commands[2]).value = str(value)
        elif commands[0] == 'type':
            type = self.memory.get_var(commands[1]).type
            self.memory.add_var(add_str(type), commands[2])
        elif commands[0] == 'import':
            from .parser import Lexer, Parser
            path = commands[1]
            if path[0] == '~':
                path = path[1:]
                paths = os.getenv('ALANY_PATH').split(':')

                for p in paths:
                    if os.path.exists(p + '/' + path + '.aln'):
                        path = p + '/' + path + '.aln'
                        break
                    elif os.path.exists(p + '/' + path + '/' + '__main__.aln'):
                        path = p + '/' + path + '/' + '__main__.aln'
                        break
            elif not path[0] == '/':
                path = '/'.join(file.split('/')[:-1]) + '/' + path + '.aln'
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
        elif commands[0] == 'file':
            if commands[1] == 'read':
                path = self.get_value(commands[2])[1:-1]
                var = commands[3]

                with open(path, 'r') as file:
                    text = "'" + file.read() + "'"

                self.memory.add_var(var_name=var, value=text)
            elif commands[1] == 'write':
                path = self.get_value(commands[2])[1:-1]
                value = self.get_value(commands[3])[1:-1]

                with open(path, 'w') as file:
                    file.write(value)
        elif commands[0] == 'random':
            self.memory.add_var(var_name=commands[1], value=random.random())
        elif commands[0] == 'pygame':
            import pygame

            if commands[1] == 'init':
                pygame.init()
                mem = self.memory.get_global_memory()
                if '__alany__' not in mem.variables:
                    mem.variables['__alany__'] = {}
                mem.variables['__alany__']['__pygame__'] = {}
            elif commands[1] == 'quit':
                pygame.quit()
            elif commands[1] == 'display':
                if commands[2] == 'init':
                    pygame.display.init()
                elif commands[2] == 'set_mode':
                    a = self.get_value(commands[3])
                    b = self.get_value(commands[4])
                    mem = self.memory.get_global_memory()
                    mem.variables['__alany__']['__pygame__']['display'] = \
                        pygame.display.set_mode((a, b))
                elif commands[2] == 'set_caption':
                    val = self.get_value(' '.join(commands[3:]))[1:-1]
                    pygame.display.set_caption(val)
                    pygame.event.pump()
                elif commands[2] == 'update':
                    pygame.display.update()
            elif commands[1] == 'draw':
                if commands[2] == 'rect':
                    r = self.get_value(commands[3])
                    g = self.get_value(commands[4])
                    b = self.get_value(commands[5])
                    x = self.get_value(commands[6])
                    y = self.get_value(commands[7])
                    width = self.get_value(commands[8])
                    height = self.get_value(commands[9])
                    mem = self.memory.get_global_memory()
                    pygame.draw.rect(mem.variables['__alany__']['__pygame__']
                                     ['display'], pygame.Color(r, g, b),
                                     pygame.Rect(x, y, width, height))
            elif commands[1] == 'event':
                if commands[2] == 'get':
                    mem = self.memory.get_global_memory()
                    mem.variables['__alany__']['__pygame__']['events'] \
                        = pygame.event.get()
                    ln = str(len(mem.variables['__alany__']['__pygame__']
                                 ['events']))
                    self.set_value(commands[3], ln)
                elif commands[2] == 'poll':
                    mem = self.memory.get_global_memory()
                    events = mem.variables['__alany__']['__pygame__']['events']
                    event = events[0]
                    mem.variables['__alany__']['__pygame__']['events'].pop(0)

                    self.set_value(commands[3], str(event.type))
                    type = event.type
                    if type == pygame.KEYDOWN or type == pygame.KEYUP:
                        self.set_value(commands[4], str(event.key))
                    else:
                        self.set_value(commands[4], -1)
        elif len(commands[0].split('(')) > 0 and \
                self.memory.in_memory(commands[0].split('(')[0]):

            var = self.memory.get_var(commands[0].split('(')[0])
            if var.type == 'node':
                node: Node = var.value
                args_names = node.get_args()
                args = ''.join(''.join(commands[0:]).split('(')[1:])
                args = args.split(')')[0].split(',')
                args = parse_args(args)
                for i in range(len(args)):
                    node.memory.add_var(value=self.get_value(args[i]),
                                        var_name=args_names[i])
                node.run_children(file)
            else:
                value = self.get_value(' '.join(commands[1:]))
                self.set_value(commands[0], value)
        elif self.is_interpreter is True:
            values = []
            for i in commands:
                if not i == '':
                    values.append(i)
            for i, value in enumerate(values):
                val = str(self.get_value(value))
                if is_string(val):
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
