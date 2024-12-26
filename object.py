import math
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Point:
    def __init__(self, x, y, mass, pinned, can_interact=True):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.mass = mass
        self.pinned = pinned
        self.sticks = [0, 0]
        self.interactive = can_interact

    def update(self, dt, force, drag, elasticity, mouse_pos, mouse_pos_rel, btn_clicked, radius):

        if not self.pinned:
            if self.interactive:
                cursor_to_pos_dir_x = self.x - mouse_pos[0]
                cursor_to_pos_dir_y = self.y - mouse_pos[1]
                cursor_to_pos_dist = cursor_to_pos_dir_x * cursor_to_pos_dir_x + cursor_to_pos_dir_y * cursor_to_pos_dir_y
                cursorSize = radius

                is_selected = cursor_to_pos_dist < cursorSize * cursorSize

                for stick in self.sticks:
                    if stick != 0:
                        stick.is_selected = is_selected

                if is_selected and btn_clicked == 1:
                    difference_x = mouse_pos_rel[0]
                    difference_y = mouse_pos_rel[1]

                    if difference_x > elasticity:
                        difference_x = elasticity
                    if difference_y > elasticity:
                        difference_y = elasticity
                    if difference_x < -elasticity:
                        difference_x = -elasticity
                    if difference_y < -elasticity:
                        difference_y = -elasticity

                    self.old_x = self.x - difference_x
                    self.old_y = self.y - difference_y

                #
                if btn_clicked == 3 and is_selected:
                    for stick in self.sticks:
                        if stick != 0:
                            stick.detach()

            vel_x = self.x - self.old_x
            vel_y = self.y - self.old_y

            self.old_x = self.x
            self.old_y = self.y

            acc_x = force["x"] / self.mass
            acc_y = force["y"] / self.mass

            self.x += vel_x * (1.0 - drag) + (acc_x * dt * dt) * (1.0 - drag)
            self.y += vel_y * (1.0 - drag) + (acc_y * dt * dt) * (1.0 - drag)

            self.constrain()

    def add_stick(self, stick, index):
        self.sticks[index] = stick

    def constrain(self):
        vel_x = self.x - self.old_x
        vel_y = self.y - self.old_y

        if self.x < 0:
            self.x = 0
            self.old_x = self.x + vel_x
        elif self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
            self.old_x = self.x + vel_x
        if self.y < 0:
            self.y = 0
            self.old_y = self.y + vel_y
        elif self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.old_y = self.y + vel_y

    def render(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), 2)


class Stick:
    def __init__(self, p0, p1, length):
        self.p0 = p0
        self.p1 = p1
        self.length = length
        self.is_active = True
        self.is_selected = False

    def update(self):
        if not self.is_active:
            return
        dx = self.p1.x - self.p0.x
        dy = self.p1.y - self.p0.y
        dist = math.sqrt(dx * dx + dy * dy)
        diff = self.length - dist
        if dist == 0:
            return

        percent = (diff / dist) / 2

        offset_x = dx * percent
        offset_y = dy * percent

        if not self.p0.pinned:
            self.p0.x -= offset_x
            self.p0.y -= offset_y

        if not self.p1.pinned:
            self.p1.x += offset_x
            self.p1.y += offset_y

    def detach(self):
        self.is_active = False

    def render(self, screen):
        if not self.is_active:
            return
        pygame.draw.line(screen, "white", (self.p0.x, self.p0.y), (self.p1.x, self.p1.y), 2)
