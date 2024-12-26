import pygame


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, start_value, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.slider_pos = x + (start_value - min_value) / (max_value - min_value) * width
        self.dragging = False
        self.width = width
        self.x = x
        self.y = y
        self.text = text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update slider position within bounds
            mouse_x = event.pos[0]
            self.slider_pos = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
            # Calculate the slider value
            self.value = round(self.min_value + (self.slider_pos - self.rect.x) / self.rect.width * (
                    self.max_value - self.min_value))

    def draw(self, surface):
        font = pygame.font.Font(None, 36)
        text = f"{self.text}: {self.value}"
        text_surface = font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=(self.x + (self.width / 2), self.y - 30))  # Center at (400, 300)
        surface.blit(text_surface, text_rect)
        # Draw the slider bar
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        # Draw the slider knob
        knob_x = self.slider_pos - 5
        knob_y = self.rect.y - 5
        knob_rect = pygame.Rect(knob_x, knob_y, 15, self.rect.height + 10)
        pygame.draw.rect(surface, (100, 100, 255), knob_rect)


    def get_value(self):
        return self.value
