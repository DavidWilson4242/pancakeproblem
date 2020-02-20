import random

class PancakeState:
  
  allNeighbors = {}

  def __init__(self, stack):
    self.f = 0
    self.g = 0
    self.h = 0
    self.stack = stack
    self.hash = self.hashify()

  def copyStack(self):
    return self.stack[:]

  def hashify(self):
    return "".join([str(i) for i in self.stack])
  
  # flips 'i' pancakes at the top of the stack
  def flip(self, i):
    flips = []
    for n in range(i):
      flips.append(self.stack.pop())
    for n in range(i):
      self.stack.append(flips.pop(0))
    self.hash = self.hashify()

  # heuristic function that uses the method outlined in the paper
  # that was provided on canvas
  def heuristic(self):
    cost = 0
    for i in range(len(self.stack) - 1):
      if (abs(self.stack[i + 1] - self.stack[i]) > 1):
        cost += 1
    return cost

  # the distance function tells how many pancakes were flipped between
  # two states.  The states MUST be adjacent, meaning only one flip 
  # must have occured between 'self' and 'other'
  def distance(self, other):
    cost = 0
    for i in range(len(self.stack)):
      cost += 1
      if self.stack[i] != other.stack[i]:
        break
    return len(self.stack) - cost

  # generates all neighboring states.  If the neighbor hasn't been
  # created yet, create it.  Otherwise return a reference into allNeighbors
  def generateNeighbors(self):
    neighbors = []
    for i in range(len(self.stack) - 1):
      neighbor = PancakeState(self.copyStack())
      neighbor.flip(i + 2)
      if neighbor.hash in self.allNeighbors:
        neighbors.append(self.allNeighbors[neighbor.hash])
      else:
        neighbors.append(neighbor)
    return neighbors

def stackPancakes():
  # generate a random initial state of pancakes size [1, 10]
  initialState = list(range(11))[1:]
  random.shuffle(initialState)
  
  # setup the initial state
  initialPancake = PancakeState(initialState)
  initialPancake.g = 0
  initialPancake.h = initialPancake.heuristic()
  initialPancake.f = initialPancake.h

  print("INITIAL STATE:")
  print(initialPancake.stack)
  print("========================================")
  
  # setup the initial A* state
  cameFrom = {}
  openSet = {}
  closedSet = {}
  openSet[initialPancake.hash] = initialPancake
  finalValue = None
  
  # find the goal state, keeping track of where each node came from
  while len(openSet) > 0:
    smallestKey = min(openSet, key=lambda k: openSet[k].f)
    top = openSet[smallestKey]
    if top.heuristic() == 0:
      finalValue = top
      break
    del openSet[smallestKey]
    closedSet[smallestKey] = top
    neighbors = top.generateNeighbors()
    for neighbor in neighbors:
      cost = top.g + neighbor.distance(top)
      if neighbor.hash in openSet:
        if neighbor.g <= cost:
          continue
      elif neighbor.hash in closedSet:
        if neighbor.g <= cost:
          continue
        openSet[neighbor.hash] = closedSet[neighbor.hash]
        del closedSet[neighbor.hash]
      else:
        openSet[neighbor.hash] = neighbor
        neighbor.h = neighbor.heuristic()
        neighbor.f = neighbor.h + neighbor.g
      neighbor.g = cost
      cameFrom[neighbor.hash] = top
        
  # follow the goal state's parents until we reach the initial state,
  # generating a path backwards
  path = []
  while finalValue.hash != initialPancake.hash:
    path.append(finalValue)
    finalValue = cameFrom[finalValue.hash]
  path.reverse()
  
  # print the solution
  print("SOLUTION:")
  for p in path:
    print(p.stack)


stackPancakes()
