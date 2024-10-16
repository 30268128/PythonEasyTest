import pygame
import requests

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
PLAYER_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Fishing Game")

# Player class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

# Game loop
def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            player.move(5, 0)
        if keys[pygame.K_UP]:
            player.move(0, -5)
        if keys[pygame.K_DOWN]:
            player.move(0, 5)

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)
        player.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
