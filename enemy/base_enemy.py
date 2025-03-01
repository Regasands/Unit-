from map.texture import *


class Enemy(Structure):
    def __init__(self, image_name: str | None = None):
        super().__init__(image_name)


class Water(Enemy):
    def __init__(self, x, y):
        image_name = 'water'
        self.x = x
        self.y = y
        super().__init__(image_name)

    def copy(self):
        return Water(self.x, self.y)
