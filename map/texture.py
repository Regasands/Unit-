from os import SEEK_CUR, supports_bytes_environ
import pygame


class Structure:
    def __init__(self,
                 image_name: str | None = None):
        if image_name:
            image_path = f"sprites/structures/{image_name}.png"
            self.image = pygame.image.load(image_path)
        else:
            self.image = None

    def get_image(self):
        return self.image


class Button(Structure):
    def __init__(self, name):
        if name = 'Menu':
            self.x, self.y = 0, 0
        else:
            self.x, self.y = -1, -1
        super.__init__(image_name)

class Base(Structure):
    def __init__(self, key):
        super().__init__(f'base_{key}')


class Mob(Structure):
    def __init__(self, image_name):
        if image_name == 'Base_0':
            self.count_money = 100
            self.unical_id = 100

        else:
            self.count_money = 10
            self.unical_id = 10
        super.__init__(image_name)
