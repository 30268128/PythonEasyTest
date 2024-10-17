import pygame
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
