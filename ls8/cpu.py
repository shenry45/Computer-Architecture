"""CPU functionality."""

import sys

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

        program = [
            # From print8.ls8
            0b10000010, # LDI
            0b00000000, # REG 0 identifier
            0b00001000, # 8 value
            0b01000111, # PRN
            0b00000000, # REG 0 identifier
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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
            reg_a = getattr(self.ram[reg_a])
            reg_b = getattr(self.reg[reg_b])
            if reg_b == 0:
                # TODO Halt
                print('Error on operation: DIV')
        elif op == 0b00000001:
            '''HLT'''
            exit()
        elif op == 'INC':
            setattr(self.reg[reg_a], reg_a + 1)
        elif op == 'INT':
            setattr(self.reg[7], reg_a)
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
            # get reg address to write to
            reg_addr = self.ir['PC'] + 1
            reg_val = self.ram[reg_addr]
            # get int addr for reg write
            int_addr = self.ir['PC'] + 2
            integer_val = self.ram[int_addr]
            # set reg addr to int value
            self.ram_write(reg_val, integer_val)
            
            self.ir['PC'] += 3
        elif op == 'MOD':
            pass
        elif op == 'MUL':
            pass
        elif op == 'NOP':
            pass
        elif op == 'NOT':
            pass
        elif op == 'OR':
            pass
        elif op == 'POP':
            pass
        elif op == 'PRA':
            pass
        elif op == 0b01000111:
            '''PRN'''
            print(self.reg[reg_a])
            self.ir['PC'] += 2

        elif op == 'PUSH':
            # change SP
            self.reg[7] -= 1
            # copy value from register into memory
            reg_num = self.ram[self.ir['PC'] + 1]
            value = self.ram[reg_num + 1]

            address = self.reg[7]
            self.ram[address] = value

            pc += 2
            
        elif op == 'RET':
            pass
        elif op == 'SHL':
            setattr(self.reg[reg_a], reg_a << reg_b)
        elif op == 'SHR':
            setattr(self.reg[reg_a], reg_a >> reg_b)
        elif op == 'ST':
            setattr(self.reg[reg_b], reg_a)
        elif op == 'SUB':
            setattr(self.reg[reg_a], reg_a - reg_b)
        elif op == 'XOR':
            setattr(self.reg[reg_a], reg_a ^ reg_b)
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

        print()

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
