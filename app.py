import pygame
from game.state_game import Game, State
from map.field import Field, FieldMenu, FieldShop
from map.texture import Button

# todo убрать этот импорт
from map.texture import grass


if __name__ == '__main__':
    pygame.init()
    size: tuple = 800, 800
    screen = pygame.display.set_mode(size)
    run = True
    field = Field()
    field_menu = FieldMenu()
    field_shop = FieldShop()
    game = Game(screen, field_menu=field_menu, field_shop=field_shop, field_game=field)
    state_engine = State()

    while state_engine.start_game:
        for event in pygame.event.get():
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
                                                pass
                                        elif struct.name == 'Upgrade':
                                                state_engine.shop = True
                                        screen.fill((0, 0, 0))
                                        continue
                                x, y = field.get_coords_by_mouse_pos(event.pos)
                                field.set_structure(None, (x, y))
                                field.set_moving_structure(struct, event.pos)
                                state_engine.objects_moving = True
                    elif event.button == 3:
                        x, y = field.get_coords_by_mouse_pos(event.pos)
                        field.set_structure(grass, (x, y))
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if state_engine.objects_moving:
                            state_engine.objects_moving = False
                            field.finish_moving()
                game.field_game.render_structures(screen)

            # МАГАЗИН
            elif state_engine.shop:
                pass

            # МЕНЮ
            elif state_engine.menu:
                game.field_menu.render_structures(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    object_ = field_menu.get_structure_by_mouse_pos(event.pos)
                    if object_ is None:
                        break
                    if object_.name == 'Start':
                        state_engine.menu = False
                        state_engine.game = True
                        screen.fill((0, 0, 0))
        pygame.display.flip()
        game.clock.tick(60)
pygame.quit()
