from .result import Result
from .parser import Lexer, Parser
from .memory import Memory

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