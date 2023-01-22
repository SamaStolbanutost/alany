code = [
    0x08, 0x00, 0x05, #SET 0x00 = 0x05
    0x08, 0x01, 0x02, #SET 0x01 = 0x02
    0x08, 0x02, 0x00, #SET 0x02 = 0x00
    0x08, 0x03, 0x01, #SET 0x03 = 0x01
    0x03, 0x03, 0x01, 0x15, #JG 0x03 > 0x01 THEN 0x19
    0x01, 0x02, 0x00, #ADD 0x02 0x00
    0x02, 0x01, 0x03, #SUB 0x01 0x03
    0x07, 0x0B, #JMP 0x08
    0x00
]
memory = [0x00] * 0xff

i = 0
while True:
    command = code[i]
    print(memory, command, i)
    if command == 0x01:
        memory[code[i + 1]] += memory[code[i + 2]]
        i = i + 2
    if command == 0x02:
        memory[code[i + 1]] -= memory[code[i + 2]]
        i = i + 2
    if command == 0x03:
        if memory[code[i + 1]] > memory[code[i + 2]]:
            i = code[i + 3] - 1
        i = i + 3
    if command == 0x04:
        if memory[code[i + 1]] >= memory[code[i + 2]]:
            i = code[i + 3] - 1
        i = i + 3
    if command == 0x05:
        if memory[code[i + 1]] == memory[code[i + 2]]:
            i = code[i + 3] - 1
        i = i + 3
    if command == 0x06:
        if memory[code[i + 1]] != memory[code[i + 2]]:
            i = code[i + 3] - 1
        i = i + 3
    if command == 0x07:
        print(code[i + 1])
        i = code[i + 1] - 1
        i += 1
    if command == 0x08:
        memory[code[i + 1]] = code[i + 2]
        i = i + 2
    if command == 0x09:
        memory[code[i + 1]] = memory[code[i + 2]]
        i = i + 2
    input()
    i += 1
    if i >= len(code):
        break
        
print(memory)