import pygame


class State:
    def __init__(self) -> None:
        self.start_game = True

        # moving objects_moving
        self.moving = False
        self.objects_moving = None

        # menu
        self.menu = True

        # shop
        self.shop = False

        # game
        self.game = False


class Game:
    def __init__(self, screen: pygame.surface.Surface, field_menu, field_shop, field_game) -> None:
        self.screen = screen
        self.speed = 5
        self.field_game = field_game
        self.field_menu = field_menu
        self.field_shop = field_shop
        self.clock = pygame.time.Clock()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.field_game.render_structures(self.screen)

