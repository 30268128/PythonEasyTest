import pygame
import random
import requests
import os
import json
pygame.init()

FISH_TYPES = [
    {"name": "Trout", "catch_probability": 0.6},
    {"name": "Salmon", "catch_probability": 0.3},
    {"name": "Catfish", "catch_probability": 0.1},
]
SERVER_URL = "http://127.0.0.1:5000"
WIDTH, HEIGHT = 1064, 571
FPS = 60
PLAYER_COLOR = (0, 128, 255)
OTHER_PLAYER_COLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
player_image = pygame.image.load(os.path.join("assets", "player.png"))
font = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
SAVE_FILE_PATH = "player_data.json"

    
class Player:
    def __init__(self, username, x, y):
        self.username = username
        self.rect = pygame.Rect(x, y, 50, 50)
        self.fishing = False
        self.inventory = []
        self.skill_level = 1  # Starting skill level
        self.experience = 0
        self.show_inventory = False  # Whether to display the inventory
        self.balance = 0
        self.font = pygame.font.SysFont(None, 24)
        

    def move(self, dx, dy):
        if not self.fishing:  # Only allow movement if not fishing
            self.rect.x += dx
            self.rect.y += dy
            self.update_position(dx, dy)

    def update_position(self, dx, dy):
        # Send the updated position to the server
        data = {'id': self.username, 'dx': dx, 'dy': dy}
        try:
            requests.post(f"{SERVER_URL}/update", json=data)
        except requests.ConnectionError:
            print("Failed to connect to the server.")

    def draw(self):
    # 繪製玩家圖片
        screen.blit(player_image, (self.rect.x, self.rect.y))
        # Draw the player's name above the rectangle
        name_surface = self.font.render(self.username, True, (0, 0, 0))  # Black text
        screen.blit(name_surface, (self.rect.centerx - name_surface.get_width() // 2, self.rect.top - 25))

        # If fishing, draw a circle to indicate fishing line
        if self.fishing:
            pygame.draw.circle(screen, (255, 0, 0), (self.rect.centerx, self.rect.bottom + 20), 5)

    def cast_line(self):
        self.fishing = True
        # Simulate waiting for a fish to bite
        pygame.time.set_timer(pygame.USEREVENT, random.randint(1000,10000)) 

    def catch_fish(self):
        self.fishing = False
        fish = random.choices(FISH_TYPES, weights=[f["catch_probability"] * (1 + self.skill_level * 0.1) for f in FISH_TYPES])[0]
        if random.random() < fish["catch_probability"]:
            self.inventory.append(fish["name"])
            self.experience += 20  # Gain experience for catching fish
            self.level_up()
            
            # 顯示捕魚訊息在遊戲畫面
            self.catch_message = f"You caught a {fish['name']}!"
            print(self.catch_message)  # 還可以選擇保留在終端顯示
        else:
            self.catch_message = "No fish this time!"
            print(self.catch_message)
    
        # 設置消息顯示計時器
        self.message_timer = pygame.time.get_ticks()

    def draw_catch_message(self):
        # 顯示釣魚消息5秒
        if hasattr(self, 'catch_message') and pygame.time.get_ticks() - self.message_timer < 5000:
            message_surface = font.render(self.catch_message, True, (255, 0, 0))  # 紅色文字
            screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2))


    def level_up(self):
        if self.experience >= 100:  # Example threshold for leveling up
            self.skill_level += 1
            self.experience -= 100  # Reset experience after leveling up
            print(f"Level Up! New Skill Level: {self.skill_level}")

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory  # Toggle inventory display on/off

    def draw_inventory(self):
        # Draw the inventory as a box on the screen
        if self.show_inventory:
            # Background box for inventory
            pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2), 2)

            # Display each item in the inventory
            for i, item in enumerate(self.inventory):
                text = font.render(f"{i + 1}. {item}", True, FONT_COLOR)
                screen.blit(text, (WIDTH // 4 + 20, HEIGHT // 4 + 20 + i * 40))

    def sell_fish(self, fish_prices):
        # Calculate total price of inventory
        total_value = sum(fish_prices[fish] for fish in self.inventory)
        self.balance += total_value
        self.inventory.clear()  # Empty the inventory after selling
        print(f"Sold all fish for ${total_value}. New balance: ${self.balance}")

    def draw_ui(self):
        # Draw the player's level and experience
        level_text = font.render(f"Level: {self.skill_level}", True, FONT_COLOR)
        screen.blit(level_text, (20, 20))
        exp_text = font.render(f"EXP: {self.experience}", True, FONT_COLOR)
        screen.blit(exp_text, (20, 60))

        # Draw the player's balance
        balance_text = font.render(f"Balance: ${self.balance}", True, FONT_COLOR)
        screen.blit(balance_text, (20, 100))
