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
        tm = time.perf_counter()
        main = Main(code)
        result = main.run(file)
        if result.is_success():
            print(f'\nProgram: Completed in {time.perf_counter()-tm} seconds')
        else:
            Error.Programm.stop()
