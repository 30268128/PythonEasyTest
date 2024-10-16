import pygame
import requests
import random
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_COLOR = (0, 128, 255)
OTHER_PLAYER_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Fishing Game")

# Font for displaying inventory and text input
font = pygame.font.SysFont(None, 36)


class NPC:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 100)  # NPC position

    def draw(self):
        pygame.draw.rect(screen, (255, 165, 0), self.rect)  # Draw NPC as a rectangle

    def interact(self, player, fish_prices):
        # Check if the player is near enough to interact
        if self.rect.colliderect(player.rect):
            player.sell_fish(fish_prices)

# Player class
class Player:
    def __init__(self, player_id, x, y):
        self.player_id = player_id
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
        data = {'id': self.player_id, 'dx': dx, 'dy': dy}
        try:
            requests.post(f"{SERVER_URL}/update", json=data)
        except requests.ConnectionError:
            print("Failed to connect to the server.")

    def draw(self):
        # Draw the player's rectangle (character)
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

        # Draw the player's name above the rectangle
        name_surface = self.font.render(self.player_id, True, (0, 0, 0))  # Black text
        screen.blit(name_surface, (self.rect.centerx - name_surface.get_width() // 2, self.rect.top - 25))

        # If fishing, draw a circle to indicate fishing line
        if self.fishing:
            pygame.draw.circle(screen, (255, 0, 0), (self.rect.centerx, self.rect.bottom + 20), 5)

    def cast_line(self):
        self.fishing = True
        # Simulate waiting for a fish to bite
        pygame.time.set_timer(pygame.USEREVENT, 3000)  # Wait for 3 seconds

    def catch_fish(self):
        self.fishing = False
        fish = random.choices(FISH_TYPES, weights=[f["catch_probability"] * (1 + self.skill_level * 0.1) for f in FISH_TYPES])[0]
        if random.random() < fish["catch_probability"]:
            self.inventory.append(fish["name"])
            self.experience += 20  # Gain experience for catching fish
            self.level_up()
            print(f"You caught a {fish['name']}!")
        else:
            print("No fish this time!")

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
class Chat:
    def __init__(self, max_messages=5):
        self.messages = []         # Store chat messages
        self.current_message = ""  # For typing the current message
        self.max_messages = max_messages
        self.chat_active = False   # Whether the chat input is active
        self.font = pygame.font.SysFont(None, 24)  # Font for chat display

    def handle_input(self, event):
        # Handle typing input when chat is active
        if event.key == pygame.K_RETURN:
            if self.current_message:
                self.add_message(self.current_message)
                self.current_message = ""
                self.chat_active = False  # Exit chat mode after sending message
        elif event.key == pygame.K_BACKSPACE:
            self.current_message = self.current_message[:-1]
        else:
            self.current_message += event.unicode

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)  # Remove old messages if exceeded limit

    def toggle_chat(self):
        # Activate or deactivate chat input mode
        self.chat_active = not self.chat_active

    def draw(self, screen, width, height):
        # Draw the chat messages at the bottom left of the screen
        y_offset = height - 100
        for message in reversed(self.messages):  # Display recent messages at the bottom
            message_surface = self.font.render(message, True, (0, 0, 0))  # Black text
            screen.blit(message_surface, (20, y_offset))
            y_offset -= 30

        # Draw current input line if chat is active
        if self.chat_active:
            input_surface = self.font.render(f"> {self.current_message}", True, (0, 0, 0))
            screen.blit(input_surface, (20, height - 30))


# Function to join the game
def join_game(player_id):
    data = {'id': player_id}
    try:
        response = requests.post(f"{SERVER_URL}/join", json=data)
        return response.json()
    except requests.ConnectionError:
        print("Failed to connect to the server.")
        return None

# Function to get all players from the server
def get_all_players():
    try:
        response = requests.get(f"{SERVER_URL}/players")
        return response.json()
    except requests.ConnectionError:
        print("Failed to connect to the server.")
        return {}

def main():
    clock = pygame.time.Clock()

    # Get player name from in-game input
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
        player.draw()
        npc.draw()
        player.draw_ui()
        player.draw_inventory()

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
