# Drone.py

import math

class Drone:
    def __init__(self, x, y, max_speed, acceleration, angular_speed, max_angle, flight_time):
        self.x = x
        self.y = y
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.angular_speed = angular_speed
        self.max_angle = max_angle
        self.flight_time = flight_time
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.speed_x = 0
        self.speed_y = 0
        self.altitude = 0
        self.battery_status = flight_time

    def update_position(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def update_speed(self):
        if self.pitch != 0:
            self.speed_y = min(self.max_speed, self.speed_y + self.acceleration * 0.1 * math.sin(math.radians(self.pitch)))
        if self.roll != 0:
            self.speed_x = min(self.max_speed, self.speed_x + self.acceleration * 0.1 * math.sin(math.radians(self.roll)))
