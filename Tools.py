def find_safe_starting_position(map_obj, safe_distance):
    for y in range(map_obj.screen_height):
        for x in range(map_obj.screen_width):
            if map_obj.is_walkable(x, y) and is_safe_position(map_obj, x, y, safe_distance):
                return x, y
    return 0, 0

def is_safe_position(map_obj, x, y, safe_distance):
    for dx in range(-safe_distance, safe_distance + 1):
        for dy in range(-safe_distance, safe_distance + 1):
            if not map_obj.is_walkable(x + dx, y + dy):
                return False
    return True
