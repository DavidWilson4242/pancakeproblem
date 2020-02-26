from pancake import stackPancakes
import pygame

class StackState:
  def __init__(self, screenSize, initialState): 
    self.states = initialState[:]
    self.positions = []
    self.sizes = []
    self.screenSize = screenSize

    rootPos = (self.screenSize[0]/2, self.screenSize[1] - 100)
    for i in range(len(self.states)):
      width = self.states[i]*20
      height = 30
      self.positions.append((rootPos[0] - width/2, rootPos[1] - i*height))
      self.sizes.append((width, height))

class Visualizer:
  def __init__(self, initialState):
    self.running = False
    self.screenSize = (600, 600)
    self.screen = pygame.display.set_mode(self.screenSize)
    self.clock = pygame.time.Clock()
    self.stackState = StackState(self.screenSize, initialState)

    self.colors = {
      "RED": (255, 0, 0),
      "GREEN": (0, 255, 0),
      "BLUE": (0, 0, 255),
      "BLACK": (0, 0, 0),
      "WHITE": (255, 255, 255)
    }

    pygame.init()

  def drawStack(self):
    state = self.stackState
    for size, pos in zip(state.sizes, state.positions):
      pygame.draw.rect(self.screen, self.colors["RED"], pos + size)

  def run(self):
    self.running = True
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
          break
  
      self.drawStack()

      self.clock.tick(60)
      pygame.display.update()


if __name__ == "__main__":
  v = Visualizer([5, 6, 4, 2, 3, 1])
  v.run()
