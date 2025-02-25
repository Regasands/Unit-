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
        count = size // self.cell
        self.count_x, self.count_y = count_x, count_y
        self.field: list[list[Structure | None]] = [[None] * count for _ in range(count)]
        for x in range(self.count_x): 
                for y in range(self.count_y):
                        self.field[x + key][y + key] = Base(key)

    def render_structures(self, screen):

        self.structures_sprites = pygame.sprite.Group()

        for x in range(rows):
            for y  in range(cols):
                structure = self.field[y][x]
                if structure is None:
                    continue
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(
                    structure.get_image(), self.cell)
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
        x, y = pos[x] // self.cell, pos[y] // self.cell
        return self.field[y][x]

    def replace_structure(self, target, new_value):
        coords = self.find_structure(target)
        if coords:
            x, y = coords
            self.field[y][x] = new_value
            print(f"Элемент заменён в позиции: {x}, {y}")
        else:
            print("Элемент не найден, замена невозможна")

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
        self.cell = 10
        count = size // self.cell
       #Поля
        self.field: list[list[Structure | None]] = [[None] * count for _ in range(count)]
        self.button_box = ['Start'] 
        for x in self.button_box:
            button = Button(x)
            self.field[button.y][button.x] = button
            self.field[button.y][button.x] = button

class FieldShop(Field):
    def __init__(self, size: int = 1600):
        # Размеры
        self.size = size
        self.width, self.height = size, size
        self.cell = 16
        count = size // self.cell
       
       #Поля
        self.field: list[list[Structure | None]] = [[None] * count for _ in range(count)]
        self.button_box = []
        for x in self.button_box:
            button = Button(x)
            self.field[Button.y][button.x] = button
            
