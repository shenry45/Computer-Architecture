"""CPU functionality."""

import sys
from pathlib import Path

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 00
        self.fl = {
            'L': 0,
            'G': 0,
            'E': 0
        }
        self.opcodes = {
            0b10100000: "ADD",
            0b01010000: "CALL",
            0b10000010: "LDI",
            0b00010001: "RET",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01000111: "PRN",
            0b00000001: "HLT",
            0b10100111: "CMP",
            0b01010101: "JEQ",
            0b01010100: "JMP",
            0b01010110: "JNE"
        }
        self.branchtable = {
            "HLT": self.hlt,
            "PRN": self.prn,
            "LDI": self.ldi,
            "RET": self.ret,
            "PUSH": self.push,
            "POP": self.pop,
            "CALL": self.call,
            "JEQ": self.jeq,
            "JMP": self.jmp,
            "JNE": self.jne
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        if len(sys.argv) != 2:
            print("File parameters for %s not met" % (sys.argv[0]))
            sys.exit(2)

        try:
            path = Path(f"examples/{sys.argv[1]}")
            with open(path) as file:
                for line in file:
                    if line[0] == '#' or line == '' or line == '\n':
                        continue
                    line = line.split()
                    # add binary literal from binary string to program
                    binary_lit = int(line[0], 2)
                    # program.append(bin_lit)
                    self.ram[address] = binary_lit
                    address += 1

        except FileNotFoundError:
            print("%s not found" % (sys.argv[1]))


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]            
        elif op == "CMP":
            reg_a = self.reg[reg_a]
            reg_b = self.reg[reg_b]

            if reg_a == reg_b:
                self.fl['E'] = 1
            else:
                self.fl['E'] = 0

            if reg_a < reg_b:
                self.fl['L'] = 1
            else:
                self.fl['L'] = 0
            
            if reg_a > reg_b:
                self.fl['G'] = 1
            else:
                self.fl['G'] = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(self, reg):
        return self.ram[reg]
    def ram_write(self, addr, val):
        self.ram[addr] = val

    def run(self):
        """Run the CPU."""
        # init stack pointer at F4
        self.reg[7] = 0xF4
        # init program counter at 00
        self.pc = 0x00

        # run commands until init value found
        while self.ram[self.pc] != 0:
            IR = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            num_operands = (IR >> 6)

            sets_pc = ((IR >> 4) & 0b0001) == 1

            is_alu_comm = ((IR >> 5) & 0b001) == 1

            opcode = self.opcodes[IR]

            if not sets_pc:
                self.pc += 1 + num_operands

            if is_alu_comm:
                self.alu(opcode, op_a, op_b)
            else:
                self.branchtable[opcode](op_a, op_b)
            
    
    def prn(self, op_a, _):
        print(self.reg[op_a])

    def hlt(self, _, __):
        sys.exit(2)

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b

    def ret(self, _, __):
        self.pc = self.ram[self.reg[7]]

    def push(self, op_a, _):
        # change SP
        self.reg[7] -= 1
        # copy value from register into memory
        reg_val = self.reg[op_a]

        address = self.reg[7]
        self.ram[address] = reg_val

    def pop(self, op_a, __):
        sp_val = self.ram[self.reg[7]]
        self.reg[op_a] = sp_val

        self.reg[7] += 1

    def call(self, op_a, _):
        # pushes next command address stack
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc + 2
        # takes in register to move PC to
        self.pc = self.reg[op_a]

    def jeq(self, op_a, _):
        if self.fl['E'] == 1:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    def jmp(self, op_a, _):
        self.pc = self.reg[op_a]

    def jne(self, op_a, _):
        if self.fl['E'] == 0:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2