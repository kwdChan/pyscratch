import pygame
pygame.init()

# Set up a display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Mouse Scroll Demo")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect mouse wheel scroll
        elif event.type == pygame.MOUSEWHEEL:
            print(f"Mouse wheel scrolled: precise_y={event.precise_y}, y={event.y}")
            # y > 0 means scroll up, y < 0 means scroll down

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()
