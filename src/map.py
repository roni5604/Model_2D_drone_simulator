# map.py
import pygame
import numpy as np

class Map:
    def __init__(self, image_path, drone_start_point):
        self.image_path = image_path
        self.drone_start_point = drone_start_point
        self.map = self.load_map(image_path)

    def load_map(self, path):
        img = pygame.image.load(path)
        img_array = pygame.surfarray.array3d(img)
        map_array = np.all(img_array != 0, axis=2)
        return map_array.T  # Transpose to match the coordinates

    def is_collide(self, x, y):
        return not self.map[x, y]

    def draw(self, screen):
        for x in range(self.map.shape[0]):
            for y in range(self.map.shape[1]):
                if not self.map[x, y]:
                    screen.set_at((x, y), (0, 0, 0))
