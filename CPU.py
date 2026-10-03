def AND(input0, input1):
    if input0 == 1 and input1 == 1:
        return 1
    else:
        return 0

def OR(input0, input1):
    if input0 == 0 and input1 == 0:
        return 0
    else:
        return 1

def NOT(input0):
    if input0 == 0:
        return 1
    else:
        return 0

def XOR(input0, input1):
    if input0 != input1:
        return 1
    else:
        return 0

def NAND(input0, input1):
    return NOT(AND(input0, input1))

def NOR(input0, input1):
    return NOT(OR(input0, input1))

def half_adder(a, b):
    SUM = XOR(a, b)
    CARRY = AND(a,b)
    return SUM, CARRY

def full_adder(a, b, carry_in):
    sum1, carry1 = half_adder(a, b)

    sum, carry2 = half_adder(sum1, carry_in)

    carry_out = OR(carry1, carry2)

    return sum, carry_out

def four_bit_adder(a, b):
    sum = [0,0,0,0,0]
    sum[3], carry = full_adder(a[3], b[3], 0)
    sum[2], carry = full_adder(a[2], b[2], carry)
    sum[1], carry = full_adder(a[1], b[1], carry)
    sum[0], carry = full_adder(a[0], b[0], carry)
    return sum

def mux(a, b, select):
    return OR(AND(a, NOT(select)), AND(b, select))

def four_bit_mux(a, b, select):
    result = [0,0,0,0]
    result[0] = mux(a[0], b[0], select)
    result[1] = mux(a[1], b[1], select)
    result[2] = mux(a[2], b[2], select)
    result[3] = mux(a[3], b[3], select)
    return result

def four_to_one_mux(a, b, c, d, select0, select1):
    result1 = four_bit_mux(a, b, select0)
    result2 = four_bit_mux(c, d, select0)
    result = four_bit_mux(result1, result2, select1)
    return result

def four_bit_and(a,b):
    result = [0,0,0,0]
    result[0] = AND(a[0], b[0])
    result[1] = AND(a[1], b[1])
    result[2] = AND(a[2], b[2])
    result[3] = AND(a[3], b[3])
    return result

def four_bit_or(a,b):
    result = [0,0,0,0]
    result[0] = OR(a[0], b[0])
    result[1] = OR(a[1], b[1])
    result[2] = OR(a[2], b[2])
    result[3] = OR(a[3], b[3])
    return result

def four_bit_xor(a,b):
    result = [0,0,0,0]
    result[0] = XOR(a[0], b[0])
    result[1] = XOR(a[1], b[1])
    result[2] = XOR(a[2], b[2])
    result[3] = XOR(a[3], b[3])
    return result

def four_bit_complement(a):
    result = [0,0,0,0]

    result[0] = NOT(a[0])
    result[1] = NOT(a[1])
    result[2] = NOT(a[2])
    result[3] = NOT(a[3])

    result = four_bit_adder(result, [0,0,0,1])

    return result[:4]

def four_bit_zero(a):
    if a == [0,0,0,0]:
        return 1
    else:
        return 0


def alu(a, b, select0, select1):
    and_result = four_bit_and(a,b)
    or_result = four_bit_or(a, b)
    xor_result = four_bit_xor(a,b)
    add_result = four_bit_adder(a,b)

    #and_result = 00
    #or_result = 01
    #xor_result = 10
    #add_result = 11

    result1 = four_bit_mux(and_result, or_result, select0)
    result2 = four_bit_mux(xor_result, add_result, select0)

    result = four_bit_mux(result1, result2, select1)
    return result

def decode_bits(bits):
    num = 0
    for i in range (len(bits)):
        num += bits[i] * 2**(len(bits) - i - 1)
    return num

class Register:
    def __init__(self):
        self.value = [0,0,0,0]
        self.input = [0,0,0,0]
        self.load = 0

    def tick(self):
        next_value = mux(self.value, self.input, self.load)
        self.value = next_value
        return self.value

class FourBitRegister:
    def __init__(self):
        self.register1 = Register()
        self.register2 = Register()
        self.register3 = Register()
        self.register4 = Register()
        self.register = []

    def tick(self, input, load):
        self.register1.input = input[0]
        self.register2.input = input[1]
        self.register3.input = input[2]
        self.register4.input = input[3]
        self.register1.load = load
        self.register2.load = load
        self.register3.load = load
        self.register4.load = load
        self.register1.tick()
        self.register2.tick()
        self.register3.tick()
        self.register4.tick()
        self.register = [self.register1.value, self.register2.value, self.register3.value, self.register4.value]
        return self.register

