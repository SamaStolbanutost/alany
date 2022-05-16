from typing import List
from .node import Node
from .memory import Memory
from .functions import remove_space


class Parser(object):
    def __init__(self, code: str, memory: Memory,
                 is_interpreter: bool = False):
        self.code: str = code
        self.memory: Memory = memory
        self.is_interpreter: bool = is_interpreter

    def parse(self, i=-1) -> List[Node]:
        memory = self.memory
        is_interpreter = self.is_interpreter
        main_node = Node(memory=memory, is_interpreter=is_interpreter)
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
                self.memory = Memory(parent=self.memory)
                node = Node(command, index=i, memory=self.memory,
                            is_interpreter=self.is_interpreter)
                result = self.parse(i)
                node.children = result[0].children
                main_node.children.append(node)
                con = True
                con_to = result[1]
            elif command.split(' ')[0] == 'endblock':
                self.memory = self.memory.parent
                return [main_node, i]
            else:
                main_node.children.append(Node(command, index=i,
                                               memory=self.memory,
                                               is_interpreter=is_interpreter))

        return [main_node, i]


class Lexer(object):
    def __init__(self, code: str):
        self.code: str = code

    def parse(self) -> str:
        self.code = self.code.replace('\n', '')
        self.code = self.code.replace('    ', '').replace('   ', '')
        self.code = self.code.replace('  ', '')
        self.code = self.code.replace(' {', ';').replace('{', ';')
        self.code = self.code.replace('}', 'endblock;')
        self.code = self.code.replace(' == ', '==').replace(' != ', '!=')
        self.code = self.code.replace(' > ', '>').replace(' < ', '<')
        return self.code
