"""CPU functionality."""

import sys
from pathlib import Path

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.ir = {
            'PC': 00,
            'IR': '',
            'MAR': '',
            'MDR': ''
        }
        self.fl = {
            'L': 0,
            'G': 0,
            'E': 0
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
                    bin_lit = int(line[0], 2)
                    program.append(bin_lit)

            for instruction in program:
                self.ram[address] = instruction
                address += 1

        except FileNotFoundError:
            print("%s not found" % (sys.argv[1]))



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            reg_a = getattr(self.ram[reg_a])
            reg_b = getattr(self.reg[reg_b])
            setattr(self.reg[reg_a], reg_a + reg_b)
        elif op == "AND":
            reg_a = getattr(self.ram[reg_a])
            reg_b = getattr(self.reg[reg_b])
            setattr(self.reg[reg_a], reg_a & reg_b)
        elif op == "CALL":
            # TODO: Push address to top of stack
            # reverse counter after?
            pass
        elif op == "CMP":
            if reg_a == reg_b:
                setattr(self.fl['E'], 1)
            else:
                setattr(self.fl['E'], 0)

            if reg_a < reg_b:
                setattr(self.fl['L'], 1)
            else:
                setattr(self.fl['L'], 0)
            
            if reg_a > reg_b:
                setattr(self.fl['G'], 1)
            else:
                setattr(self.fl['G'], 0)
        elif op == 'DEC':
            setattr(self.reg[reg_a], reg_a - 1)
        elif op == 'DIV':
            pass
        elif op == 0b00000001:
            '''HLT'''
            exit()
        elif op == 'INC':
            reg_val = self.reg
            self.ram_write(reg_a, )
        elif op == 'INT':
            pass
        elif op == 'IRET':
            pass
        elif op == 'JEQ':
            pass
        elif op == 'JGE':
            pass
        elif op == 'JGT':
            pass
        elif op == 'JLE':
            pass
        elif op == 'JLT':
            pass
        elif op == 'JMP':
            pass
        elif op == 'JNE':
            pass
        elif op == 'LD':
            pass
        elif op == 0b10000010:
            '''LDI'''
            self.reg[reg_a] = reg_b            
            self.ir['PC'] += 3
        elif op == 'MOD':
            pass
        elif op == 0b10100010:
            ''' MUL '''
            reg_a_val = self.reg[reg_a]
            reg_b_val = self.reg[reg_b]

            multiply_val = reg_a_val * reg_b_val

            self.ram_write(reg_a, multiply_val)

            self.ir['PC'] += 3
        elif op == 'NOP':
            pass
        elif op == 'NOT':
            pass
        elif op == 'OR':
            pass
        elif op == 0b01000110:
            ''' POP '''
            sp_val = self.reg[7]
            self.reg[reg_a] = sp_val

            self.reg[7] += 1
            self.ir['PC'] += 2
        elif op == 'PRA':
            pass
        elif op == 0b01000111:
            '''PRN'''
            print(self.reg[reg_a])
            self.ir['PC'] += 2
        elif op == 0b01000101:
            ''' PUSH '''
            # change SP
            self.reg[7] -= 1
            # copy value from register into memory
            reg_val = self.reg[reg_a]

            address = self.reg[7]
            self.ram[address] = reg_val

            self.ir['PC'] += 2     
        elif op == 'RET':
            pass
        elif op == 'SHL':
            pass
            # setattr(self.reg[reg_a], reg_a << reg_b)
        elif op == 'SHR':
            pass
            # setattr(self.reg[reg_a], reg_a >> reg_b)
        elif op == 'ST':
            pass
            # setattr(self.reg[reg_b], reg_a)
        elif op == 'SUB':
            pass
            # setattr(self.reg[reg_a], reg_a - reg_b)
        elif op == 'XOR':
            pass
            # setattr(self.reg[reg_a], reg_a ^ reg_b)
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
    def ram_write(self, reg, val):
        self.reg[reg] = val

    def run(self):
        """Run the CPU."""
        # init stack pointer at F4
        self.reg[7] = 0xF4
        # init program counter at 00
        self.ir['PC'] = 0x00

        # run commands until
        while self.ram[self.ir['PC']] != 0:
            command_addr = self.ir['PC']
            reg_a_val = self.ram[command_addr + 1]
            reg_b_val = self.ram[command_addr + 2]
            command_val = self.ram[command_addr]
            # run command
            self.alu(command_val, reg_a_val, reg_b_val)
