#Main memory, 16 registers
class Memory():
  # Initializes registers full of zeros
  def __init__(self):
    self.number_registers = [0 for i in range(16)]
    self.numbers_index = 1
    
  def store(self, value_to_store, address):
    self.number_registers[address] = value_to_store
    return

  def load( self, register_address):
    index = register_address
    int_value = self.number_registers[index]
    return int_value