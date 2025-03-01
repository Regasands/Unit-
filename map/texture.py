from re import S
import pygame
from PIL import Image


class AnimatedGif:
    def __init__(self, gif_path):
        self.gif_path = gif_path
        self.frames = []
        self.durations = []
        self.load_gif()
        self.active = False
        self.current_frame_index = 0
        self.last_update = 0
        self.start_time = 0
        self.rect = None
        self.fade_duration = None

    def load_gif(self):
        pil_image = Image.open(self.gif_path)
        try:
            while True:
                frame = pil_image.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_frame = pygame.image.fromstring(data, size, mode)
                self.frames.append(py_frame)
                self.durations.append(pil_image.info.get("duration", 100))
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass
        self.total_frames = len(self.frames)

    def start(self, rect, fade_duration):
        self.active = True
        self.rect = rect
        self.fade_duration = fade_duration
        self.current_frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.start_time = self.last_update

    def update(self, screen):
        if not self.active:
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        fade_factor = max(0, 1 - elapsed / self.fade_duration)
        if fade_factor == 0:
            self.active = False
            return
        if now - self.last_update >= self.durations[self.current_frame_index]:
            self.current_frame_index = (self.current_frame_index + 1) % self.total_frames
            self.last_update = now
        frame = self.frames[self.current_frame_index]
        if frame.get_size() != (self.rect.width, self.rect.height):
            frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        frame_copy = frame.copy()
        frame_copy.set_alpha(int(255 * fade_factor))
        screen.blit(frame_copy, self.rect)


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

        elif name == 'NextParam':
            self.x, self.y = 7, -3
        elif name == 'BackParam':
            self.x, self.y = 2, -3
        elif name == 'BuyParam':
            self.x, self.y = 4, -3
        elif name == 'Start2':
            self.x, self.y = -1, -1
        elif name == 'DeletUpgrade':
            self.x, self.y = -2, 0
        elif name == 'HardLevel':
            self.x, self.y = 4, 2
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
                self.count_money = 2
                self.cost =120
            elif level == 1:
                image_name = 'tall_grass'
                self.count_money = 5
                self.cost = 270
            elif level == 2:
                self.count_money = 17
                image_name = 'berries'
                self.cost = 1000
            elif level == 3:
                image_name = 'birch'
                self.count_money = 40
                self.cost = 1500
            elif level == 4:
                image_name = 'spruce'
                self.count_money = 60
                self.cost = 4000
            elif level == 5:
                image_name = 'oak'
                self.count_money = 150
                self.cost = 5000
            elif level == 6:
                image_name = 'super_oak'
                self.count_money = 300
                self.cost = 100000
            elif level == 7:
                image_name = 'golden_oak'
                self.cost = 1000000
                self.count_money = 900
            elif level == 8:
                self.count_money = 600

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
