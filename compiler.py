OP_END = 0
OP_INC_DP = 1
OP_DEC_DP = 2
OP_INC_VAL = 3
OP_DEC_VAL = 4
OP_WRITE = 5
OP_READ = 6
OP_JMP_FWD = 7
OP_JMP_BCK = 8

PROGRAM_SIZE = 2048
DATA_SIZE = 65536
STACK_SIZE = 1024

SUCCESS = 0
FAILURE = 1

class Instruction:
    def __init__(self):
        self.operator = None
        self.operand = None


def compile_bf(f, stack, program, pc=0):
    while True:
        c = f.read(1)
        if not c:
            break
        if c == '>':
            program[pc].operator = OP_INC_DP
        elif c == '<':
            program[pc].operator = OP_DEC_DP
        elif c == '+':
            program[pc].operator = OP_INC_VAL
        elif c == '-':
            program[pc].operator = OP_DEC_VAL
        elif c == '.':
            program[pc].operator = OP_WRITE
        elif c == ',':
            program[pc].operator = OP_READ
        elif c == '[':
            program[pc].operator = OP_JMP_FWD
            if len(stack) > STACK_SIZE:
                return FAILURE
            stack.append(pc)
        elif c == ']':
            if len(stack) == 0:
                return FAILURE
            jmp_pc = stack.pop()
            program[pc].operator = OP_JMP_BCK
            program[pc].operand = jmp_pc
            program[jmp_pc].operand = pc

        else:
            pc -= 1
        pc += 1

    if len(stack) != 0 or pc == PROGRAM_SIZE:
            return FAILURE
    program[pc].operator = OP_END
    return SUCCESS


def run_bf(stack, program, pc=0):
    data = [0 for _ in range(DATA_SIZE)]
    ptr = 0
    output_string = ''
    while program[pc].operator != OP_END and ptr < DATA_SIZE:
        if program[pc].operator == OP_INC_DP:
            ptr += 1
        elif program[pc].operator == OP_DEC_DP:
            ptr -= 1
        elif program[pc].operator == OP_INC_VAL:
            data[ptr] += 1
        elif program[pc].operator == OP_DEC_VAL:
            data[ptr] -= 1
        elif program[pc].operator == OP_WRITE:
            output_string += chr(data[ptr])
        elif program[pc].operator == OP_READ:
            data[ptr] == ord(input()[0:1])
        elif program[pc].operator == OP_JMP_FWD:
            if data[ptr] == 0:
                pc = program[pc].operand
        elif program[pc].operator == OP_JMP_BCK:
            if data[ptr] != 0:
                pc = program[pc].operand
        else:
            return FAILURE
        pc += 1

    if ptr < DATA_SIZE:
        print (output_string)
        return SUCCESS
    return FAILURE


if __name__ == '__main__':
    print("Enter file name(full path of file) to compile: ")
    file_name = input()
    f = open(file_name, 'r')
    stack = list()
    program = [Instruction() for _ in range(PROGRAM_SIZE)]
    if compile_bf(f, stack, program) == SUCCESS:
        if run_bf(stack, program) == SUCCESS:
            pass
        else:
            print ('Error in program execution')
    else:
        print ('Error in program compilation')

