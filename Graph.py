import pygame
import random


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.positions = {}

    def add_vertex(self, name):
        last_vertex = self.nodes[-1] if self.nodes else None
        self.nodes.append(name)
        if last_vertex is not None:
            self.add_edge(last_vertex, name)
        self.positions[name] = (random.randint(50, 450), random.randint(50, 450))

    def add_edge(self, v1, v2):
        self.edges.append((v1, v2))

    def get_graph(self):
        return self.nodes, self.edges

    def get_output(self):
        return str(self.nodes)

    def draw_graph(self, screen):
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(screen, (0, 0, 0), self.positions[edge[0]], self.positions[edge[1]], 2)

        # Draw nodes
        for node in self.nodes:
            pygame.draw.circle(screen, (0, 0, 255), self.positions[node], 20)
            font = pygame.font.Font(None, 24)
            text_surf = font.render(str(node), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.positions[node])
            screen.blit(text_surf, text_rect.topleft)