class RegisterFile:
    def __init__(self):
        R0 = FourBitRegister()
        R1 = FourBitRegister()
        R2 = FourBitRegister()
        R3 = FourBitRegister()
        self.registers = [R0, R1, R2, R3]

    def write_register(self, register_number, value):
        self.registers[register_number].tick(value, 1)

    def read_register(self, register_number):
        return self.registers[register_number].register

class InstructionRegister:
    def __init__(self):
        self.instruction = []

    def write(self, instruction):
        if len(instruction) == 8:
            self.instruction = instruction
        else:
            print("Invalid Instruction")

    def return_instruction(self):
        return self.instruction

    def clear_instruction(self):
        self.instruction = []


class ControlUnit():
    def __init__(self):
        self.instruction_list = {
            (0,0,0,0) : "LOAD",
            (0,0,0,1) : "STORE",
            (0,0,1,0) : "ADD",
            (0,0,1,1) : "SUB",
            (0,1,0,0) : "AND",
            (0,1,0,1) : "OR",
            (0,1,1,0) : "XOR",
            (0,1,1,1) : "JUMP",
            (1,0,0,0) : "HALT",
            (1,0,0,1) : "JZ",
            (1,0,1,0) : "CMP",
            (1,0,1,1) : "JNZ",
        }

    def decode(self, instruction):
        handler = self.instruction_list.get(tuple(instruction))

        if handler:
            return handler



class ProgramCounter:
    def __init__(self):
        self.address = 0

    def read(self):
        return self.address

    def increment(self):
        self.address += 1

    def reset_address(self):
        self.address = 0

class Memory:
    def __init__(self):
        self.memory = [[0,0,0,0,0,0,0,0]]
        self.memory *= 16

    def write(self,location , value):
        if len(value) <= 8:
            for i in range (8 - len(value)):
                value.append(0)
            self.memory[location] = value
        else:
            print("Memory Error\n Memory only contains 8 bits")

    def read(self,location):
        return self.memory[location]

    def clear(self):
        self.memory = [[0,0,0,0,0,0,0,0]]
        self.memory *= 16

class DataMemory:
    def __init__(self):
        self.memory = [[0,0,0,0]]
        self.memory *= 16

    def write(self,location , value):
        if len(value) <= 4:
            for i in range (4 - len(value)):
                value.append(0)
            self.memory[location] = value
        else:
            print("Memory Error\n Data Memory only contains 4 bits")

    def read(self,location):
        return self.memory[location]

    def clear(self):
        self.memory = [[0,0,0,0]]
        self.memory *= 16

class CPU:
    def __init__(self):
        self.memory = Memory()
        self.data_memory = DataMemory()
        self.registers = RegisterFile()
        self.counter = ProgramCounter()
        self.instruction_register = InstructionRegister()
        self.control_unit = ControlUnit()
        self.zero_flag = 0

    def tick(self):
        instruction = self.instruction_register.instruction = self.memory.read(self.counter.read())
        opcode = instruction[:4]
        operand = instruction[4:]
        command = self.control_unit.decode(opcode)
        self.counter.increment()

        if command == "LOAD":
            operand = decode_bits(operand)
            self.registers.write_register(0, self.data_memory.read(operand))
        elif command == "STORE":
            operand = decode_bits(operand)
            self.data_memory.write(operand, self.registers.read_register(0))
        elif command == "ADD":
            operand = decode_bits(operand)
            self.registers.write_register(0, alu(self.registers.read_register(0), self.registers.read_register(operand), 1, 1))
        elif command == "SUB":
            operand = decode_bits(operand)
            sub = four_bit_complement(self.registers.read_register(operand))
            self.registers.write_register(0, alu(self.registers.read_register(0), sub, 1, 1))
        elif command == "AND":
            operand = decode_bits(operand)
            self.registers.write_register(0, four_bit_and(self.registers.read_register(operand), self.registers.read_register(0)))
        elif command == "OR":
            operand = decode_bits(operand)
            self.registers.write_register(0, four_bit_or(self.registers.read_register(operand), self.registers.read_register(0)))
        elif command == "XOR":
            operand = decode_bits(operand)
            self.registers.write_register(0, four_bit_xor(self.registers.read_register(operand), self.registers.read_register(0)))
        elif command == "JUMP":
            operand = decode_bits(operand)
            self.counter.address = operand
        elif command == "HALT":
            print("HALT PROCEED")
            exit()
        elif command == "JZ":
            operand = decode_bits(operand)
            if self.zero_flag == 1:
                self.counter.address = operand
        elif command == "CMP":
            operand = decode_bits(operand)
            sub = four_bit_complement(self.registers.read_register(operand))
            result = alu(self.registers.read_register(0), sub, 1, 1)
            if four_bit_zero(result):
                self.zero_flag = 1
            else:
                self.zero_flag = 0
        elif command == "JNZ":
            operand = decode_bits(operand)
            if self.zero_flag == 0:
                self.counter.address = operand

        if four_bit_zero(self.registers.read_register(0)):
            self.zero_flag = 1
        else:
            self.zero_flag = 0

