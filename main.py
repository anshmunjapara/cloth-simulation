import pygame
from object import Point
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

force = {
    "x": 200.0,
    "y": 300.0
}

points = [Point(400, 200, 1.0),
          Point(600, 200, 1.0)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    # deltaTime in seconds

    dt = clock.tick() / 1000.0
    dt = min(1/100, dt)

    for point in points:
        point.update(dt, force)

    for point in points:
        point.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()