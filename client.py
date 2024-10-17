import pygame
import requests
import random
import os
import json
from player import Player
from npc import NPC
from chat import Chat

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1064, 571
FPS = 60
OTHER_PLAYER_COLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Server URL
SERVER_URL = "http://127.0.0.1:5000"

# Define fish types
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


# Create the screen
pygame.display.set_caption("Multiplayer Fishing Game")

# Font for displaying inventory and text input
font = pygame.font.SysFont(None, 36)

# 加載背景圖片
background_image = pygame.image.load(os.path.join("assets", "background.png"))

# 加載背景音樂
pygame.mixer.music.load(os.path.join("assets", "background_music.mp3"))
pygame.mixer.music.play(-1)  # 循環播放

# Function to handle name input
def get_player_name():
    name = ""
    font = pygame.font.SysFont(None, 48)
    input_active = True

    while input_active:
        screen.fill(BACKGROUND_COLOR)
        prompt_text = font.render("Enter your name: ", True, (0, 0, 0))
        screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 3))

        # Render the typed name
        name_text = font.render(name, True, (0, 0, 0))
        screen.blit(name_text, (WIDTH // 4, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to submit the name
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace to delete a character
                    name = name[:-1]
                else:
                    # Add typed character to the name
                    name += event.unicode

    return name


# Function to join the game
def join_game(player_id):
    data = {'id': player_id}
    try:
        response = requests.post(f"{SERVER_URL}/join", json=data)
        return response.json()
    except requests.ConnectionError:
        print("Failed to connect to the server.")
        return None

def get_all_players():
    try:
        response = requests.get(f"{SERVER_URL}/players")
        return response.json()
    except requests.ConnectionError:
        print("Failed to connect to the server.")
        return {}

# 繪製其他玩家和名字
def draw_other_players(player_data, player_id):
    for pid, pdata in player_data.items():
        if pid != player_id:
            # 繪製玩家方塊
            pygame.draw.rect(screen, OTHER_PLAYER_COLOR, (pdata['x'], pdata['y'], 50, 50))

            # 繪製玩家名字
            name_surface = font.render(pid, True, (0, 0, 0))  # 黑色文字
            screen.blit(name_surface, (pdata['x'] + 25 - name_surface.get_width() // 2, pdata['y'] - 25))
def main():
    clock = pygame.time.Clock()

    # Get player name from   in-game input
    player_id = get_player_name()

    # Join the game with the provided player name (ID)
    player_data = join_game(player_id)
    if player_data is None:
        return

    player = Player(player_id, player_data[player_id]['x'], player_data[player_id]['y'])
    npc = NPC(600, 300)  # NPC for selling fish
    chat = Chat()  # Initialize the Chat system

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.USEREVENT and player.fishing:
                player.catch_fish()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:  # 'T' key to toggle chat mode
                    chat.toggle_chat()
                if chat.chat_active:
                    chat.handle_input(event)
                elif event.key == pygame.K_i and not player.fishing:
                    player.toggle_inventory()

        keys = pygame.key.get_pressed()
        if not player.fishing and not chat.chat_active:  # Don't move if fishing or chatting
            if keys[pygame.K_LEFT]:
                player.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                player.move(5, 0)
            if keys[pygame.K_UP]:
                player.move(0, -5)
            if keys[pygame.K_DOWN]:
                player.move(0, 5)

        if keys[pygame.K_SPACE] and not player.fishing and not chat.chat_active:
            player.cast_line()
        if keys[pygame.K_e]:  # Interact with NPC
            npc.interact(player, fish_prices)

        # Clear the screen
        
        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, (0, 0))
        player.draw()
        npc.draw_npc()
        player.draw_ui()
        player.draw_inventory()
        # Draw other players
        all_players = get_all_players()
        draw_other_players(all_players, player_id)
        player.draw_catch_message()

        # Draw chat system
        chat.draw(screen, WIDTH, HEIGHT)
        

        # Draw other players
        all_players = get_all_players()
        for pid, pdata in all_players.items():
            if pid != player_id:
                pygame.draw.rect(screen, OTHER_PLAYER_COLOR, (pdata['x'], pdata['y'], 50, 50))
        

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
if __name__ == "__main__":
    main()
