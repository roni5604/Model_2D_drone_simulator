import pygame
import sys
import time
from Drone import Drone
from Map import Map
from Graph import Graph
from Tools import find_safe_starting_position
from WorldParams import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MAX_SPEED, PLAYER_ACCELERATION, ANGULAR_SPEED, MAX_ANGLE, \
    FLIGHT_TIME, SAFE_DISTANCE, BUTTON_WIDTH, BUTTON_HEIGHT
from DistanceLogger import DistanceLogger


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('2D Map Navigation')

    map_obj = Map("Maps/p12.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    drone_x, drone_y = find_safe_starting_position(map_obj, SAFE_DISTANCE)
    drone = Drone(drone_x, drone_y, PLAYER_MAX_SPEED, PLAYER_ACCELERATION, ANGULAR_SPEED, MAX_ANGLE, FLIGHT_TIME)

    distance_logger = DistanceLogger(drone)

    start_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button_rect = pygame.Rect(200, SCREEN_HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)

    game_running = False
    flight_start_time = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_running:
                    if event.key == pygame.K_LEFT:
                        drone.roll = max(drone.roll - ANGULAR_SPEED * 0.1, -MAX_ANGLE)
                    elif event.key == pygame.K_RIGHT:
                        drone.roll = min(drone.roll + ANGULAR_SPEED * 0.1, MAX_ANGLE)
                    elif event.key == pygame.K_UP:
                        drone.pitch = max(drone.pitch - ANGULAR_SPEED * 0.1, -MAX_ANGLE)
                    elif event.key == pygame.K_DOWN:
                        drone.pitch = min(drone.pitch + ANGULAR_SPEED * 0.1, MAX_ANGLE)
                    elif event.key == pygame.K_w:
                        drone.yaw += ANGULAR_SPEED * 0.1
                    elif event.key == pygame.K_s:
                        drone.yaw -= ANGULAR_SPEED * 0.1
                    elif event.key == pygame.K_SPACE:
                        if drone.altitude == 0:
                            drone.altitude = 1  # Takeoff
                        else:
                            drone.altitude = 0  # Landing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    drone.x, drone.y = find_safe_starting_position(map_obj,
                                                                   SAFE_DISTANCE)  # Reset to the fixed walkable starting position
                    drone.pitch = drone.roll = drone.yaw = 0
                    drone.speed_x = drone.speed_y = 0
                    drone.altitude = 0
                    drone.battery_status = FLIGHT_TIME
                    game_running = True
                    flight_start_time = time.time()
                    distance_logger.start_logging()
                elif stop_button_rect.collidepoint(event.pos):
                    game_running = False
                    distance_logger.stop_logging()

        if game_running:
            # Update battery status
            drone.battery_status = max(0, FLIGHT_TIME - (time.time() - flight_start_time))
            if drone.battery_status == 0:
                print("Game Over: Battery depleted.")
                game_running = False
                distance_logger.stop_logging()

            # Update speed based on pitch and roll
            drone.update_speed()

            # Movement logic
            new_x = drone.x + drone.speed_x
            new_y = drone.y + drone.speed_y

            # Check if the new position is walkable and within bounds
            if not map_obj.is_walkable(new_x, new_y):
                print("Game Over: Player moved out of the map or into an unwalkable area.")
                game_running = False
                distance_logger.stop_logging()
            else:
                drone.x, drone.y = new_x, new_y

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the map and the player
        screen.blit(map_obj.map_image, map_obj.map_image.get_rect())
        Graph.draw_drone(screen, drone)

        # Draw buttons
        Graph.draw_buttons(screen, game_running, start_button_rect, stop_button_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
