import pygame

from game.state_game import Game, State
from map.field import Field, FieldMenu, FieldShop

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
            if state_engine.game:
                if state_engine.objects_moving:
                    mouse_pos = pygame.mouse.get_pos()
                    field.set_moving_pos(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 1 - левая кнопка
                        # до сюда сделать проверку кнопок чтобы спрайты не нажимались через кнопки
                        for sprite in field.get_structure_sprites():
                            if sprite.rect.collidepoint(event.pos):
                                struct = field.get_structure_by_mouse_pos(event.pos)
                                if struct == "error":
                                    continue
                                field.replace_structure(struct, None)
                                field.set_moving_structure(struct, event.pos)
                                state_engine.objects_moving = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if state_engine.objects_moving:
                            state_engine.objects_moving = False
                            field.finish_moving()
                game.render()
            elif state_engine.shop:
                pass
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