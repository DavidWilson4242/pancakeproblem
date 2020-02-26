from pancake import stackPancakes, generateInitialState
import pygame
import time

def rangemap(x, a, b, c, d):
  return (x - a)/(b - a) * (d - c) + c

class TweenState:
  def __init__(self, startPos, endPos, totalSteps):
    self.startPos = startPos
    self.endPos = endPos
    self.atPos = startPos
    self.maxSteps = steps
    self.change = ((endPos[0] - startPos[0])/totalSteps, 
                   (endPos[1] - startPos[1])/totalSteps)
    self.steps = 0
    self.finished = False

  def step(self):
    self.steps += 1
    if self.steps == self.maxSteps:
      self.finished = True
      self.atPos = self.endPos


class StackState:
  def __init__(self, screenSize, initialState): 
    self.states = initialState[:]
    self.sizes = [None] * len(self.states)
    self.positions = [None] * len(self.states)
    self.posTweens = {}
    self.screenSize = screenSize
    self.updateDimensions()

  def updateDimensions(self):
    rootPos = (self.screenSize[0]/2, self.screenSize[1] - 100)
    for i in range(len(self.states)):
      width = self.states[i]*10
      height = 8
      self.positions[i] = (rootPos[0] - width/2, rootPos[1] - i*height)
      self.sizes[i] = (width, height)

  def flip(self, n):
    self.states = self.states[:-n] + self.states[:-n-1:-1]
    self.updateDimensions()
    

class Visualizer:
  def __init__(self, initialState):
    self.running = False
    self.done = False
    self.screenSize = (600, 600)
    self.screen = pygame.display.set_mode(self.screenSize)
    self.clock = pygame.time.Clock()
    self.stackState = StackState(self.screenSize, initialState)
    self.solution = stackPancakes(initialState=initialState, printResults=False)
    self.solindex = 0
    self.stepTime = time.time()

    self.colors = {
      "RED": (255, 0, 0),
      "GREEN": (0, 255, 0),
      "BLUE": (0, 0, 255),
      "BLACK": (0, 0, 0),
      "WHITE": (255, 255, 255)
    }

    pygame.init()

    self.drawStack()

  def drawStack(self):
    self.screen.fill(self.colors["WHITE"])
    state = self.stackState
    for size, pos, cake in zip(state.sizes, state.positions, state.states):
      color = (255 - rangemap(cake, 1, len(state.states), 0, 255), 110, rangemap(cake, 1, len(state.states), 0, 255))
      pygame.draw.rect(self.screen, color, pos + size)
    pygame.display.flip()

  def run(self):
    self.running = True
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
          break

      if not self.done and time.time() - self.stepTime > 0.25:
        self.stepTime = time.time()
        if self.solindex == len(self.solution):
          done = True
        else:
          self.stackState.flip(self.solution[self.solindex])
          self.solindex += 1
          self.drawStack()

      self.clock.tick(60)


if __name__ == "__main__":
  v = Visualizer(generateInitialState(50))
  v.run()
