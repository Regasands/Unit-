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
            self.x, self.y = 4, 4
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
    def __init__(self, image_name, key: str, level: int):
        self.key = key
        self.level = level
        if key == 0:
            if level == 0:
                self.count_money = 1
            elif level == 1:
                self.count_money = 3
            elif level == 2:
                self.count_money = 9
            elif level == 3:
                self.count_money = 20
            elif level == 4:
                self.count_money = 35
            elif level == 5:
                self.count_money = 100
            elif level == 6:
                self.count_money = 150
            elif level == 7:
                self.count_money = 300
            elif level == 8:
                self.count_money = 1000

        super().__init__(image_name)


trees = {0: "grass",
         1: "tall_grass",
         2: "berries",
         3: "birch",
         4: "spruce",
         5: "oak",
         6: "super_oak",
         7: "golden_oak"}

keys = {0: trees}
