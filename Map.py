import pygame
from PIL import Image


class Map:
    def __init__(self, path, drone_start_point):
        self.drone_start_point = drone_start_point
        try:
            img_map = Image.open(path)
            self.map = self.render_map_from_image_to_boolean(img_map)
        except IOError as e:
            print(e)

    def render_map_from_image_to_boolean(self, map_img):
        w, h = map_img.size
        map_array = [[False for _ in range(h)] for _ in range(w)]
        for y in range(h):
            for x in range(w):
                r, g, b = map_img.getpixel((x, y))[:3]
                if r != 0 and g != 0 and b != 0:  # assuming non-black means passable
                    map_array[x][y] = True
        return map_array

    def is_collide(self, x, y):
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]):
            return not self.map[x][y]
        return True  # out of bounds is treated as collision

    def paint(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if not self.map[i][j]:
                    screen.set_at((i, j), (128, 128, 128))
