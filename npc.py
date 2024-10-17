import pygame
import os
npc_image = pygame.image.load(os.path.join("assets", "npc.png"))
WIDTH, HEIGHT = 1064, 571
FPS = 60
FONT_COLOR = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class NPC:
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 100)  # NPC position
        self.font = pygame.font.SysFont(None, 24)
    def draw_npc(self):
        screen.blit(npc_image, (self.rect.x, self.rect.y))
        name_surface = self.font.render("Vendor", True, (0, 0, 0))  # Black text
        screen.blit(name_surface, (self.rect.centerx - name_surface.get_width() // 2, self.rect.top - 25))


    def interact(self, player, fish_prices):
        # Check if the player is near enough to interact
        if self.rect.colliderect(player.rect):
            player.sell_fish(fish_prices)