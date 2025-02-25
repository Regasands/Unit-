from map.texture import *
from math import ceil


class Field:
    """
    Класс поля, отвечает за все объекты в игре и их рендеринг
    """

    def __init__(self,
                 width: int = 10,
                 height: int = 10,
                 ):
        # размеры (в клетках)
        self.width, self.height = width, height

        # все эти нужны для старых функций
        self.x: float = 1
        self.y: float = 1
        self.delta_x: float = 0
        self.delta_y: float = 0
        self.cell_size: float = 80

        self.field: list[list[Structure | None]] = [[None] * self.width for _ in range(self.height)]
        self.field[0][0] = Tree()
        self.field[3][3] = Tree()

        self.structure_sprites = pygame.sprite.Group()

        self.moving_structure: Structure | None = None
        self.moving_pos: tuple[int, int] | None = None
        self.moving_original_coords: tuple[int, int] | None = None

    def render_structures(self, screen):
        screen_width, screen_height = screen.get_size()
        cell_size: int = round(self.cell_size)
        rows = ceil(screen_height / cell_size) + 1
        cols = ceil(screen_width / cell_size) + 1

        self.structure_sprites = pygame.sprite.Group()

        for row in range(rows):
            y = (ceil(self.height - self.y) + row) % self.height
            for col in range(cols):
                x = (ceil(self.width - self.x) + col) % self.width
                structure = self.field[y][x]
                if structure is None:
                    continue
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(
                    structure.get_image(), (cell_size, cell_size)
                )
                sprite.rect = pygame.Rect(
                    round((col + self.delta_x - 1) * cell_size),
                    round((row + self.delta_y - 1) * cell_size),
                    cell_size,
                    cell_size,
                )
                self.structure_sprites.add(sprite)
        self.add_moving_structure_sprite()
        self.structure_sprites.draw(screen)

    def add_moving_structure_sprite(self):  # добавляет к группе
        if self.moving_structure is None:
            return
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(
            self.moving_structure.get_image(), (self.cell_size, self.cell_size)
        )
        x, y = self.moving_pos
        sprite.rect = pygame.Rect(
            x - self.cell_size // 2,
            y - self.cell_size // 2,
            self.cell_size,
            self.cell_size,
        )
        self.structure_sprites.add(sprite)

    def get_structure_sprites(self):
        return self.structure_sprites

    def get_coords_by_mouse_pos(self, pos):
        pos_x, pos_y = pos[0] / self.cell_size, pos[1] / self.cell_size
        x, y = pos_x - self.x, pos_y - self.y
        x, y = ceil(x), ceil(y)
        return x, y

    def get_structure_by_mouse_pos(self, pos):
        x, y = self.get_coords_by_mouse_pos(pos)
        if not (0 <= x < self.width and 0 <= y < self.height):
            return "error"
        return self.field[y][x]

    def replace_structure(self, target, new_value):
        coords = self.get_structure(target)
        if coords:
            x, y = coords
            self.field[y][x] = new_value
            print(f"Элемент заменён в позиции: {x}, {y}")
        else:
            print("Элемент не найден, замена невозможна")

    def get_structure(self, target):
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

    def set_moving_structure(self, structure: tuple[int, int] | None, pos: tuple[int, int] | None = None):
        self.moving_structure = structure
        self.moving_pos = pos
        if pos is not None:
            self.moving_original_coords = self.get_coords_by_mouse_pos(pos)
        else:
            self.moving_original_coords = None

    def set_moving_pos(self, pos: tuple[int, int]):
        self.moving_pos = pos

    def finish_moving(self):
        structure = self.get_structure_by_mouse_pos(self.moving_pos)
        if structure is not None or structure == "error":
            x, y = self.moving_original_coords
            self.field[y][x] = self.moving_structure
            self.set_moving_structure(None)
        else:
            x, y = self.get_coords_by_mouse_pos(self.moving_pos)
            self.field[y][x] = self.moving_structure
            self.set_moving_structure(None)



class FieldMenu(Field):
    def __init__(self,
                 width: int = 10,
                 height: int = 10):
        super().__init__(width, height)
        self.field: list[list[Structure | None]] = [[None] * self.width for _ in range(self.height)]
        self.button_box = ['Start']
        for x in self.button_box:
            button = Button(x)
            self.field[button.y][button.x] = button
            self.field[button.y][button.x] = button


class FieldShop(Field):
    def __init__(self,
                 width: int = 10,
                 height: int = 10):
        super().__init__(width, height)
        self.field: list[list[Structure | None]] = [[None] * self.width for _ in range(self.height)]
        self.button_box = []
        for x in self.button_box:
            button = Button(x)
            self.field[Button.y][button.x] = button
