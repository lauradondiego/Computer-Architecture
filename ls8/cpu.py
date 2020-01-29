"""CPU functionality."""
import sys

# decalare opcodes up here instead
ldi = 0b10000010
# Set the value of a register to an integer.
prn = 0b01000111
# Print numeric value stored in the given register.
# Print to the console the decimal integer value that is stored in the given register.
hlt = 0b00000001
# Halt the CPU (and exit the emulator).
mul = 0b10100010
# Multiply the values in two registers together and store the result in registerA.
push = 0b01000101
# Push the value in the given register on the stack.
pop = 0b01000110
# Pop the value at the top of the stack into the given register


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # list of 256 zeros
        # We're essentially making "buckets" for our locations
        # in memory, in which we can use to store bits later.
        self.registers = [0] * 8
        self.pc = 0  # program counter and current value of IR
        # contains a copy of the currently executing instruction (PC)
        # self.ir = 0b00000000
        self.pc = 7
        self.running = False  # initialize running to false
        # pointer (dont need this but makes it easier to visualize)
        self.registers[self.pc] = 0xF4
        # our 8th register at index 7
        # R7 is reserved for stack pointer
        # R7 is set to 0xF4 (0x is prefix for hexidecimal)
        self.branchtable = {}
        self.branchtable[ldi] = self.ldi  # key
        self.branchtable[prn] = self.prn  # key
        self.branchtable[hlt] = self.hlt  # key
        self.branchtable[mul] = self.mul  # key
        self.branchtable[push] = self.push  # key
        self.branchtable[pop] = self.pop  # key


    # ADDING RAM_READ()
    def ram_read(self, mar_address):
        # should accept the address to read and return the value stored there.
        # MAR # holds the memory address we're reading or writing
        return self.ram[mar_address]

    # ADDING RAM_WRITE()
    def ram_write(self, mar_address, mdr_value):
        # should accept a value to write, and the address to write it to.
        # MDR # holds the value to write or the value just read
        self.ram[mar_address] = mdr_value

    # ADDING HLT FUNCTION
    def hlt(self, operand_a, operand_b):
        # halt the CPU and exit the emulator.
        return(0, False)

    # ADDING LDI FUNCTION
    def ldi(self, operand_a, operand_b):
        # load "immediate", store a value in a register,
        # or "set this register to this value".
        self.registers[operand_a] = operand_b
        return (3, True)

    # ADDING PRN FUNCTION
    def prn(self, operand_a, operand_b):
       # a pseudo-instruction that prints the numeric value
       # stored in a register.
        print(self.registers[operand_a])
        return (2, True)

    # ADDING MUL FUNCTION
    def mul(self, operand_a, operand_b):
        self.registers[operand_a] * self.registers[operand_b]
        return (3, True)

    # ADDING PUSH FUNCTION
    def push(self):
        reg = self.ram[self.pc + 1]
        val = self.registers[reg]  # CREATE STACK POINTER
        self.registers[self.pc] -= 1  # decrement stack pointer
        # copy value to given reg
        self.ram[self.registers[self.sp]] = val
        self.pc += 2

    # ADDING POP FUNCTION
    def pop(self):
        reg = self.ram[self.pc + 1]
        val = self.ram[self.registers[self.sp]]
        self.registers[reg] = val
        self.registers[self.sp] += 1  # increment stack pointer
        self.pc += 2

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            # memory = self.ram
            # print("try memory", memory)
            with open(filename) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue  # Ignore blank line
                    value = int(num, 2)   # Base 10, but ls-8 is base 2
                    # print("value", value)
                    # int changes binary strings to int values
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)
    # address = 0

    # # For now, we've just hardcoded a program:

    # program = [
    #     # From print8.ls8
    #     0b10000010,  # LDI R0,8
    #     0b00000000,
    #     0b00001000,
    #     0b01000111,  # PRN R0
    #     0b00000000,
    #     0b00000001,  # HLT
    # ]

    # for instruction in program:
    #     self.ram[address] = instruction
    #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # elif op == "MUL":
        #     self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # ADDING LIST OF COMMANDS NEEDED FOR RUN()
        # ldi = 0b10000010
        # # Set the value of a register to an integer.
        # prn = 0b01000111
        # # Print numeric value stored in the given register.
        # # Print to the console the decimal integer value that is stored in the given register.
        # hlt = 0b00000001
        # # Halt the CPU (and exit the emulator).
        # mul = 0b10100010
        # # Multiply the values in two registers together and store the result in registerA.
        # push = 0b01000101
        # # Push the value in the given register on the stack.
        # pop = 0b01000110
        # Pop the value at the top of the stack into the given register.

        self.running = True

        while self.running:
            self.trace()  # says to call this for help debugging
            # local variable called INSTRUCTION REGISTER
            ir = self.ram[self.pc]
            self.branchtable[ir]()
            # It needs to read the memory address that's
            # stored in register PC (initialized to self.pc = 0) in Class

            # remember to put self. before pc
            # read the bytes at PC+1 and PC+2 and store in variables

            # operand_a = self.ram_read(self.pc + 1)
            # operand_b = self.ram_read(self.pc + 2)

            # op = self.OPCODES[ir]

            # if op == "LDI":
            #     self.ldi()
            # elif op == "PRN":
            #     self.prn()
            # elif op == "MUL":
            #     self.mul()
            # elif op == "PUSH":
            #     self.push()
            # elif op == "POP":
            #     self.pop()
            # elif op == "HLT":
            #     running = False  # stop running
            # else:
            #     print(f'Unknown Commands: {ir}')
            #     sys.exit(1)
            # if ir == ldi:
            #     self.registers[operand_a] = operand_b
            #     # set value of register to an integer
            #     self.pc += 3
            # elif ir == prn:
            #     print(f'{self.registers[operand_a]}')
            #     self.pc += 2
            # elif ir == mul:
            #     # self.reg[operand_a] * self.reg[operand_b]
            #     self.registers[operand_a] = self.registers[operand_a] * \
            #         self.registers[operand_b]
            #     self.pc += 3
            # elif ir == push:
            #     reg = self.ram[self.pc + 1]
            #     val = self.registers[reg]
            #     self.registers[self.sp] -= 1
            #     self.ram[self.registers[self.sp]] = val
            #     self.pc += 2
            # elif ir == pop:
            #     reg = self.ram[self.pc + 1]
            #     val = self.ram[self.registers[self.sp]]
            #     self.registers[reg] = val
            #     self.registers[self.sp] += 1
            #     self.pc += 2
            # elif ir == hlt:
            #     running = False  # stop running
            # else:
            #     print(f'Unknown Commands: {ir}')
            #     sys.exit(1)
