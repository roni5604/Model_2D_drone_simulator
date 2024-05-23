import pygame

class Graph:
    @staticmethod
    def draw_drone(screen, drone):
        pygame.draw.circle(screen, (0, 255, 0), [int(drone.x), int(drone.y)], 5)

    @staticmethod
    def draw_buttons(screen, game_running, start_button_rect, stop_button_rect):
        pygame.draw.rect(screen, (0, 255, 0) if game_running else (255, 255, 255), start_button_rect)
        pygame.draw.rect(screen, (255, 0, 0) if not game_running else (255, 255, 255), stop_button_rect)
        font = pygame.font.Font(None, 36)
        start_text = font.render('Start', True, (0, 0, 0))
        stop_text = font.render('Stop', True, (0, 0, 0))
        screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))
        screen.blit(stop_text, (stop_button_rect.x + 20, stop_button_rect.y + 10))
