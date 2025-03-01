import logging
import pygame
import json
import time
import os

from pygame.rect import RectType
from enemy.base_enemy import Water
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

        # end
        self.end = False



class Music:
    pass


class Game:
    def __init__(self, screen: pygame.surface.Surface, field_menu, field_shop, field_game, field_end) -> None: 

        # logic game
        self.screen = screen
        self.field_game = field_game
        self.field_menu = field_menu
        self.field_shop = field_shop
        self.field_end = field_end

        #logic timer
        self.clock = pygame.time.Clock()
        self.update_text_time = 0
        self.update_delta_time = 1
        
        # alert logic
        self.alert: bool = False
        self.time_alert = 0
        self.text_alert = 0

        # time mob
        self.time_spawn_mob = 0.1
        self.time_mob_move = 0.1
        self.x_time_mob_move = 0.2
        self.x_time_mob_spawn = 5

        # create base alert
        self.overlay_alert: Surface = pygame.Surface((250, 30), pygame.SRCALPHA)
        self.overlay_alert.fill((0, 0, 0, 0))
        self.overlay_rect_alert: Rect = pygame.Rect(0, 0, 250, 30)

        # economic
        self.updater_state_economic = SaveData()
        self.params_economic_data = self.updater_state_economic.get_data(self.updater_state_economic.setting_updaters)
        self.money = self.params_economic_data['money']
        self.profit = self.params_economic_data['profit']
        self.max_money = self.updater_state_economic.get_only_effect('max_money', self.params_economic_data['max_money'])

        # logic for overlay
        self.overlay = pygame.Surface((400, 70), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 0))

        # basic info
        self.font = pygame.font.Font(None, 36)

        # position
        self.overlay_rect = pygame.Rect(0, 0, 400, 70)
        
        # update

        self.overlay_update = pygame.Surface((512, 200), pygame.SRCALPHA)
        self.overlay_update.fill((0, 0, 0 ,0))
        self.overlay_update_react = pygame.Rect(0, 0, 512, 200)

        # x_hard
        self.x_hard = 1


    def render(self):
        self.screen.fill((0, 0, 0))
        self.field_game.render_structures(self.screen)

    def render_text_price(self, arg2 = 255, arg1 = 255) -> None:
        # draw text
        pygame.draw.rect(self.overlay, (0, 0, 0, 0), self.overlay_rect, 0)
        text = self.font.render(f"Your money: {self.money}/{self.max_money}", True, (255, arg1, arg2))

        text_2 = self.font.render(f"Your profit: {self.profit}. Game: {self.x_hard}", True, (255, 255, 255))
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
        self.screen.blit(self.overlay_alert, (420, 10))

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

            text_1 = self.font.render(f'Upgrade {upgrade_type}. Price:  {states[1]["price"] * current_discount}', True, (255, 255, 0))
            text_2 = self.font.render(f'Current effect {states[0]["effect"]}. Next effect {states[1]["effect"]}', True, (255, 255, 0))
            text_3 = self.font.render(f'Current level: {current_level}/{8}', True, (255, 255, 0))
        pygame.draw.rect(self.overlay_update, (0, 0, 0, 0), self.overlay_update_react, 0)
        self.overlay_update.blit(text_1, (self.overlay_update_react.x + 30, self.overlay_update_react.y + 20))

        if text_2:
            self.overlay_update.blit( text_2, (self.overlay_update_react.x + 30, self.overlay_update_react.y + 60))
            self.overlay_update.blit(text_3, (self.overlay_update_react.x + 300, self.overlay_update_react.y + 150))

        self.screen.blit(self.overlay_update, (150, 300))
            
    def complite_upgrade_updates(self):

        # проверяю и делаю улучшение, если все условия соблюдены

        key = self.field_shop.get_key()
        logging.error(key)

        # получаем следующий уровень цены нашего улучшения
        price_next_level = self.updater_state_economic.get_value(key, self.params_economic_data[key])[1]
        price_next = price_next_level.get('price')

        if price_next is None:
            logging.info('Ошибка обновление бонусов или достигнут максимальный уровень')
            self.set_alert(100, 'Уже максимальный уровнь')
            return

        # получаем скидку 
        discount = self.updater_state_economic.get_only_effect('discount_shop', self.params_economic_data['discount_shop'])

        final_price = price_next * discount
        if final_price > self.money:
            self.set_alert(100, 'Не хватает денег')
            return
        
        self.money -= final_price
        new_data = self.updater_state_economic.update_data(key, self.updater_state_economic.setting_updaters)

        if key == 'max_money':
            self.max_money = price_next_level['effect']

        self.params_economic_data = new_data 

        logging.info(f'обновление закончено текущий уровень всего : {self.params_economic_data}')
        
    # самое интересное , сохранение параметров при выходе из игры
    def saves(self):
        # пока не успеваю сделать, будет дальнейшим режимом
        pass

    # мало, но приятно получаем основные параметры баффы
    def get_effect(self, name: str):
        level_effect = self.params_economic_data[name]
        return self.updater_state_economic.get_only_effect(name, level_effect)

    # обнуление игры 
    def reset_simple(self):
        self.updater_state_economic.get_reset(self.updater_state_economic.setting_updaters)
        self.params_economic_data = self.updater_state_economic.get_data(self.updater_state_economic.setting_updaters)
        self.money = self.params_economic_data['money']
        self.profit = self.params_economic_data['profit']
        self.max_money = self.updater_state_economic.get_only_effect('max_money', self.params_economic_data['max_money'])    
    
    # mob spawn and renderin
    def spawn_enemy(self):
        if time.time() > self.time_spawn_mob:
            self.field_game.create_mob()
            self.time_spawn_mob = time.time() + self.x_time_mob_spawn // self.x_hard

        if time.time() > self.time_mob_move:
            self.field_game.move_mob()
            self.time_mob_move = time.time() + self.x_time_mob_move


