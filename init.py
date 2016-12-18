import pygame, sys,os
from pygame.locals import *
pygame.init()
# utworzenie okna
window = pygame.display.set_mode((640, 400))

def input(events):
   for event in events:
      if event.type == QUIT:
         sys.exit(0)
      else:
         print(event)

# działaj aż do przerwania
while True:
   input(pygame.event.get())