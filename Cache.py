#Write-through policy, fifo-replacement policy
class Cache():
  def __init__(self):
    self.fifo_indices = [0, 0, 0, 0]
    self.sets = 1 # Set to 1, 2 or 4
    self.fifo_indices = [0, None, None, None]

    if self.sets == 2:
      self.fifo_indices = [0, 2, None, None]
    elif self.sets == 4:
      self.fifo_indices = [0, 1, 2, 3]

    self.data = [
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
    ]

  def write(self, address, data):
    entry = self.get_entry(address)
    if entry is not None:
      entry["data"] = data

    else:
      self.replace_entry(address, data)

  def read(self, address):
    data = None
    entry = self.get_entry(address)
    if entry is not None:
      data = entry["data"]
      return data
    else:
      return None 

  def replace_entry(self, address, data):
    index = 0
    set_number = address % self.sets
    index = self.fifo_policy(set_number)
    self.data[index] = {"tag": address, "data": data}

  def fifo_policy(self, set_number):
    index = self.fifo_indices[set_number]
    self.fifo_indices[set_number] += 1
    if self.fifo_indices[set_number] == len(self.data)/self.sets+(set_number*int(len(self.data)/self.sets)):
      self.fifo_indices[set_number] = set_number*int(len(self.data)/self.sets)

    return self.fifo_indices[set_number]

  # Returns entry on cache hit
  # Returns None on cache miss
  def get_entry(self, address):
    for entry in self.data:
      if entry["tag"] == address and entry["data"] != "":
          return entry
        
    return None