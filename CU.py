# Control Unit, decodes machine code
class CU():
  # Checks that the machine code is HALT and the lenght of the machine code is appropiat. Then initializes the splitting the machine code into parts.
  def __init__(self, instruction):
    if instruction == ';':
      instruction = 'trmnte'+'0'*26
    
    elif len(instruction) != 32:
      print("Invalid Instruction Length")
      instruction = 'invlid'+'0'*26
    
    self.opcode = instruction[0:6]
    self.source_one = instruction[6:11]
    self.source_two = instruction[11:16]
    self.store = instruction[16:26]
    self.function_code = instruction[26:]
  
  # Decodes the machine code. If input is not in ISA then the return is 'a'.
  def output(self):
    if self.opcode == '000000':
      ops_list = ['ADD', 'SUB', 'SLT']
      if self.function_code == '100000':
        ops = ops_list[0]
      elif self.function_code == '100010':
        ops = ops_list[1]
      else:
        ops = ops_list[2]
        
      return [ops, int(self.source_one,2), int(self.source_two, 2), int(self.store[:5],2)]
    
    if self.opcode == '001000':
      return ['ADDI', int(self.source_one, 2), int(self.source_two, 2), int(self.store + self.function_code, 2)]
    
    elif self.opcode == '000101':
      return ['BNE', int(self.source_one, 2), int(self.source_two, 2), int(self.store + self.function_code, 2)]
    
    elif self.opcode == '100011':
      return ['LW', int(self.source_one, 2), int(self.source_two, 2), int(self.store + self.function_code, 2)]
    
    elif self.opcode == '101011':
      return ['SW', int(self.source_one, 2), int(self.source_two, 2), int(self.store + self.function_code, 2)]
    
    elif self.opcode == '000010':
      return ['J', int(self.source_one + self.source_two + self.store + self.function_code, 2)]
    
    elif self.opcode == '000011':
      return ['JAL', int(self.source_one + self.source_two + self.store + self.function_code, 2)]
    
    elif self.opcode == '011111':
      return ['CACHE', int(self.source_two, 2)]
    
    elif self.opcode == 'invlid':
      return None
    
    elif self.opcode == 'trmnte':
      return ['terminate']
      
    else:
      return 'a' #some mesage saying invalid instructions
