import math

class AutoAlgo:
    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    @staticmethod
    def calculate_sensor_distances(x, y, angle, speed):
        # Example sensor calculations
        forward_distance = x + speed * math.cos(math.radians(angle))
        backward_distance = x - speed * math.cos(math.radians(angle))
        right_distance = y + speed * math.sin(math.radians(angle))
        left_distance = y - speed * math.sin(math.radians(angle))
        return forward_distance, backward_distance, right_distance, left_distance
