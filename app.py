from os import stat
import pygame
from map.field import Field, FieldMenu, FieldShop
from game.state_game import Game, State

if __name__ == '__main__':
     pygame.init()
     size: tuple = 1600, 1600
     screen = pygame.display.set_mode(size)
     run = True
     field = Field(10, 10, 0)
     field_menu = FieldMenu()
     field_shop = FieldShop()
     game = Game(screen, field_menu=field_menu, field_shop=field_shop, field_game=field)
     state_engine = State()
     while state_engine.start_game:
        for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                        break
                if state_engine.menu:
                        pass
                elif state_engine.shop:
                        pass
                elif state_engine.game:
                        pass