class Assembler:
    def __init__(self):
        self.bits = []
        self.instruction = ""
        self.instructions = {
            "LOAD" : [0,0,0,0],
            "STORE" : [0,0,0,1],
            "ADD" : [0,0,1,0],
            "SUB" : [0,0,1,1],
            "AND" : [0,1,0,0],
            "OR" : [0,1,0,1],
            "XOR" : [0,1,1,0],
            "JUMP" : [0,1,1,1],
            "HALT" : [1,0,0,0],
            "JZ" : [1,0,0,1],
            "CMP" : [1,0,1,0],
            "JNZ" : [1,0,1,1],
        }
        self.labels = {}

    def encode(self, value):
        bits = [0,0,0,0]
        while value > 0:
            if value >= 8:
                bits[0] = 1
                value -= 8
            if value >= 4:
                bits[1] = 1
                value -= 4
            if value >= 2:
                bits[2] = 1
                value -= 2
            if value >= 1:
                bits[3] = 1
                value -= 1
        self.bits = bits
        return bits

    def assemble(self, instruction):
        result = []
        instruction = instruction.split(" ")
        if instruction[0] in self.instructions:
            if instruction[0] == "HALT":
                if len(instruction) != 1:
                    print("INVALID OPERAND")
                    return None
                else:
                    self.instruction = self.instructions.get(instruction[0])
                    for bit in self.instruction:
                        result.append(bit)
                    for bit in [0,0,0,0]:
                        result.append(bit)
            else:
                if len(instruction) == 1:
                    print("INVALID OPERAND")
                    return None
                elif instruction[1].isdigit():
                    if -1 > int(instruction[1]) or int(instruction[1]) > 15:
                        print("INVALID OPERAND")
                        return None
                    else:
                        self.instruction = self.instructions.get(instruction[0])
                        for bit in self.instruction:
                            result.append(bit)
                        for bit in self.encode(int(instruction[1])):
                            result.append(bit)
                else:
                    operand = self.labels.get(instruction[1])
                    if operand is None or -1 > operand or operand > 15:
                        print("INVALID OPERAND")
                        return None
                    self.instruction = self.instructions.get(instruction[0])

                    for bit in self.instruction:
                        result.append(bit)

                    operand = self.labels.get(instruction[1])

                    for bit in self.encode(operand):
                        result.append(bit)
            print("ASSEMBLED:", instruction, len(result), result)
            return result
        else:
            if instruction[0] == "LOOP:":
                return None
            else:
                print("INVALID INSTRUCTION")
                return None

    def assemble_program(self, program):
        result = []
        address = 0
        for line in program:
            parts = line.split(" ")
            if parts[0].endswith(":"):
                self.labels[parts[0].rstrip(":")] = address
            else:
                instruction = [address]
                instruction.extend(self.assemble(line))
                result.append(instruction)
                address += 1
        return result


cpu = CPU()

# Put some data into data memory
cpu.data_memory.write(1, [0, 1, 0, 0])  # counter
cpu.data_memory.write(2, [0, 0, 0, 0])  # result

# Put 3 into R1, 1 to R2
cpu.registers.write_register(1, [0,0,1,1])
cpu.registers.write_register(2, [0,0,0,1]) #sub-ber
cpu.registers.write_register(3, [0,0,0,0]) #comparer

assembler = Assembler()
program = [
    "LOOP:",
    "LOAD 2",
    "ADD 1",
    "STORE 2",
    "LOAD 1",
    "SUB 2",
    "STORE 1",
    "CMP 3",
    "JNZ LOOP",
    "HALT",
]

program = assembler.assemble_program(program)

for instruction in program:
    operation = instruction[1:]
    address = instruction[0]
    cpu.memory.write(address, operation)

while True:
    cpu.tick()
    print(cpu.registers.read_register(0))
    print(cpu.data_memory.read(2))
