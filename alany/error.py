class Error:
    class Runtime:
        def not_a_number(value_1: any, value_2: any = None,
                         fun: str = '') -> None:
            if value_1 is not None:
                print(f'RuntimeError: Not a number {value_1} {fun} {value_2}')
            else:
                print(f'RuntimeError: Not a number {fun}({value_1})')

        def not_existing_variable(name: str):
            print(f'RuntimeError: Not existing variable {name}')

        def unknow_type(value: any) -> None:
            print(f'RuntimeError: Unknow type {value}')

    class Programm:
        def stop() -> None:
            print('Program: Stopped with error')
