# main.py
import pygame
import sys
from drone import Drone
from map import Map
from point import Point

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
DRONE_COLOR = (0, 0, 255)
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Drone Simulator')

# Create the map, drone, and obstacles
drone_start_point = Point(400, 300)
map_image_path = "../Maps/p12.png"  # Ensure this path is correct
real_map = Map(map_image_path, drone_start_point)
drone = Drone(real_map)
drone.add_lidar(0)
drone.add_lidar(90)
drone.add_lidar(180)
drone.add_lidar(270)

# Main loop
clock = pygame.time.Clock()

def draw_objects():
    screen.fill(BG_COLOR)
    real_map.draw(screen)
    drone_position = drone.get_point_on_map()
    pygame.draw.circle(screen, DRONE_COLOR, (int(drone_position[0]), int(drone_position[1])), 10)
    for lidar in drone.lidars:
        lidar.paint(screen)
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    delta_time = clock.get_time()
    if keys[pygame.K_UP]:
        drone.update(delta_time)
    if keys[pygame.K_DOWN]:
        drone.update(-delta_time)
    if keys[pygame.K_LEFT]:
        drone.rotate_left(delta_time)
    if keys[pygame.K_RIGHT]:
        drone.rotate_right(delta_time)
    if keys[pygame.K_w]:
        drone.speed_up(delta_time)
    if keys[pygame.K_s]:
        drone.slow_down(delta_time)

    draw_objects()
    clock.tick(FPS)
