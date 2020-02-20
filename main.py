# Artificial Intelligence Pancake Problem
# Code by David Wilson and Yang He
# This code must be run with Python3
#
# Run the program:
# To run the "pancake solver", simply call stackPancakes().  There are
# two optional arguments that you may pass to the function:
#   numPancakes =>   the number of pancakes that you'd like to test flipping with.
#                    defaults to 10.  if initialState has a value, overrides this
#   initialState =>  a list of integers that contains values [1, len(initialState)]
#                    may be passed.  Any ordering is acceptable.  If initialState is
#                    passed, its length overrides numPancakes. If initialState is None, 
#                    a randomly sorted stack from [1, numPancakes] is used. 
#
# A benchmarking function is also included.  It flips stacks of increasing size and
# reports how long each flipping process takes
#
# Finally, the user may pass the number of pancakes to be flipped via command line.
# Example:   python3 main.py 20
# This would flip 20 pancakes, calling stackPancakes(numPancakes=20)

import random
import time
import sys

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

# helper function for printing the output in stackPancakes
def listdif(a, b):
  dif = 0
  for v, k in zip(a, b):
    if v != k:
      break
    dif += 1
  return len(a) - dif

def stackPancakes(numPancakes=10, initialState=None, printResults=True):
  
  if initialState != None:
    numPancakes = len(initialState)

    # validate the user's initial state
    for i in range(numPancakes):
      if not (i + 1) in initialState:
        print("initialState is not well formed.  Must be an array containing " +
              "integers [1, len(initialState)] in any order.")
        return
  else:
    # generate a random initial state of pancakes size [1, 10]
    initialState = list(range(numPancakes + 1))[1:]
    random.shuffle(initialState)
  
  # setup the initial state
  initialPancake = PancakeState(initialState)
  initialPancake.g = 0
  initialPancake.h = initialPancake.heuristic()
  initialPancake.f = initialPancake.h
  
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
    path.append(finalValue.stack)
    finalValue = cameFrom[finalValue.hash]
  path.reverse()

  # our heuristic function says nothing about the ordering of the pancakes.
  # [1, 2, 3, 4, 5] is considered a goal, and so is [5, 4, 3, 2, 1].  To remedy
  # this, simply add one more flip if the array is backwards.  This is a valid
  # move, essentially putting the spatula under the entire stack and flipping it
  # one final time
  if path[-1][0] == 1:
    finalStep = path[-1][:]
    finalStep.reverse()
    path.append(finalStep)

  # insert the initial state at the front of the path, just for
  # output formatting reasons
  path.insert(0, initialState)

  # print the solution
  if printResults:
    print("INITIAL PANCAKE STATE:")
    print(initialState)
    print("========================================")
    print("SOLUTION:")
    print(initialState)
    for i in range(len(path) - 1):
      print(path[i + 1], end="")
      print(" // flipped {} pancakes".format(listdif(path[i], path[i + 1])))

def benchmark():
  for i in range(20):
    stackSize = (i + 1)*10
    startTime = time.time()
    stackPancakes(numPancakes=stackSize, printResults=False)
    print("flipped {} pancakes.  elapsed time: {:.3f} seconds".format(stackSize, float(time.time() - startTime)))

# execute the code!  see top of program for documentation
if len(sys.argv) > 1:
  try:
    stackPancakes(numPancakes=int(sys.argv[1]))
  except ValueError:
    print("Input argument must be an integer")
else:
  stackPancakes()
  # other function calls you may be interested in:
  # stackPancakes(numPancakes=30)
  # stackPancakes(initialState=[7,3,4,1,2,6,5])
  # benchmark()
