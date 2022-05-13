from typing import List
from .node import Node
from .memory import Memory

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
    
def remove_space(string: str):
    if string and string[0] == ' ':
        string = string[1:]
        return remove_space(string)
    else:
        return string