class SaveData:
    # test create saves
    def __init__(self) -> None:
        self.setting_updaters = 'datafile/saves.json'
        self.hard_level = 'datafiles/saves_hard.json'

    def get_data(self, name):

        if not os.path.exists(name):
            self.get_reset(name)
            logging.info('файл успешно создан')
            return self.read_json(name)

        data = self.read_json(name)

        if data:
            return data
        else:
            self.get_reset(name)
            self.read_json(name)
   
    def update_data(self, key, name):
        if not os.path.exists(name):
            return

        params = self.get_data(name)
        params[key] = params[key] + 1 if isinstance(params[key], int) else not params[key]

        with open(name, 'w', encoding='utf-8') as file:
            json.dump(params,  file, ensure_ascii=False)
        return params


    def get_value(self, key, level):
        key = key.upper()
        new_level = level + 1

        if key == 'CLICK_MOB':
            return DataEconomy.CLICK_MOB.get(level), DataEconomy.CLICK_MOB.get(new_level)
        elif key == 'X':
            return DataEconomy.X.get(level), DataEconomy.X.get(new_level)
        elif key == 'CUSTOM_X':
            return DataEconomy.CUSTOM_X.get(level), DataEconomy.CUSTOM_X.get(new_level)
        elif key == 'KEY':
            return DataEconomy.KEY.get(level), DataEconomy.KEY.get(new_level)
        elif key == 'LEVEL_UPGRADE':
            return DataEconomy.LEVEL_UPGRADE.get(level), DataEconomy.LEVEL_UPGRADE.get(new_level)
        elif key == 'MAX_MONEY':
            return DataEconomy.MAX_MONEY.get(level), DataEconomy.MAX_MONEY.get(new_level)
        elif key == 'DISCOUNT_SHOP':
            return DataEconomy.DISCOUNT_SHOP.get(level), DataEconomy.DISCOUNT_SHOP.get(new_level)

    def get_only_effect(self, key, level):
        return self.get_value(key, level)[0]['effect']
    
    def get_reset(self, name):
        with open(name, 'w', encoding='utf-8') as file:
            json.dump(DataEconomy.START_UPDATERS, file, ensure_ascii=False)

    def read_json(self, name):
        try:
            with open(name, 'r', encoding='utf-8') as file:
                return json.load(file)

        except Exception as e:
            logging.error(f'Произошла ошибка {e}')
            return False

