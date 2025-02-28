from  map.texture import *

class Enemy(Structure):
        def __init__(self, image_name: str | None = None):
                self.speed = 5
                super().__init__(image_name)


class Stone(Enemy):
        def __init__(self, x , y):
                image_name = 'stone'
                self.is_move = True
                self.x = x
                self.y = y
                super().__init__(image_name)
