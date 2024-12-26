import math
import pygame

from cloth import Cloth
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from fan import Fan
from slider import Slider

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

slider_for_radius = Slider(1350, 100, 150, 5, 5, 50, 30, "Cursor Radius")
slider_for_fan_speed = Slider(1350, 200, 150, 5, 0, 50, 0, "Force")

fan = Fan(200, 800, 20, 100)

cloth = Cloth()
cloth.setup(71, 45, 10, 200, 50)
mouse_pos = mouse_pos_rel = (0, 0)
btn_clicked = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cloth.force["x"] += 5
            elif event.key == pygame.K_DOWN:
                cloth.force["x"] -= 5
            elif event.key == pygame.K_SPACE:
                cloth.force["x"] = 0
            if event.key == pygame.K_0:
                del slider_for_fan_speed
                del slider_for_radius
                del cloth
                slider_for_radius = Slider(1350, 100, 150, 5, 5, 50, 30, "Cursor Radius")
                slider_for_fan_speed = Slider(1350, 200, 150, 5, 0, 50, 0, "Force")
                cloth = Cloth()
                cloth.setup(71, 45, 10, 200, 50)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                btn_clicked = 1
            elif event.button == 3:
                btn_clicked = 3
        elif event.type == pygame.MOUSEBUTTONUP:
            btn_clicked = 0
        elif event.type == pygame.MOUSEMOTION and btn_clicked != 0:
            mouse_pos = event.pos
            mouse_pos_rel = event.rel
        slider_for_radius.handle_event(event)
        slider_for_fan_speed.handle_event(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # print(pygame.mouse.get_pos())
    # RENDER YOUR GAME HERE
    # deltaTime in seconds

    dt = clock.tick() / 1000.0
    dt = min(1 / 100, dt)

    slider_for_radius.draw(screen)
    slider_for_fan_speed.draw(screen)
    radius = slider_for_radius.get_value()
    speed = slider_for_fan_speed.get_value()
    fan.update(mouse_pos, btn_clicked,)
    fan.draw(screen)

    cloth.update(dt, mouse_pos, mouse_pos_rel, btn_clicked, radius, speed, fan)
    cloth.draw(screen)

    pygame.display.flip()

pygame.quit()
