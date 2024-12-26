import math

import pygame

from object import Point, Stick


def distance(p0_x, p0_y, p1_x, p1_y):
    dx = p1_x - p0_x
    dy = p1_y - p0_y
    return math.sqrt(dx * dx + dy * dy)


class Fan:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.angle = 90
        self.rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect_surface.fill((255, 0, 0))  # Fill it with red color
        self.rotated_surface = pygame.transform.rotate(self.rect_surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=(self.x, self.y))
        self.edge_point_x = x + (width / 2 - 10)
        self.edge_point_y = y + height / 2
        self.update_edge_point()

    def update_edge_point(self):
        # Calculate the edge point relative to the center based on the angle
        offset_x = self.width / 2
        offset_y = 0  # The edge is on the right end of the rectangle
        rotated_x = offset_x * math.cos(math.radians(self.angle)) - offset_y * math.sin(math.radians(self.angle))
        rotated_y = offset_x * math.sin(math.radians(self.angle)) + offset_y * math.cos(math.radians(self.angle))
        self.edge_point_x = self.x + rotated_x
        self.edge_point_y = self.y + rotated_y

    def update(self, mouse_pos, btn_clicked):
        angle_rad = math.radians(-self.angle)  # Convert angle to radians
        if btn_clicked == 1 and self.touches_end(mouse_pos):
            mouse_x, mouse_y = mouse_pos
            self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
            self.rotated_surface = pygame.transform.rotate(self.rect_surface, -self.angle)
            self.rotated_rect = self.rotated_surface.get_rect(center=(self.x, self.y))
            self.update_edge_point()

    def touches_end(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return distance(self.edge_point_x, self.edge_point_y, mouse_x, mouse_y) < 20

    def draw(self, surface):
        surface.blit(self.rotated_surface, self.rotated_rect.topleft)

        pygame.draw.circle(surface, (0, 255, 0), (int(self.edge_point_x), int(self.edge_point_y)), 5)

