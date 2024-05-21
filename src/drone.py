# drone.py
from tools import get_point_by_distance, noise_between
from world_params import WorldParams
from lidar import Lidar
from point import Point

class Drone:
    def __init__(self, real_map):
        self.real_map = real_map
        self.start_point = real_map.drone_start_point
        self.point_from_start = Point(0, 0)
        self.sensor_optical_flow = Point(0, 0)
        self.lidars = []
        self.rotation = 0
        self.gyro_rotation = self.rotation
        self.speed = 0.2

    def add_lidar(self, degrees):
        lidar = Lidar(self, degrees)
        self.lidars.append(lidar)

    def get_point_on_map(self):
        x = self.start_point.x + self.point_from_start.x
        y = self.start_point.y + self.point_from_start.y
        return (x, y)

    def update(self, delta_time):
        dist_moved = (self.speed * 100) * (delta_time / 1000)
        self.point_from_start = get_point_by_distance((self.point_from_start.x, self.point_from_start.y), self.rotation, dist_moved)

        noise_to_distance = noise_between(WorldParams.MIN_MOTION_ACCURACY, WorldParams.MAX_MOTION_ACCURACY, False)
        self.sensor_optical_flow = get_point_by_distance((self.sensor_optical_flow.x, self.sensor_optical_flow.y), self.rotation, dist_moved * noise_to_distance)

        noise_to_rotation = noise_between(WorldParams.MIN_ROTATION_ACCURACY, WorldParams.MAX_ROTATION_ACCURACY, False)
        self.gyro_rotation += (1 - noise_to_rotation) * delta_time / 60000
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    @staticmethod
    def format_rotation(rotation):
        rotation %= 360
        if rotation < 0:
            rotation = 360 + rotation
        return rotation

    def rotate_left(self, delta_time):
        rotation_changed = WorldParams.ROTATION_PER_SECOND * delta_time / 1000
        self.rotation += rotation_changed
        self.rotation = self.format_rotation(self.rotation)
        self.gyro_rotation += rotation_changed
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    def rotate_right(self, delta_time):
        rotation_changed = -WorldParams.ROTATION_PER_SECOND * delta_time / 1000
        self.rotation += rotation_changed
        self.rotation = self.format_rotation(self.rotation)
        self.gyro_rotation += rotation_changed
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    def speed_up(self, delta_time):
        self.speed += (WorldParams.ACCELERATE_PER_SECOND * delta_time / 1000)
        if self.speed > WorldParams.MAX_SPEED:
            self.speed = WorldParams.MAX_SPEED

    def slow_down(self, delta_time):
        self.speed -= (WorldParams.ACCELERATE_PER_SECOND * delta_time / 1000)
        if self.speed < 0:
            self.speed = 0

    def get_info_html(self):
        info = f"""
        Rotation: {self.rotation:.4f}<br>
        Location: {self.point_from_start}<br>
        GyroRotation: {self.gyro_rotation:.4f}<br>
        SensorOpticalFlow: {self.sensor_optical_flow}<br>
        """
        return info
