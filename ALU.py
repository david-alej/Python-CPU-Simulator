from MainMemory import Memory
from Cache import Cache

# Contains the Memory and cache class
class ALU:
  #initializes Memeory, cache class, and a number (1 or 0) to decide if the chache is on or off.
  def __init__(self):
    self.mainmem = Memory()
    self.cache = Cache()
    self.cache10 = 1
      
  # Helper function to extract values from addresses using cache hit or miss when cahce is on.
  def extract(self, address):
    if self.cache10 == 1:
      print('Cache Read: ')
      num = self.cache.read(address)
      if num is None:
        num = self.mainmem.load(address)
        print(f'Miss - Main Memory read: {num} \n')
        self.cache.replace_entry(address, num)
      
      else:
        num = int(num)
        print(f'Cache Hit: {num}')
        
    else:
      num = self.mainmem.load(address)
      print(f'Main memory read: {num}')
      
    return num
  
  # The rest are the operations that the ALU does
  def add(self, num1, num2):
    return num1 + num2
    
  def subtract(self, num1, num2):
    return num1 - num2


  def slt(self, num1, num2):
    if num1 < num2:
      return 1
    else:
      return 0
    
  def bne(self, num1, num2, offset, programcounter):
    if num1 != num2:
      programcounter = (programcounter + 4) + offset*4
      return programcounter
    
    else:
      return None
  
  def j(self, instr_idx, programcounter):
    front = self.binbits( programcounter, 32)
    middle = self.binbits(instr_idx, 26)
    back = '00'
    return front[0:4] + middle + back
  
  # in JAL operations the first operation goes to the last address in the main memory address 15, not 31.

  def lw(self, base, address2, offset):
    return [ base + int(offset, 2), address2]
  
  def sw(self, base, address2, offset):
    return [address2, base+ offset]
  
  def cache_op(self, op):
    if op == 0:
      self.cache10 = 0
      return print('\nCache Off\n')
    
    elif op == 1:
      self.cache10 = 1
      return print('\nCache On\n')
    
    elif op == 2:
      for i in range(len(self.data)):
        self.cache.data[i]['tag'] = None
        self.cache.data[i]['data'] = ''
      return print('\nCache Flushed\n')
    
    else:
      print('\nInvalid Opocode\n')
      return None
  
  # Helper function ment to get number in binary that has a certain number of bits.
  def binbits(self, x, n):
    bits = bin(x).split('b')[1]
    if len(bits) <= n:
      return '0'*(n-len(bits)) + bits

    else:
      print(f'\n{x} exceeds given bit number, {n}')
      return None
    