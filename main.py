import random

allNeighbors = {}
cameFrom = {}

class PancakeState:
  def __init__(self, stack):
    self.f = 0
    self.g = 0
    self.h = 0
    self.stack = stack
    self.hash = self.hashify()
    self.parent = None
  def copyStack(self):
    return self.stack[:]
  def hashify(self):
    return "".join([str(i) for i in self.stack])
  def flip(self, i):
    flips = []
    for n in range(i):
      flips.append(self.stack.pop())
    for n in range(i):
      self.stack.append(flips.pop(0))
    self.hash = self.hashify()
  def heuristic(self):
    cost = 0
    for i in range(len(self.stack) - 1):
      if (abs(self.stack[i + 1] - self.stack[i]) > 1):
        cost += 1
    return cost
  def distance(self, other):
    cost = 0
    for i in range(len(self.stack)):
      cost += 1
      if self.stack[i] != other.stack[i]:
        break
    return len(self.stack) - cost
  def generateNeighbors(self):
    neighbors = []
    for i in range(len(self.stack) - 1):
      neighbor = PancakeState(self.copyStack())
      neighbor.flip(i + 2)
      if neighbor.hash in allNeighbors:
        neighbors.append(allNeighbors[neighbor.hash])
      else:
        neighbors.append(neighbor)
    return neighbors

def gscore(stack):
  return

def checkList(container, value):
  for i in range(len(container)):
    if container[i] == value:
      return i
  return -1

def isInList(container, pancake):
  for i in range(len(container)):
    success = True
    for j in range(len(pancake.stack)):
      if container[i].stack[j] != pancake.stack[j]:
        success = False
        break
    if success:
      return True
  return False

def stack_pancakes():
  # generate a random initial state of pancakes size [1, 10]
  initialState = list(range(20))[1:]
  random.shuffle(initialState)
  
  initialPancake = PancakeState(initialState)
  initialPancake.g = 0
  initialPancake.h = initialPancake.heuristic()
  initialPancake.f = initialPancake.h

  print("INITIAL STATE:")
  print(initialPancake.stack)
 
  open_set = {}
  closed_set = {}
  open_set[initialPancake.hash] = initialPancake
  finalValue = None

  while len(open_set) > 0:
    smallestKey = min(open_set, key=lambda k: open_set[k].f)
    top = open_set[smallestKey]
    if top.heuristic() == 0:
      finalValue = top
      break
    del open_set[smallestKey]
    closed_set[smallestKey] = top
    neighbors = top.generateNeighbors()
    for neighbor in neighbors:
      cost = top.g + neighbor.distance(top)
      if neighbor.hash in open_set:
        if neighbor.g <= cost:
          continue
      elif neighbor.hash in closed_set:
        if neighbor.g <= cost:
          continue
        open_set[neighbor.hash] = closed_set[neighbor.hash]
        del closed_set[neighbor.hash]
      else:
        open_set[neighbor.hash] = neighbor
        neighbor.h = neighbor.heuristic()
        neighbor.f = neighbor.h + neighbor.g
      neighbor.g = cost
      cameFrom[neighbor.hash] = top
        
  path = []
  while finalValue.hash != initialPancake.hash:
    path.append(finalValue)
    finalValue = cameFrom[finalValue.hash]
  
  path.reverse()

  for p in path:
    print(p.stack)


stack_pancakes()
