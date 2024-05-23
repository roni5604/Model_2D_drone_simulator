import pygame

class Map:
    def __init__(self, map_image_path, screen_width, screen_height):
        self.map_image = pygame.image.load(map_image_path)
        self.map_image = pygame.transform.scale(self.map_image, (screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height

    def is_walkable(self, x, y):
        if x < 0 or x >= self.screen_width or y < 0 or y >= self.screen_height:
            return False
        pixel_color = self.map_image.get_at((int(x), int(y)))
        return pixel_color == (255, 255, 255, 255)  # Check for white color
