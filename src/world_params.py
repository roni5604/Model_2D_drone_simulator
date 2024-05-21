# world_params.py
class WorldParams:
    CM_PER_PIXEL = 1  # Set according to your scale
    MIN_MOTION_ACCURACY = 0.1
    MAX_MOTION_ACCURACY = 0.3
    MIN_ROTATION_ACCURACY = 0.1
    MAX_ROTATION_ACCURACY = 0.3
    ROTATION_PER_SECOND = 10  # Degrees per second
    ACCELERATE_PER_SECOND = 0.1
    MAX_SPEED = 2  # Max speed
    LIDAR_LIMIT = 100
    LIDAR_NOISE = 5
