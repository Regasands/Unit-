import math
import random
from math import ceil
import numpy
from  map.texture  import *

class Field:
    """
    Класс поля, отвечает за все объекты в игре и их рендеринг
    """
    def __init__(self,
                 count_x: int, count_y: int, key: 0, size: int = 1600):
        self.size = size
        self.width, self.height = size, size
        self.cell = 16
        self.count = size // self.cell
        self.count_x, self.count_y = count_x, count_y
        self.field: list[list[Structure | None]] = [[None] * self.count for _ in range(self.count)]
        for x in range(self.count_x): 
                for y in range(self.count_y):
                    self.field[x + key][y + key] = Base(key)

    def render_structures(self, screen):

        self.structures_sprites = pygame.sprite.Group()

        for x in range(self.count):
            for y  in range(self.count):
                structure = self.field[y][x]
                if structure is None:
                    continue
                if isinstance(structure, Button):
                    size = (200, 30)
                else:
                    size = (self.cell, self.cell)
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(
                    structure.get_image(), size) 
                sprite.rect = pygame.Rect(
                    round(x * self.cell),
                    round(y * self.cell),
                    self.cell,
                    self.cell)
                
                self.structures_sprites.add(sprite)
        self.structures_sprites.draw(screen)
    def get_structure_sprites(self):
        return self.structures_sprites

    def get_structure_by_mouse_pos(self, pos):
        x, y = pos[0] // self.cell, pos[1] // self.cell
        return self.field[y][x]

    def replace_structure(self, target, new_value):
        coords = self.find_structure(target)
        if coords:
            x, y = coords
            self.field[y][x] = new_value
            print(f"Элемент заменён в позиции: {x}, {y}")

    def find_structure(self, target):
        for y, row in enumerate(self.field):  # Перебираем строки
            if target in row:  # Если элемент есть в строке
                x = row.index(target)  # Индекс в строке
                # Я предлагаю всегда использовать (х,у) и обращаться к полю self.field[y][x], чтобы не запутаться
                return x, y
        return None  # Если не найден

    def add_structure(self,
                      structure: Structure,
                      coords: tuple[int, int]
                      ):
        self.field[coords[1]][coords[0]] = structure


class FieldMenu(Field):
    def __init__(self, size: int = 1600):
        # Размеры
        self.size = size
        self.width, self.height = size, size
        self.cell = 100
        self.count = size // self.cell
       #Поля
        self.field: list[list[Structure | None]] = [[None] * self.count for _ in range(self.count)]
        self.button_box = ['Start']
        for x in self.button_box:
            button = Button(x)
            self.field[button.y][button.x] = button
class FieldShop(Field):
    def __init__(self, size: int = 1600):
        # Размеры
        self.size = size
        self.width, self.height = size, size
        self.cell = 16
        self.count = size // self.cell
       
       #Поля
        self.field: list[list[Structure | None]] = [[None] * self.count for _ in range(self.count)]
        self.button_box = []
        for x in self.button_box:
            button = Button(x)
            self.field[Button.y][button.x] = button
            
