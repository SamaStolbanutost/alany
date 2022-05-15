from .main import Main

def lines_input(text):
    contents = []
    while True:
        try:
            line = input(text)
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)

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
            code = lines_input('>>> ')
            main = Main(code)
            main.run(file, memory=memory, is_interpreter=True)
            memory = main.node.memory