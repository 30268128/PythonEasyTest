import pygame
import random

# 初始化 Pygame
pygame.init()

# 常數定義
WIDTH, HEIGHT = 720 , 640
FPS = 60
PLAYER_COLOR = (0, 128, 255)
NPC_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

# 創建遊戲視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("單機釣魚遊戲")
font = pygame.font.SysFont(None, 36)

# 定義魚的種類和價格
FISH_TYPES = [
    {"name": "Trout", "catch_probability": 0.6},
    {"name": "Salmon", "catch_probability": 0.3},
    {"name": "Catfish", "catch_probability": 0.1},
]
fish_prices = {
    "Trout": 10,
    "Salmon": 20,
    "Catfish": 50
}

# 玩家類別
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.fishing = False
        self.inventory = []
        self.skill_level = 1
        self.experience = 0
        self.show_inventory = False
        self.balance = 0
        self.font = pygame.font.SysFont(None, 24)
    
    def move(self, dx, dy):
        if not self.fishing:
            self.rect.x += dx
            self.rect.y += dy
    
    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
        # 在玩家頭上顯示等級
        level_text = self.font.render(f"Level {self.skill_level}", True, FONT_COLOR)
        screen.blit(level_text, (self.rect.centerx - level_text.get_width() // 2, self.rect.top - 25))
        if self.fishing:
            pygame.draw.circle(screen, (255, 0, 0), (self.rect.centerx, self.rect.bottom + 20), 5)
    
    def cast_line(self):
        self.fishing = True
        pygame.time.set_timer(pygame.USEREVENT, 3000)  # 等待3秒
    
    def catch_fish(self):
        self.fishing = False
        fish = random.choices(FISH_TYPES, weights=[f["catch_probability"] * (1 + self.skill_level * 0.1) for f in FISH_TYPES])[0]
        if random.random() < fish["catch_probability"]:
            self.inventory.append(fish["name"])
            self.experience += 20
            self.level_up()
            print(f"你捕獲了一條 {fish['name']}!")
        else:
            print("這次沒有魚上鉤！")
    
    def level_up(self):
        if self.experience >= 100:
            self.skill_level += 1
            self.experience -= 100
            print(f"升級了！新技能等級：{self.skill_level}")
    
    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
    
    def draw_inventory(self):
        if self.show_inventory:
            pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2), 2)
            for i, item in enumerate(self.inventory):
                text = font.render(f"{i + 1}. {item}", True, FONT_COLOR)
                screen.blit(text, (WIDTH // 4 + 20, HEIGHT // 4 + 20 + i * 40))
    
    def sell_fish(self, fish_prices):
        total_value = sum(fish_prices[fish] for fish in self.inventory)
        self.balance += total_value
        self.inventory.clear()
        print(f"賣出了所有魚，獲得 ${total_value}。當前餘額：${self.balance}")
    
    def draw_ui(self):
        level_text = font.render(f"等級: {self.skill_level}", True, FONT_COLOR)
        screen.blit(level_text, (20, 20))
        exp_text = font.render(f"經驗值: {self.experience}", True, FONT_COLOR)
        screen.blit(exp_text, (20, 60))
        balance_text = font.render(f"餘額: ${self.balance}", True, FONT_COLOR)
        screen.blit(balance_text, (20, 100))

# NPC 類別
class NPC:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 100)
    
    def draw(self):
        pygame.draw.rect(screen, NPC_COLOR, self.rect)
    
    def interact(self, player, fish_prices):
        if self.rect.colliderect(player.rect):
            player.sell_fish(fish_prices)

# 主遊戲循環
def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2)
    npc = NPC(600, 300)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT and player.fishing:
                player.catch_fish()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and not player.fishing:
                    player.toggle_inventory()
        keys = pygame.key.get_pressed()
        if not player.fishing:
            if keys[pygame.K_LEFT]:
                player.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                player.move(5, 0)
            if keys[pygame.K_UP]:
                player.move(0, -5)
            if keys[pygame.K_DOWN]:
                player.move(0, 5)
        if keys[pygame.K_SPACE] and not player.fishing:
            player.cast_line()
        if keys[pygame.K_e]:
            npc.interact(player, fish_prices)
        # 清除螢幕
        screen.fill(BACKGROUND_COLOR)
        player.draw()
        npc.draw()
        player.draw_ui()
        player.draw_inventory()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()