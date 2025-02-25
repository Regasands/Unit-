from os import stat
from re import purge
from numpy import ptp
import pygame
from map.field import Field, FieldMenu, FieldShop
from game.state_game import Game, State

if __name__ == '__main__':
     pygame.init()
     size: tuple = 800, 800
     screen = pygame.display.set_mode(size)
     run = True
     field = Field(10, 10, 0, size = 800)
     field_menu = FieldMenu(size = 800)
     field_shop = FieldShop(size = 800)
     game = Game(screen, field_menu=field_menu, field_shop=field_shop, field_game=field)
     state_engine = State()
     while state_engine.start_game:
        for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                        state_engine.start_game  =  False
                if state_engine.menu:
                        game.field_menu.render_structures(screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                object_ = field_menu.get_structure_by_mouse_pos(event.pos)
                                if object_ is None:
                                        break
                                if object_.name == 'Start':
                                        state_engine.menu  = False
                                        state_engine.game = True
                                        screen.fill((0, 0, 0))
                elif state_engine.shop:
                        pass
                elif state_engine.game:
                        game.field_game.render_structures(screen)
        pygame.display.flip()
        game.clock.tick(60)
pygame.quit()

