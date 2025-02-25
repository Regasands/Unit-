from math import e
from os import stat
from typing import overload
import pygame

from map.texture import Mob


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
        self.money = 100
        self.profit = 1 / 60
        # logic for overlay
        self.overlay = pygame.Surface((300, 70))
        self.overlay.fill((0, 0, 0, 0))
        # basic info
        self.font  = pygame.font.Font(None, 36)
        # position
        self.overlay_rect = pygame.Rect(0, 0, 300, 70)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.field_game.render_structures(self.screen)

    def render_text(self) -> None:
        self.update_price_and_money()
        pygame.draw.rect(self.overlay, (0, 0, 0, 0), self.overlay_rect, 0)
        text = self.font.render(f"Your money: {self.money}", True, (255, 255, 255))

        text_2 = self.font.render(f"Your profit: {self.profit}", True, (255, 255, 255))
        self.overlay.blit(text_2, (self.overlay_rect.x + 20, self.overlay_rect.y + 25))
        self.overlay.blit(text, (self.overlay_rect.x + 20, self.overlay_rect.y + 5))
        self.screen.blit(self.overlay, (10, 10))

    def update_price_and_money(self):
        start_point = 1
        for elem in self.field_game.field:
            if isinstance(elem, Mob):
                start_point += elem.count_money

        self.profit = start_point
        self.money += self.profit / 60
