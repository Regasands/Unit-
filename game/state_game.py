from logging import addLevelName
import logging
import re
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
        # logic game
        self.screen = screen
        self.field_game = field_game
        self.field_menu = field_menu
        self.field_shop = field_shop

        #logic timer
        self.clock = pygame.time.Clock()
        self.update_text_time = 0
        
        # alert logic
        self.alert: bool = False
        self.time_alert = 0
        self.text_alert = 0

        self.overlay_alert: Surface = pygame.Surface((250, 30))
        self.overlay_alert.fill((0, 0, 0, 0))
        self.overlay_rect_alert: Rect = pygame.Rect(0, 0, 250, 30)

        # economic
        self.money = 100
        self.profit = 1

        # logic for overlay
        self.overlay = pygame.Surface((300, 70))
        self.overlay.fill((0, 0, 0, 0))

        # basic info
        self.font = pygame.font.Font(None, 36)

        # position
        self.overlay_rect = pygame.Rect(0, 0, 300, 70)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.field_game.render_structures(self.screen)

    def render_text_price(self) -> None:
        # check time
        self.update_text_time += 1 
        if self.update_text_time > 100:
            self.update_price_and_money()
            self.update_text_time = 0

        # draw text
        pygame.draw.rect(self.overlay, (0, 0, 0, 0), self.overlay_rect, 0)
        text = self.font.render(f"Your money: {self.money}", True, (255, 255, 255))

        text_2 = self.font.render(f"Your profit: {self.profit}", True, (255, 255, 255))
        self.overlay.blit(text_2, (self.overlay_rect.x + 20, self.overlay_rect.y + 30))
        self.overlay.blit(text, (self.overlay_rect.x + 20, self.overlay_rect.y + 5))
        self.screen.blit(self.overlay, (10, 10))

    def update_price_and_money(self):
        start_point = 1
        for list_ in self.field_game.field:
            for elem in list_:
                if isinstance(elem, Mob):
                    start_point += elem.count_money

        self.profit = start_point
        self.money += self.profit

    # пробновая версия алертов
    def set_alert(self, time, text):
        if self.alert:
            return
        self.alert = True
        self.text_alert = text
        self.time_alert = time

    def render_text_alert(self):
        if not self.alert:
            return
        self.time_alert -= 1
        if self.time_alert <= 0:
            self.alert = False
        pygame.draw.rect(self.overlay_alert, (0, 0, 0, 0), self.overlay_rect_alert, 0)
        text = self.font.render(f'{self.text_alert}', True, (255, 0, 0))
        self.overlay_alert.blit(text, (self.overlay_rect_alert.x + 10, self.overlay_rect_alert.y + 5))
        self.screen.blit(self.overlay_alert, (300, 10))





