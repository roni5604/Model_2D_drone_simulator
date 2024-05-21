# lidar.py
import random
from tools import get_point_by_distance
from world_params import WorldParams
import pygame

class Lidar:
    def __init__(self, drone, degrees):
        self.drone = drone
        self.degrees = degrees
        self.current_distance = 0

    def get_distance(self):
        actual_point = self.drone.get_point_on_map()
        rotation = self.drone.rotation + self.degrees
        distance_cm = 1
        while distance_cm <= WorldParams.LIDAR_LIMIT:
            point = get_point_by_distance(actual_point, rotation, distance_cm)
            if self.drone.real_map.is_collide(int(point[0]), int(point[1])):
                break
            distance_cm += 1
        return distance_cm

    def get_simulation_distance(self):
        if random.uniform(0, 1) <= 0.05:  # 5% of the time, not getting an answer
            distance_cm = 0
        else:
            distance_cm = self.get_distance()
            distance_cm += random.randint(-WorldParams.LIDAR_NOISE, WorldParams.LIDAR_NOISE)
        self.current_distance = distance_cm
        return distance_cm

    def paint(self, screen):
        actual_point = self.drone.get_point_on_map()
        rotation = self.drone.rotation + self.degrees
        to_point = get_point_by_distance(actual_point, rotation, self.current_distance)
        pygame.draw.line(screen, (0, 255, 0), (actual_point[0], actual_point[1]), (to_point[0], to_point[1]))
