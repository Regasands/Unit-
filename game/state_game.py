from logging import addLevelName, disable
import logging
import re
from sys import pycache_prefix
import pygame
import json
import time
import os
from pygame.rect import RectType
from map.texture import Mob
from datafile.config import DataEconomy


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
        self.update_delta_time = 1
        
        # alert logic
        self.alert: bool = False
        self.time_alert = 0
        self.text_alert = 0

        self.overlay_alert: Surface = pygame.Surface((250, 30))
        self.overlay_alert.fill((0, 0, 0, 0))
        self.overlay_rect_alert: Rect = pygame.Rect(0, 0, 250, 30)

        # economic
        self.updater_state_economic = SaveData()
        self.params_economic_data = self.updater_state_economic.get_data(self.updater_state_economic.setting_updaters)
        self.money = self.params_economic_data['money']
        self.profit = self.params_economic_data['profit']
        self.max_money = self.updater_state_economic.get_only_effect(
                'max_money', self.params_economic_data['max_money'])

        # logic for overlay
        self.overlay = pygame.Surface((300, 70))
        self.overlay.fill((0, 0, 0, 0))

        # basic info
        self.font = pygame.font.Font(None, 36)

        # position
        self.overlay_rect = pygame.Rect(0, 0, 300, 70)
        
        # update

        self.overlay_update = pygame.Surface((512, 256))
        self.overlay_update.fill((0, 0, 0 ,0))
        self.overlay_update_react = pygame.Rect(0, 0, 512, 256)


    def render(self):
        self.screen.fill((0, 0, 0))
        self.field_game.render_structures(self.screen)

    def render_text_price(self) -> None:
        # draw text
        pygame.draw.rect(self.overlay, (0, 0, 0, 0), self.overlay_rect, 0)
        text = self.font.render(f"Your money: {self.money}/{self.max_money}", True, (255, 255, 255))

        text_2 = self.font.render(f"Your profit: {self.profit}", True, (255, 255, 255))
        self.overlay.blit(text_2, (self.overlay_rect.x + 20, self.overlay_rect.y + 30))
        self.overlay.blit(text, (self.overlay_rect.x + 20, self.overlay_rect.y + 5))
        self.screen.blit(self.overlay, (10, 10))

    def update_price_and_money(self):
        # check time
        if self.update_text_time > time.time():
            return
        self.update_text_time = time.time() + self.update_delta_time

        start_point = 1
        for list_ in self.field_game.field:
            for elem in list_:
                if isinstance(elem, Mob):
                    start_point += elem.count_money

        self.profit = start_point
        self.money += self.profit
        if self.money >= self.max_money:
            self.money = self.max_money

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

    def render_update_inforamtion(self):

        # рендерю информацию об улучшении, на этом уровне не провожу само улучшение
        
        upgrade_type = self.field_shop.get_key()
        current_level = self.params_economic_data[upgrade_type]
        states = self.updater_state_economic.get_value(upgrade_type, current_level)
        if current_level == 8:
            text_1 = self.font.render(f'You have max level. Current effect - {self.states[0]["effect"]}. Level - 8', True, (255, 255, 0))
            text_2 = False
        else:

            current_discount =self.updater_state_economic.get_only_effect('discount_shop', self.params_economic_data['discount_shop'])

            text_1 = self.font.render(f'Upgrade {key} for {states[1]["price"] * current_discount}. Upgrade level -- {current_level + 1}', True, (255, 255, 0))
            text_2 = self.font.render(f'Current effect {states[0]["effect"]}. Next effect {states[1]["effect"]}', True, (255, 255, 0))

        self.overlay_update.blit(text_1, (self.overlay_update_react.x + 5, self.overlay_update_react.y + 5))

        if text_2:
            self.overlay_update.blit( text_2, (self.overlay_update_react.x + 5, self.overlay_update_react.y + 40))
        self.screen.blit(self.overlay_update, (50, 60))

    def complite_upgrade_updates(self):

        # проверяю и делаю улучшение, если все условия соблюдены

        key = self.field_shop.get_key()
        
        # получаем следующий уровень цены нашего вопроса
        price_next_level = self.updater_state_economic.get_value(key, self.params_economic_data[key])[1]
        price_next = price_next_level.get('price')
        if price_next is None:
            logging.info('Ошибка обновление бонусов или достигнут максимальный уровень')
            self.set_alert(100, 'Уже максимальный уровнь')
            return
        # получаем скидку 
        dicount = self.updater_state_economic.get_only_effect('discount_shop', self.params_economic_data['discount_shop'])

        final_price = price_next * discount
        if final_price > self.money:
            self.set_alert(100, 'Не хватает денег')
            return
        
        self.money -= final_price
        self.updater_state_economic.update_data(key, self.updater_state_economic.setting_updaters)

        logging.info(f'обновление закончено текущий уровень всего : {self.params_economic_data}')



class SaveData:
    # test create saves
    def __init__(self) -> None:
        self.setting_updaters = 'datafile/saves.json'
        self.data_ds = {}

    def get_data(self, name):
        if not os.path.exists(name):
            with open(name, 'w', encoding='utf-8') as file:
                json.dump(DataEconomy.START_UPDATERS, file, ensure_ascii=False)
                logging.info('файл успешно создан')

                return DataEconomy.START_UPDATERS
        try:
            with open(name, 'r', encoding='utf-8') as file:

                data =  json.load(file)
                logging.info('файл успешно прочитан')
                return data
        except Exception as e:
            logging.error(f'произошла ошибка {e}')
            with open(name, 'w', encoding='utf-8') as file:
                json.dump(DataEconomy.START_UPDATERS, file, ensure_ascii=False)
                logging.info('Файл создан, переходим к чтению')

            with open(name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logging.info(f'{data}, файл прочитан')
                return data

    def update_data(self, key, name):
        if not os.path.exists(name):
            return

        params = self.get_data(name)
        params[key] = params[key] + 1 if isinstance(params[key], int) else not params[key]

        with open(name, 'w', encoding='utf-8') as file:
            json.dump(DataEconomy.START_UPDATERS, file, ensure_ascii=False)


    def get_value(self, key, level):
        key = key.upper()
        if key == 'CLICK_MOB':
            return DataEconomy.CLICK_MOB.get(level), DataEconomy.CLICK_MOB.get(level + 1)
        elif key == 'X':
            return DataEconomy.X.get(level), DataEconomy.X.get(level+ 1)
        elif key == 'CUSTOM_X':
            return DataEconomy.CUSTOM_X.get(level), DataEconomy.CUSTOM_X.get(level + 1)
        elif key == 'KEY':
            return DataEconomy.KEY.get(level), DataEconomy.KEY.get(level + 1)
        elif key == 'LEVEL_UPGRADE':
            return DataEconomy.LEVEL_UPGRADE.get(level), DataEconomy.LEVEL_UPGRADE.get(level + 1)
        elif key == 'MAX_MONEY':
            return DataEconomy.MAX_MONEY.get(level), DataEconomy.MAX_MONEY.get(level+ 1)
        elif key == 'DISCOUNT_SHOP':
            return DataEconomy.DISCOUNT_SHOP.get(level), DataEconomy.DISCOUNT_SHOP.get(level + 1)

    def get_only_effect(self, key, level):
        return self.get_value(key, level)[0]['effect']

