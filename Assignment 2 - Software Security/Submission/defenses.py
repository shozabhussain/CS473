## Intruction Guides ##
# func x-> defines a function with name 'x' e.g func main defines 'main'
# call x-> calls the function with name 'x' e.g call main calls 'main'
# puts x-> prints the word 'x' (I have handled 'good' as a special case for clarity)
# exit -> stops the execution of the program
# aloc x -> alocates x spaces on the stack
# gets -> gets user input
# movb x y -> moves a space or 'byte' from x to y (* means derefernce to memory similar to '()' in x86)
# dloc x -> Deallocates x spaces (opposite of aloc)
# retb -> return instruction
# pwnd -> Instruction that 'hacks' the system one you would need to inject

## Sample Run to pawn
# python3 defenses.py
# >pwnd000011112222333362

## What You Need To Do
# Carefully Read Instructions in the 3 Functions Provided
# Raise the Exceptions in StackGuard when you detect stack smashing or buffer overflow
# Raise the Exceptions in NoExecStack when you detect attacker is trying to run code from the stack section
# Randomize The Program Memory Layout (Not Just Stack Layout)

import random
##
class RunProgramSimulator:
    start_address = None
    mem_size = None
    execstack = None
    stack_start = None
    memory = None
    f_addr = {}


    code = [
        'func main',
        'call vuln',
        'puts good',
        'exit',
        'func vuln',
        'aloc 5',
        'gets',
        'movb rax *esp',
        'dloc 5',
        'retb'
    ]
    jumpTable = {}
    registers = {
        'esp': 0,
        'rip': 0,
        'rax': 0
    }

    def __init__(self):
        self.start_address = 0
        self.execstack = False
        self.mem_size = 100 #Total Memory
        self.memory = [0 for _ in range(self.mem_size)] #Initialize Memory
        code_length = self.loadCode(self.code)
        print(code_length)
        print(self.memory)
        print(self.jumpTable)
        self.registers['esp'] = code_length + 50
        self.stack_start = code_length + 10

    def loadCode(self, code):
        n = random.randint(0,9)
        codeArray = []
        for line in code:
            line_split = line.split()
            codeArray.extend(line_split)
            if line_split[0] == 'func':
                self.jumpTable[line_split[1]] = len(codeArray)+n
        self.memory[n:len(codeArray)] = codeArray
        return len(codeArray)
    #Proactive
    def kernel_va_space_randomize(self):
        # Keep Max Offset less than 10. This essentially means program can have 10 different address. This should be random
        # You can only modify the loadCode function for this task. Don't modify any other line for this task
        pass
    #Reactive
    def stack_protector(self):
        # You can only modify inputBuffer function for this. Remember to not reduce the size of the buffer. You can call other functions but not modify them
        # Have a max of 1 'byte' canary. 1 byte in this magical world of narniac assembly means 1 space of array. Raise the exception given if you detect anything.
        raise Exception('Stack Smashing Detected')
    #Reactive
    def noexecstack(self):
        # You can only modify run 'The Place' for this task. You just need to add **one** line of code there. Rest can be added here
        if self.registers['rip'] >= self.stack_start and self.registers['rip'] <= self.mem_size:
            raise Exception('Non Executable Stack')

    def stack_alloc(self, size):
        if (self.registers['esp'] - size) < self.stack_start:
            raise Exception("No Have Memory")
        else:
            self.registers['esp'] -= size
    def stack_dealloc(self, size):
        if (self.registers['esp'] + size) > len(self.memory):
            raise Exception("Too Much Memory")
        else:
            self.registers['esp'] += size
    def callFunction(self, fname):
        self.stack_alloc(1)
        self.memory[self.registers['esp']] = self.registers['rip'] + 2
        self.registers['rip'] = int(self.jumpTable[fname])
    def retFunction(self):
        self.registers['rip'] = int(self.memory[self.registers['esp']])
        print(self.memory)
        print(self.registers['rip'])
        self.stack_dealloc(1)
    def inputBuffer(self, buffer):
        j = 0
        lenOfBuffer = int(self.memory[self.registers['rip']-1])
        canaryPosition = self.registers['esp'] + lenOfBuffer - 1
        canary = 'cnry'
        self.memory[canaryPosition] = canary
        self.stack_alloc(1)
        for i in range(0, len(buffer), 4):
            self.memory[self.registers['esp'] + j] = buffer[i:i+4]
            j += 1
        self.stack_dealloc(1)
        if self.memory[canaryPosition] != canary:
            self.stack_protector()

    def getValue(self, exp):
        if exp[0] == '*':
            exp = exp[1:]
            return self.memory[self.registers[exp]]
        else:
            return self.registers[exp]
    def storeValue(self, exp, val):
        if exp[0] == '*':
            exp = exp[1:]
            self.memory[self.registers[exp]] = val
        else:
            self.registers[exp] = val
    def start(self):
        self.registers['rip'] = self.jumpTable['main']
        ins = ''
        while ins != 'exit':
            # The Place
            self.noexecstack()
            ins = self.memory[self.registers['rip']]
            print('Instruction>',self.registers['rip'])
            print('Instruction>',ins)
            if ins == 'call':
                self.callFunction(self.memory[self.registers['rip'] + 1])
            elif ins == 'aloc':
                value = int(self.memory[self.registers['rip'] + 1])
                self.stack_alloc(value)
                self.registers['rip'] += 2
            elif ins == 'dloc':
                value = int(self.memory[self.registers['rip'] + 1])
                self.stack_dealloc(value)
                self.registers['rip'] += 2
            elif ins == 'gets':
                input_str = input('>')
                self.inputBuffer(input_str)
                self.registers['rip'] += 1
            elif ins == 'retb':
                self.retFunction()
            elif ins == 'puts':
                value = self.memory[self.registers['rip'] + 1]
                if (value == 'good'):
                    print('Everything Seems Good')
                else:
                    print(value)
                self.registers['rip'] += 2
            elif ins == 'movb':
                src = self.memory[self.registers['rip'] + 2]
                dst = self.memory[self.registers['rip'] + 1]
                value = self.getValue(src)
                self.storeValue(dst, value)
                self.registers['rip'] += 3
            elif ins == 'exit':
                return
            elif ins == 'pwnd':
                print('Pawned!!')
                exit(1)
            else:
                raise ValueError(f'Invalid Instruction {ins}')

if __name__ == "__main__":
    p = RunProgramSimulator()
    p.start()