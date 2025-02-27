import logging
import re
import pygame
from game.state_game import Game, State
from map.field import Field, FieldMenu, FieldShop
from map.texture import Button, Mob


if __name__ == '__main__':
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]  %(lineno)d %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
    )
    logging.info("Приложение запущено")

    pygame.init()
    size: tuple = 800, 800
    screen = pygame.display.set_mode(size)
    # создание основных поле
    field = Field()
    field_menu = FieldMenu()
    field_shop = FieldShop()
    game = Game(screen, field_menu=field_menu, field_shop=field_shop, field_game=field)
    state_engine = State()

    background = pygame.image.load("sprites/background.png")
    background = pygame.transform.scale(background, (800, 800))

    while state_engine.start_game:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            if event.type == pygame.QUIT:
                state_engine.start_game = False
                break

            # ИГРА
            if state_engine.game:
                if state_engine.objects_moving:
                    mouse_pos = pygame.mouse.get_pos()
                    field.set_moving_pos(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for sprite in field.get_structure_sprites():
                            if sprite.rect.collidepoint(event.pos):
                                struct = field.get_structure_by_mouse_pos(event.pos)
                                if struct == "error":
                                    continue
                                if isinstance(struct, Button):
                                        state_engine.game = False
                                        if struct.name == 'Menu':
                                                state_engine.menu = True
                                        elif struct.name == 'Buy':
                                                x, y = game.field_game.get_index_objects(None)
                                                if x == 'full':
                                                        game.set_alert(50, 'Full field')
                                                elif game.money >= 10:
                                                        game.money -= 10
                                                        game.field_game.field[y][x] = Mob('grass', 0, 0)
                                                else:
                                                        game.set_alert(50, 'Need more money')
                                                state_engine.game = True
                                        elif struct.name == 'Upgrade':
                                                state_engine.shop = True
                                        continue
                                x, y = field.get_coords_by_mouse_pos(event.pos)
                                field.set_structure(None, (x, y))
                                field.set_moving_structure(struct, event.pos)
                                state_engine.objects_moving = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if state_engine.objects_moving:
                            state_engine.objects_moving = False
                            field.finish_moving()
            # магазин улучшений `
            elif state_engine.shop:
                game.field_shop.render_structures(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                        object_ = field_shop.get_structure_by_mouse_pos(event.pos)
                        for sprite in field_menu.get_structure_sprites():
                                if sprite.rect.collidepoint(event.pos):
                                        structure = game.field_shop.get_structure_by_mouse_pos(event.pos)
                                        if not isinstance(structure, Button):
                                                break
                                        if structure.name == 'Menu':
                                                pass
                                        elif structure.name == 'Start':
                                                pass
                                        elif structure.name == 'BuyParam':
                                                logging.info('Пошло обновление')
                                                game.complite_upgrade_updates() 
                                        elif structure.name == 'NextParam':
                                                pass
                                        elif structure.name == 'BackParam':
                                                pass
            # МЕНЮ
            elif state_engine.menu:
                game.field_menu.render_structures(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    object_ = field_menu.get_structure_by_mouse_pos(event.pos)
                    for sprite in field_menu.get_structure_sprites():
                        if sprite.rect.collidepoint(event.pos):
                            state_engine.menu = False
                            state_engine.game = True

        if state_engine.game:
            game.render_text_price()
            game.update_price_and_money()
            game.field_game.render_structures(screen)

        elif state_engine.shop:
                game.field_shop.render_structures(screen)
                game.render_update_inforamtion()
            # game.field_game.render_animations(screen)
        game.render_text_alert()
        pygame.display.flip()
        game.clock.tick(100)
pygame.quit()
