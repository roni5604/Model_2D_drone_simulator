# tools.py
import math
import random
from world_params import WorldParams


def get_point_by_distance(from_point, rotation, distance):
    radians = math.pi * (rotation / 180)
    distance_in_pixels = distance / WorldParams.CM_PER_PIXEL
    x = from_point[0] + math.cos(radians) * distance_in_pixels
    y = from_point[1] + math.sin(radians) * distance_in_pixels
    return (x, y)


def noise_between(min_val, max_val, is_negative):
    noise_to_distance = 1
    noise = (min_val + random.uniform(0, max_val - min_val)) / 100
    if not is_negative:
        return noise_to_distance + noise

    if random.choice([True, False]):
        return noise_to_distance + noise
    else:
        return noise_to_distance - noise


def get_rotation_between_points(from_point, to_point):
    y_diff = from_point[1] - to_point[1]
    x_diff = from_point[0] - to_point[0]
    radians = math.atan2(y_diff, x_diff)
    rotation = radians * 180 / math.pi
    return rotation


def get_distance_between_points(from_point, to_point):
    x_diff = (from_point[0] - to_point[0]) ** 2
    y_diff = (from_point[1] - to_point[1]) ** 2
    return math.sqrt(x_diff + y_diff)
