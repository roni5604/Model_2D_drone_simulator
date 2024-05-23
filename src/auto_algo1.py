# auto_algo1.py
import random
import pygame
from point import Point
from tools import get_point_by_distance, get_distance_between_points
from world_params import WorldParams
from drone import Drone
from lidar import Lidar

class AutoAlgo1:
    class PixelState:
        BLOCKED = 'blocked'
        EXPLORED = 'explored'
        UNEXPLORED = 'unexplored'
        VISITED = 'visited'

    def __init__(self, real_map):
        self.map_size = 3000
        self.map = []
        self.degrees_left = []
        self.degrees_left_func = []
        self.points = []
        self.is_rotating = 0
        self.is_speed_up = False
        self.drone = Drone(real_map)
        self.drone.add_lidar(0)
        self.drone.add_lidar(90)
        self.drone.add_lidar(-90)
        self.init_map()
        self.ai_cpu = pygame.time.Clock()
        self.is_init = True
        self.last_front_lidar_dis = 0
        self.is_rotate_right = False
        self.changed_right = 0
        self.changed_left = 0
        self.try_to_escape = False
        self.left_or_right = 1
        self.max_rotation_to_direction = 20
        self.is_finish = True
        self.is_left_right_rotation_enable = True
        self.is_risky = False
        self.max_risky_distance = 150
        self.try_to_escape = False
        self.risky_dis = 0
        self.max_angle_risky = 10
        self.is_lidars_max = False
        self.save_point_after_seconds = 3
        self.max_distance_between_points = 100
        self.start_return_home = False
        self.init_point = Point()
        self.counter = 0
        self.last_gyro_rotation = 0

    def init_map(self):
        self.map = [[self.PixelState.UNEXPLORED for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.drone_starting_point = Point(self.map_size / 2, self.map_size / 2)

    def play(self):
        self.drone.play()
        self.ai_cpu.tick(60)  # Run at 60 FPS

    def update(self, delta_time):
        self.update_visited()
        self.update_map_by_lidars()
        self.ai(delta_time)

        if self.is_rotating != 0:
            self.update_rotating(delta_time)
        if self.is_speed_up:
            self.drone.speed_up(delta_time)
        else:
            self.drone.slow_down(delta_time)

    def speed_up(self):
        self.is_speed_up = True

    def speed_down(self):
        self.is_speed_up = False

    def update_map_by_lidars(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)

        for lidar in self.drone.lidars:
            rotation = self.drone.get_gyro_rotation() + lidar.degrees
            for distance_in_cm in range(int(lidar.current_distance)):
                p = get_point_by_distance(from_point, rotation, distance_in_cm)
                self.set_pixel(p.x, p.y, self.PixelState.EXPLORED)

            if lidar.current_distance > 0 and lidar.current_distance < WorldParams.LIDAR_LIMIT - WorldParams.LIDAR_NOISE:
                p = get_point_by_distance(from_point, rotation, lidar.current_distance)
                self.set_pixel(p.x, p.y, self.PixelState.BLOCKED)

    def update_visited(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        self.set_pixel(from_point.x, from_point.y, self.PixelState.VISITED)

    def set_pixel(self, x, y, state):
        xi = int(x)
        yi = int(y)
        if state == self.PixelState.VISITED:
            self.map[xi][yi] = state
            return
        if self.map[xi][yi] == self.PixelState.UNEXPLORED:
            self.map[xi][yi] = state

    def paint_blind_map(self, screen):
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.map[i][j] != self.PixelState.UNEXPLORED:
                    if self.map[i][j] == self.PixelState.BLOCKED:
                        color = (255, 0, 0)
                    elif self.map[i][j] == self.PixelState.EXPLORED:
                        color = (255, 255, 0)
                    elif self.map[i][j] == self.PixelState.VISITED:
                        color = (0, 0, 255)
                    screen.set_at((i, j), color)

    def paint_points(self, screen):
        for p in self.points:
            pygame.draw.circle(screen, (0, 255, 0), (int(p.x + self.drone.start_point.x), int(p.y + self.drone.start_point.y)), 5)

    def paint(self, screen):
        if SimulationWindow.toogle_real_map:
            self.drone.real_map.draw(screen)
        self.paint_blind_map(screen)
        self.paint_points(screen)
        self.drone.paint(screen)

    def ai(self, delta_time):
        if not SimulationWindow.toogle_ai:
            return

        if self.is_init:
            self.speed_up()
            drone_point = self.drone.get_optical_sensor_location()
            self.init_point = Point(drone_point.x, drone_point.y)
            self.points.append(drone_point)
            self.is_init = False

        if self.is_left_right_rotation_enable:
            self.do_left_right()

        drone_point = self.drone.get_optical_sensor_location()
        if SimulationWindow.return_home:
            if get_distance_between_points(self.get_last_point(), drone_point) < self.max_distance_between_points:
                if len(self.points) <= 1 and get_distance_between_points(self.get_last_point(), drone_point) < self.max_distance_between_points / 5:
                    self.speed_down()
                else:
                    self.remove_last_point()
        else:
            if get_distance_between_points(self.get_last_point(), drone_point) >= self.max_distance_between_points:
                self.points.append(drone_point)

        if not self.is_risky:
            lidar = self.drone.lidars[0]
            if lidar.current_distance <= self.max_risky_distance:
                self.is_risky = True
                self.risky_dis = lidar.current_distance
            lidar1 = self.drone.lidars[1]
            if lidar1.current_distance <= self.max_risky_distance / 3:
                self.is_risky = True
            lidar2 = self.drone.lidars[2]
            if lidar2.current_distance <= self.max_risky_distance / 3:
                self.is_risky = True
        else:
            if not self.try_to_escape:
                self.try_to_escape = True
                lidar1 = self.drone.lidars[1]
                a = lidar1.current_distance
                lidar2 = self.drone.lidars[2]
                b = lidar2.current_distance
                spin_by = self.max_angle_risky

                if a > 270 and b > 270:
                    self.is_lidars_max = True
                    l1 = get_point_by_distance(drone_point, lidar1.degrees + self.drone.get_gyro_rotation(), lidar1.current_distance)
                    l2 = get_point_by_distance(drone_point, lidar2.degrees + self.drone.get_gyro_rotation(), lidar2.current_distance)
                    last_point = self.get_avg_last_point()
                    dis_to_lidar1 = get_distance_between_points(last_point, l1)
                    dis_to_lidar2 = get_distance_between_points(last_point, l2)
                    spin_by = 90
                    if dis_to_lidar1 < dis_to_lidar2:
                        spin_by *= -1
                else:
                    if a < b:
                        spin_by *= -1

                self.spin_by(spin_by, True, self.end_risk)

    def end_risk(self):
        self.try_to_escape = False
        self.is_risky = False

    def do_left_right(self):
        if self.is_finish:
            self.left_or_right *= -1
            self.counter += 1
            self.is_finish = False
            self.spin_by(self.max_rotation_to_direction * self.left_or_right, False, self.end_left_right_rotation)

    def end_left_right_rotation(self):
        self.is_finish = True

    def update_rotating(self, delta_time):
        if len(self.degrees_left) == 0:
            return

        degrees_left_to_rotate = self.degrees_left[0]
        is_left = degrees_left_to_rotate > 0
        curr = self.drone.get_gyro_rotation()
        just_rotated = 0

        if is_left:
            just_rotated = curr - self.last_gyro_rotation
            if just_rotated > 0:
                just_rotated = -(360 - just_rotated)
        else:
            just_rotated = curr - self.last_gyro_rotation
            if just_rotated < 0:
                just_rotated = 360 + just_rotated

        self.last_gyro_rotation = curr
        degrees_left_to_rotate -= just_rotated
        self.degrees_left[0] = degrees_left_to_rotate

        if (is_left and degrees_left_to_rotate >= 0) or (not is_left and degrees_left_to_rotate <= 0):
            self.degrees_left.pop(0)
            func = self.degrees_left_func.pop(0)
            if func:
                func()
            if len(self.degrees_left) == 0:
                self.is_rotating = 0
            return

        direction = 1 if degrees_left_to_rotate > 0 else -1
        self.drone.rotate_left(delta_time * direction)

    def spin_by(self, degrees, is_first, func=None):
        self.last_gyro_rotation = self.drone.get_gyro_rotation()
        if is_first:
            self.degrees_left.insert(0, degrees)
            self.degrees_left_func.insert(0, func)
        else:
            self.degrees_left.append(degrees)
            self.degrees_left_func.append(func)
        self.is_rotating = 1

    def get_last_point(self):
        if len(self.points) == 0:
            return self.init_point
        return self.points[-1]

    def remove_last_point(self):
        if len(self.points) == 0:
            return self.init_point
        return self.points.pop()

    def get_avg_last_point(self):
        if len(self.points) < 2:
            return self.init_point
        p1 = self.points[-1]
        p2 = self.points[-2]
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
