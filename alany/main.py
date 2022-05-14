from .result import Result
from .parser import Lexer, Parser
from .memory import Memory

class Main(object):
    def __init__(self, code: str):
        self.code: str = code
        self.lexer = Lexer(self.code)
        
    def setting(self, memory: Memory=None, is_interpreter: bool=False):
        if memory is None:
            self.memory = Memory()
        else:
            self.memory = memory
        self.lexer.parse()
        self.code = self.lexer.code
        self.parser = Parser(self.code, self.memory, is_interpreter)
        self.node = self.parser.parse()[0]
        
    def run(self, file: str, memory: Memory=None, is_interpreter: bool=False) -> Result:
        self.setting(memory, is_interpreter)
        return self.node.run_children(file)