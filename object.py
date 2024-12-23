import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Point:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.mass = mass

    def update(self, dt, force):
        # verlet integration
        vel_x = self.x - self.old_x
        vel_y = self.y - self.old_y

        # the current position becomes the old one
        self.old_x = self.x
        self.old_y = self.y

        acc_x = force["x"] / self.mass
        acc_y = force["y"] / self.mass

        self.x += vel_x + acc_x * dt * dt
        self.y += vel_y + acc_y * dt * dt

        self.constrain()

    def constrain(self):
        vel_x = self.x - self.old_x
        vel_y = self.y - self.old_y

        if self.x < 0:
            self.x = 0
            self.old_x = self.x + vel_x
        elif self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
            self.old_x = self.x + vel_x
        elif self.y < 0:
            self.y = 0
            self.old_y = self.y + vel_y
        elif self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.old_y = self.y + vel_y

    def render(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), 15)