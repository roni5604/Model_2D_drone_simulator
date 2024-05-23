import pygame
import sys
import time
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_RADIUS = 5  # Radius of the player point
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
PLAYER_MAX_SPEED = 0.3  # meters per second, reduced speed
PLAYER_ACCELERATION = 0.1  # meters per second^2, reduced acceleration
ANGULAR_SPEED = 100  # degrees per second
MAX_ANGLE = 10  # degrees
FLIGHT_TIME = 480  # seconds
SAFE_DISTANCE = 20  # Distance from the black area

# Load and scale the map image to fit the screen
map_image = pygame.image.load("../Maps/p12.png")  # Updated image path
map_image = pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
map_rect = map_image.get_rect()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Map Navigation')


# Function to check if the player is in a walkable area
def is_walkable(x, y):
    if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
        return False
    pixel_color = map_image.get_at((int(x), int(y)))
    return pixel_color == (255, 255, 255, 255)  # Check for white color


# Function to check if the position is safe (at least SAFE_DISTANCE away from unwalkable area)
def is_safe_position(x, y):
    for dx in range(-SAFE_DISTANCE, SAFE_DISTANCE + 1):
        for dy in range(-SAFE_DISTANCE, SAFE_DISTANCE + 1):
            if not is_walkable(x + dx, y + dy):
                return False
    return True


# Fixed walkable starting position with a safe distance from black area
def find_fixed_walkable_position():
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if is_walkable(x, y) and is_safe_position(x, y):
                return [x, y]
    return [0, 0]  # Default position if no walkable area is found


# Initial player position
player_pos = find_fixed_walkable_position()  # Find a fixed walkable starting position

# Drone state variables
movement_direction = None
pitch = 0  # Forward angle
roll = 0  # Side angle
yaw = 0  # Angular velocity
speed_x = 0  # Velocity in x direction
speed_y = 0  # Velocity in y direction
altitude = 0  # Altitude
battery_status = FLIGHT_TIME  # Battery status in seconds

# Game state
game_running = False
flight_start_time = None

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Button positions
start_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)
stop_button_rect = pygame.Rect(200, SCREEN_HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)


# Function to draw buttons
def draw_buttons():
    pygame.draw.rect(screen, GREEN if game_running else WHITE, start_button_rect)
    pygame.draw.rect(screen, RED if not game_running else WHITE, stop_button_rect)
    font = pygame.font.Font(None, 36)
    start_text = font.render('Start', True, BLACK)
    stop_text = font.render('Stop', True, BLACK)
    screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))
    screen.blit(stop_text, (stop_button_rect.x + 20, stop_button_rect.y + 10))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_running:
                if event.key == pygame.K_LEFT:
                    roll = max(roll - ANGULAR_SPEED * 0.1, -MAX_ANGLE)
                elif event.key == pygame.K_RIGHT:
                    roll = min(roll + ANGULAR_SPEED * 0.1, MAX_ANGLE)
                elif event.key == pygame.K_UP:
                    pitch = max(pitch - ANGULAR_SPEED * 0.1, -MAX_ANGLE)
                elif event.key == pygame.K_DOWN:
                    pitch = min(pitch + ANGULAR_SPEED * 0.1, MAX_ANGLE)
                elif event.key == pygame.K_w:
                    yaw += ANGULAR_SPEED * 0.1
                elif event.key == pygame.K_s:
                    yaw -= ANGULAR_SPEED * 0.1
                elif event.key == pygame.K_SPACE:
                    if altitude == 0:
                        altitude = 1  # Takeoff
                    else:
                        altitude = 0  # Landing
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                player_pos = find_fixed_walkable_position()  # Reset to the fixed walkable starting position
                pitch = roll = yaw = 0
                speed_x = speed_y = 0
                altitude = 0
                battery_status = FLIGHT_TIME
                movement_direction = None  # Reset movement direction
                game_running = True
                flight_start_time = time.time()
            elif stop_button_rect.collidepoint(event.pos):
                game_running = False

    if game_running:
        # Update battery status
        battery_status = max(0, FLIGHT_TIME - (time.time() - flight_start_time))
        if battery_status == 0:
            print("Game Over: Battery depleted.")
            game_running = False

        # Update speed based on pitch and roll
        if pitch != 0:
            speed_y = min(PLAYER_MAX_SPEED, speed_y + PLAYER_ACCELERATION * 0.1 * math.sin(math.radians(pitch)))
        if roll != 0:
            speed_x = min(PLAYER_MAX_SPEED, speed_x + PLAYER_ACCELERATION * 0.1 * math.sin(math.radians(roll)))

        # Movement logic
        new_x = player_pos[0] + speed_x
        new_y = player_pos[1] + speed_y

        # Check if the new position is walkable and within bounds
        if not is_walkable(new_x, new_y):
            print("Game Over: Player moved out of the map or into an unwalkable area.")
            game_running = False
        else:
            player_pos = [new_x, new_y]

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map and the player
    screen.blit(map_image, map_rect)
    pygame.draw.circle(screen, (0, 255, 0), [int(player_pos[0]), int(player_pos[1])], PLAYER_RADIUS)

    # Draw buttons
    draw_buttons()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
