import pygame
from pygame.version import SDLVersion

class State:
        def __init__(self) -> None:
                self.start_game = True
                
                #moving objects_moving
                self.moving = False
                self.objects_moving = None

                #menu
                self.menu = True

                #shop
                self.shop = False


class Game:
        def __init__(self, screen: pygame.surface.Surface, field_menu, field_shop, field_game) -> None:
                self.screen = screen
                self.speed = 5
                self.field_game = field_game
                self.field_menu = field_menu
                self.field_shop = field_shop
                
