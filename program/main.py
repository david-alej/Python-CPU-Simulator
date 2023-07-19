# This code represents a CPU class made up of a program counter register, CU, and ALU. The CU decodes the machine code and the ALU does combinatrices. Both the CU and ALU are represented as class's while the program counter is an initialized number.The ALU class has the main memory and cache inside it because it is the one sending and receiving signals by them. 
from CPU import CPU

instr_file = 'instruction_input.txt'
data_input = 'data_input.txt'

def fetch_file(file):
  raw_file = open(file, 'r')
  file_list = raw_file.readlines()
  file_list = list( map(lambda x: x.strip(), file_list) )
  return file_list

instr_list = fetch_file(instr_file)
data_list = fetch_file(data_input)

print('Welcome to the Python CPU Simulator. Initializing the CPU with initial data to store in the Main memory and some instructions.\n')

mycpu = CPU(instr_list, data_list)
mycpu.calculate()

