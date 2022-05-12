from queue import LifoQueue
from typing import List, Dict, Any

def run(index: int, code: List[str], stack: LifoQueue, memory: Dict[str, Any], fun: bool, funs: Dict[str, int]):
    commands = code[index].split(' ')
    command = commands[0]
    
    if fun == 0 or fun == 2:
        if command == 'add':
            stack.put(' '.join(commands[1:])) # add value to stack
        elif command == 'sum':
            a = int(stack.get())
            b = int(stack.get())
            stack.put(a + b)
        elif command == 'dif':
            a = int(stack.get())
            b = int(stack.get())
            stack.put(a - b)
        elif command == 'div':
            a = int(stack.get())
            b = int(stack.get())
            stack.put(a / b)
        elif command == 'mul':
            a = int(stack.get())
            b = int(stack.get())
            stack.put(a * b)
        elif command == 'stack':
            if commands[1] == 'mul': # stack multiple
                a = stack.get()
                stack.put(a)
                stack.put(a)
            elif commands[1] == 'rev': # stack reverse
                stc = []
                for i in range(len(stack.queue)):
                    stc.append(stack.get())
                for i in stc:
                    stack.put(i)
            elif commands[1] == 'clr': # clear stack
                stack = LifoQueue()
            elif commands[1] == 'trv': # revers top values
                a = stack.get()
                b = stack.get()
                stack.put(a)
                stack.put(b)
        elif command == 'out':
            print(stack.get(), end='') # print
        elif command == 'putchar':
            print(chr(int(stack.get())), end='') # print character from ASCII
        elif command == 'in':
            stack.put(input()) # put character in stack
        elif command == 'memory':
            if commands[1] == 'save': # save
                memory[commands[2]] = stack.get() # save value to memory
            elif commands[1] == 'load': # load
                if commands[2] in memory: # if the variable is in memory
                    stack.put(memory[commands[2]])
        elif command == 'jump':
            index = int(commands[1])-2 # -2 because of the index is incremented after the command is run
        elif command == 'equal':
            if str(stack.get()) == str(stack.get()):
                index = int(commands[1])-2 # -2 because of the index is incremented after the command is run
        elif command == 'less':
            if int(stack.get()) < int(stack.get()):
                index = int(commands[1])-2 # -2 because of the index is incremented after the command is run
        elif command == 'larger':
            if int(stack.get()) > int(stack.get()):
                index = int(commands[1])-2 # -2 because of the index is incremented after the command is run
        elif command == 'endfun':
            fun = 0 # end of function
        elif command == 'run':
            index = funs[commands[1]] # jump to the function
            fun = 2 # run function
        elif command == 'fun':
            funs[commands[1]] = index # save the index of the function
            fun = 1 # start of function
    elif command == 'endfun':
        fun = 0 # end of function
    
    return stack, memory, index, fun, funs

def run_code(code: str):
    code = code.replace('\n', '').replace('\\n', '\n').split(';')
    stack = LifoQueue()
    memory = {}
    
    index = 0
    main_index = 0
    fun = 0
    st = fun
    funs = {}
    while index < len(code):
        if fun == 0:
            main_index = index # save the index of the main function
        stack, memory, index, fun, funs = run(index, code, stack, memory, fun, funs)
        index += 1
        if st == 2 and fun == 0:
            index = main_index+1 # jump to the main function
        st = fun
    
def run_file(path):
    with open(path, 'r') as f:
        code = f.read()
    run_code(code)