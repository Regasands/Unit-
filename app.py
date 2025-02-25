import pygame
from map.field import Field


if __name__ == '__main__':
     pygame.init()
     size: tuple = 1600, 1600
     screen = pygame.display.set_mode(size)
     run = True
     field = Field(10, 10, 0)
     while run:
        for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                        break
                

