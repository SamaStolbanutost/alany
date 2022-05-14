from .main import Main

class Interpreter():
    def __init__(self):
        pass

    def get_node(self):
        main = Main('')
        main.setting()
        node = main.node
        return node

    def run(self) -> None:
        file = '/'
        memory = self.get_node().memory
        
        while True:
            code = input('>>> ')
            main = Main(code)
            main.run(file, memory=memory, is_interpreter=True)
            memory = main.node.memory