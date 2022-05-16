import time
from .error import Error
from .main import Main


class Compiler():
    def __init__(self):
        pass

    def run_file(self, file: str) -> None:
        with open(file, 'r') as fl:
            self.run(fl.read(), file=file)

    def run(self, code: str, file: str = '/') -> None:
        tm = time.time()
        main = Main(code)
        result = main.run(file)
        if result.is_success():
            print(f'Program: Completed in {time.time()-tm} seconds')
        else:
            Error.Programm.stop()
