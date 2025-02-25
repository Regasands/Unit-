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
        self.name = name
        if name == 'Start':
            self.x, self.y = 4, 2
        elif name == 'Menu':
            self.x, self.y = -1, 0
        elif name == 'Buy':
            self.x, self.y = -1, -1
        elif name == 'Upgrade':
            self.x, self.y = -2, -1
        else:
            self.x, self.y = -1, -1
        super().__init__(name)


class Base(Structure):
    def __init__(self, key):
        super().__init__(f'base_{key}')


class Mob(Structure):
    def __init__(self, key):
        self.level = 1
        if key == 0:
            self.count_money = 100
            self.unique_id = 100

        else:
            self.count_money = 10
            self.unique_id = 10
        super().__init__(f'mob_{key}_{self.level}')

