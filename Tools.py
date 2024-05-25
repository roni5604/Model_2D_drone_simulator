import random
import math

import WorldParams
from Point import Point


class Tools:
    @staticmethod
    def get_point_by_distance(from_point, rotation, distance):
        radians = math.pi * (rotation / 180)
        i = distance / WorldParams.WorldParams.CMPerPixel
        xi = from_point.x + math.cos(radians) * i
        yi = from_point.y + math.sin(radians) * i
        return Point(xi, yi)

    @staticmethod
    def noise_between(min_value, max_value, is_negative):
        rand = random.Random()
        noise_to_distance = 1
        noise = (min_value + rand.uniform(0, 1) * (max_value - min_value)) / 100
        if not is_negative:
            return noise_to_distance + noise

        if rand.choice([True, False]):
            return noise_to_distance + noise
        else:
            return noise_to_distance - noise

    @staticmethod
    def get_rotation_between_points(from_point, to_point):
        y1 = from_point.y - to_point.y
        x1 = from_point.x - to_point.x
        radians = math.atan2(y1, x1)  # Use atan2 for correct quadrant
        rotation = radians * 180 / math.pi
        return rotation

    @staticmethod
    def get_distance_between_points(from_point, to_point):
        x1 = (from_point.x - to_point.x) ** 2
        y1 = (from_point.y - to_point.y) ** 2
        return math.sqrt(x1 + y1)

