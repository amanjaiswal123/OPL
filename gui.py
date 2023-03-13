import pygame
from threading import Thread


class Game_display():
    def __init__(self):
        self.display_thread = Thread(target=self.run)
        self.display_thread.start()
    def run(self):
        self.intialize_screen()
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
    def update(self):
        pass

    def intialize_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((345, 750))
        self.running = True
        self.clock = pygame.time.Clock()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.start_button_rect.collidepoint(event.pos):
                self.start_clicked = True
                # Start button pressed, set start_clicked to True


    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def start_game_screen(self):
        # Set up the background image
        background_image = pygame.image.load("background.jpg").convert()
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())

        # Set up the start button
        start_button_image = pygame.image.load("start_button.png").convert_alpha()
        button_width = round(self.screen.get_size()[0] * 0.3)  # 30% of the screen width
        button_height = round(self.screen.get_size()[1] * 0.2)  # 20% of the screen height
        scaled_start_button_image = pygame.transform.scale(start_button_image, (button_width, button_height))
        self.start_button_rect = scaled_start_button_image.get_rect()
        self.start_button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        # Draw the background and start button
        self.screen.blit(scaled_background_image, (0, 0))
        self.screen.blit(scaled_start_button_image, self.start_button_rect)

        # Update the display
        pygame.display.flip()


class display_player_attributes():
    def __init__(self, hand):
        self.hand = hand
        self.hand_offset = 0
    def draw_hand(self, screen):
        # Set up constants for the tile size, padding, and font
        tile_width = (screen.get_width() - 40) // 3
        tile_height = tile_width * 1.5
        padding = 10
        font_size = 36

        font = pygame.font.SysFont(None, font_size)
        max_rows = (screen.get_height() - 40) // tile_height
        tiles_per_row = screen.get_width() // tile_width
        total_rows = (len(self.hand) + tiles_per_row - 1) // tiles_per_row
        max_offset = max(0, total_rows - max_rows)
        self.hand_offset = min(max_offset, max(0, self.hand_offset))
        start_index = self.hand_offset * tiles_per_row
        end_index = min(start_index + max_rows * tiles_per_row, len(self.hand))

        tiles_surface = pygame.Surface((screen.get_width(), tile_height+padding*2))
        tiles_surface.fill((255, 255, 255))

        for i in range(start_index, end_index):
            tile = self.hand[i]
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            y = ((i // tiles_per_row + max_offset) * (tile_height + padding))+padding

            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y)
        screen.blit(tiles_surface, (0, screen.get_height() - tiles_surface.get_height()))


class DisplayTile:

    def draw_tile(self, screen, width,height, x, y):
        # draw the tile on the screen at x and y
        # with a horizontal line separating two numbers
        if self.player.color == "B":
            primary_color = (255, 255, 255)
            alt_color = (0, 0, 0)
        elif self.player.color == "R":
            primary_color = (0, 0, 0)
            alt_color = (255, 96, 96)
        elif self.player.color == "G":
            primary_color = (0, 0, 0)
            alt_color = (96, 255, 95)
        else:
            primary_color = (0, 0, 0)
            alt_color = (255, 255, 255)
        TILE_WIDTH = width
        TILE_HEIGHT = height
        font_size = 30
        font = pygame.font.SysFont('Arial', font_size)
        tile_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        tile_surface.fill(primary_color)
        pygame.draw.line(tile_surface, alt_color, (0, TILE_HEIGHT // 2), (TILE_WIDTH, TILE_HEIGHT // 2), 2)
        top_num = font.render(str(self.left), True, alt_color)
        top_num_center = (TILE_WIDTH // 3, 0)
        bottom_num = font.render(str(self.right), True, alt_color)
        bottom_num_center = (TILE_WIDTH // 3, TILE_HEIGHT-bottom_num.get_height())
        tile_surface.blit(top_num, top_num_center)
        tile_surface.blit(bottom_num, bottom_num_center)
        screen.blit(tile_surface, (x, y))
        pygame.display.flip()
