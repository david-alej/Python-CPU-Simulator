from CU import CU
from ALU import ALU

class CPU:
  # Decodes instruction list, using CU class, to put into a decoded instrution list Then initializes program counter and ALU. Stores values into Main memory.
  def __init__(self, instruction_list, data_list):
    self.instr_list = []
    for instr in instruction_list:
      self.instr_list.append( CU(instr).output())
    
    self.programcounter = 0
    self.alu = ALU()
    for data in data_list:
      data_parsed = data.split(',')
      value = int(data_parsed[1])
      address = int(data_parsed[0], 2)
      self.alu.mainmem.store(value, address)
    
    print(f'\n{len(data_list)} values where stored in the main memory.')
    #If there is something wrong with the instructions this will deal with it.
    self.num_invalid = 0
    self.invalid_pos = []
    for i in range(len(self.instr_list)):
      if self.instr_list[i] == None:
        self.num_invalid += 1
        self.invalid_pos.append(i)
        print(f"Invalid Instruction Length at instruction list index {i}")
      
      elif self.instr_list[i] == 'a':
        self.num_invalid += 1
        self.invalid_pos.append(i)
        print('Instruction not applicable to this ISA.')
    
    print(f'\n{len(instruction_list)} Instructions where decoded.\n')  
    print('-'*50)
    print(f'CPU values before instructions:\n\nPorgram Counter = {self.programcounter}\n\nMain memory registers = {self.alu.mainmem.number_registers}\n\nCache is {self.alu.cache10} (1 for on and 0 for off)\n\nCache = {self.alu.cache.data}')
    print('-'*50 + '\n')
        
  def calculate(self):
    if self.num_invalid > 0:
      return print(f"Please review instruction list to make sure that the instructions are valid. Invalid instructions at instruction indexes:\n\n{self.invalid_pos}")
    
    print(f'Proccessing Instructions.\n')
    
    #Using ALU class to apply instructions
    for i in self.instr_list:
      # Add, Subtract, and SLT all contain: address one, address two, final address
      if i[0] == 'ADD':
        num1 = self.alu.extract(i[1])
        num2 = self.alu.extract(i[2])
        value = self.alu.add(num1, num2)
        address = i[3]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\n\nADD: {num1} + {num2} --> Register {address}\n\n')
      
      # 
      elif i[0] == 'SUB':
        num1 = self.alu.extract(i[1])
        num2 = self.alu.extract(i[2])
        value = self.alu.subtract(num1, num2)
        address = i[3]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\n\nSUB: {num1} - {num2} --> Register {address}\n\n')
        
      #  
      elif i[0] == 'SLT':
        num1 = self.alu.extract(i[1])
        num2 = self.alu.extract(i[2])
        value = self.alu.slt(num1, num2)
        address = i[3]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\n\nSUB: ({num1} < {num2}) 1:0 --> Register {address}\n\n')
        
      # Address1, address2, immediate
      elif i[0] == 'ADDI':
        num1 = self.alu.extract(i[1])
        num2 = self.alu.extract(i[3])
        value = self.alu.add(num1, num2)
        address = i[2]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\n\nADDI: {num1} + {num2} --> Register {address}\n\n')
       
      # address1, address2, offset 
      elif i[0] == 'BNE':
        num1 = self.alu.extract(i[1])
        num2 = self.alu.extract(i[2])
        value = self.alu.bne(num1, num2, i[3], self.programcounter)
        print(f'\nBNE: If {num1} does not equal {num2} then ({self.programcounter} + 4) + {i[3]}*4 --> programcounter\n')
        if value is not None:
          self.programcounter = value
          
        
      
      # instr_idx
      elif i[0] == 'J':
        value = int(self.alu.j(i[1], self.programcounter), 2)
        self.programcounter = value
        print(f'\nJ: programcounter_(31:28)||{i[1]}||00 --> Programcounter\n')
        
      # 
      elif i[0] == 'JAL':
        value = self.programcounter + 4
        address = self.alu.mainmem.number_registers[-1]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\nJAL: 1) {self.programcounter} + 4 --> Register 15\n\t2) programcounter_(31:28)||{i[1]}||00 --> Porgramcounter\n')
        value = int(self.alu.j(i[1], self.programcounter), 2)
        self.programcounter = value
        
       
      # address1, address2, offset 
      elif i[0] == 'LW':
        num1 = self.alu.extract(i[1])
        value = self.alu.extract(num1+ i[3])
        address = i[2]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\nLW: Mem[ {num1} + {i[3]} ] --> Register {i[2]}\n')
        
      # address1, address2, offset 
      elif i[0] == 'SW':
        num1 = self.alu.extract(i[1])
        value = self.alu.extract(i[2])
        address = num1+ i[3]
        self.alu.mainmem.store(value, address)
        self.alu.cache.write(value, address)
        print(f'\nSW: Register {i[2]} --> Mem[ {num1} + {i[3]} ]\n')
        
      elif i[0] == 'CACHE':
        self.alu.cache_op(i[1])
        
      elif i[0] == 'terminate':
        print('\nHALT: Instructions Terminated\n')
        break
      
      else:
        print('\nInvalid Instruction. Instructions Terminated\n')
        break
      
      self.programcounter += 1
    
    print('-'*50)
    print(f'CPU values after instructions:\n\nPorgram Counter = {self.programcounter}\n\nMain memory registers = {self.alu.mainmem.number_registers}\n\nCache is {self.alu.cache10} (1 for on and 0 for off)\n\nCache = {self.alu.cache.data}')
    print('-'*50 + '\n')