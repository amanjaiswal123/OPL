import threading

import pygame
from threading import Thread
from queue import Queue

class events_queue(list):

    def get_events(self):
        events = self
        self.clear()
        return events

    def peek_events(self):
        return list(self)

class game_display():
    def __init__(self):
        self.display_thread = Thread(target=self.run)
        self.display_thread.start()
        self.event_queue = events_queue()
        self.stack_offset = 0
        self.stack_select = False

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
        self.handle = True
        self.screen = pygame.display.set_mode((345, 750))
        self.running = True
        self.clock = pygame.time.Clock()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.event_queue.append(event)
                if len(self.event_queue) > 50:
                    self.event_queue.clear()
                    print("Event queue overflowed, clearing queue")
            # Start button pressed, set start_clicked to True
    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def stack_listener(self):
        stacks = []
        for c_player in self.players:
            for tile in c_player.stack:
                stacks.append(tile)
        # Set up constants for the tile size, padding, and font
        tile_width = (self.screen.get_width() - 40) // 3
        tile_height = tile_width * 1.5
        padding = 10
        font_size = 36

        font = pygame.font.SysFont(None, font_size)
        tiles_per_row = self.screen.get_width() // tile_width
        total_rows = (self.screen.get_height() // tile_height) - 1
        max_offset = round((len(stacks) / (tiles_per_row * total_rows)) + .5) -1
        if self.stack_offset > max_offset:
            self.stack_offset = max_offset
        if self.stack_offset < 0:
            self.stack_offset = 0
        start_index = int(self.stack_offset * tiles_per_row * total_rows)
        end_index = int(start_index + (tiles_per_row * total_rows))

        tiles_surface = pygame.Surface((self.screen.get_width(), (tile_height*total_rows + (padding * total_rows))+padding))
        tiles_surface.fill((255, 255, 255))
        i = 0
        for tile in stacks[start_index:end_index]:
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            y = ((i // tiles_per_row) * (tile_height + padding)) + padding
            screen_x = x
            screen_y = y
            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y, screen_x, screen_y)
            self.screen.blit(tiles_surface, (0, 0))
            pygame.display.flip()
            i += 1
        for tile in stacks[0:start_index]:
            tile.rect = None
        for tile in stacks[end_index:]:
            tile.rect = None

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
        check = True
        while check:
            for event in self.event_queue.get_events():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        check = False
                        break
        self.start_new_tournament(self.player_num, self.double_set_length)

    def stack_scroll(self):
        while True:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('RIGHT')
                        self.stack_offset += 1
                        self.stack_listener()
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                    if event.key == pygame.K_LEFT:
                        print('LEFT')
                        self.stack_offset -= 1
                        self.stack_listener()
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for c_player in self.players:
                        for tile in c_player.stack:
                            if tile.rect != None:
                                if tile.rect.collidepoint(event.pos):
                                    if self.stack_select:
                                        for tile_ in c_player.stack:
                                            tile_.selected = False
                                        tile.selected = True
                                        print(tile)
                                        return
                                    if event in self.event_queue:
                                        self.event_queue.pop(self.event_queue.index(event))

class display_player_attributes():
    def __init__(self):
        self.hand_offset = 0
        self.hand_select = False
    def draw_hand(self, screen):
        # Set up constants for the tile size, padding, and font
        tile_width = (screen.get_width() - 40) // 3
        tile_height = tile_width * 1.5
        padding = 10
        font_size = 36

        font = pygame.font.SysFont(None, font_size)
        tiles_per_row = screen.get_width() // tile_width
        max_offset = (len(self.hand) // tiles_per_row)-1
        if self.hand_offset > max_offset:
            self.hand_offset = max_offset
        if self.hand_offset < 0:
            self.hand_offset = 0
        start_index = self.hand_offset * tiles_per_row
        end_index = start_index + tiles_per_row

        tiles_surface = pygame.Surface((screen.get_width(), tile_height+padding*2))
        tiles_surface.fill((255, 255, 255))
        i = 0
        for tile in self.hand[start_index:end_index]:
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            y = ((i // tiles_per_row) * (tile_height + padding))+padding
            screen_x = x
            screen_y = screen.get_height() - tiles_surface.get_height() + y
            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y, screen_x, screen_y)
            i += 1
        screen.blit(tiles_surface, (0, screen.get_height() - tiles_surface.get_height()))
        pygame.display.flip()
        for tile in self.hand[0:start_index]:
            tile.rect = None
        for tile in self.hand[end_index:]:
            tile.rect = None




    def hand_listener(self, event_queue, screen):
        while True:
            for event in event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_UP:
                        print('UP')
                        self.hand_offset += 1
                        self.draw_hand(screen)
                        pygame.display.flip()
                        if event in event_queue:
                            event_queue.pop(event_queue.index(event))
                    if event.key == pygame.K_DOWN:
                        print('DOWN')
                        self.hand_offset -= 1
                        self.draw_hand(screen)
                        pygame.display.flip()
                        if event in event_queue:
                            event_queue.pop(event_queue.index(event))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for tile in self.hand:
                        if tile.rect != None:
                            if tile.rect.collidepoint(event.pos) and self.hand_select:
                                for tile_ in self.hand:
                                    tile_.selected = False
                                tile.selected = True
                                print(tile)
                                if event in event_queue:
                                    event_queue.pop(event_queue.index(event))
                                return



class DisplayTile:

    def __init__(self):
        self.rect = None
        self.selected = False

    def draw_tile(self, screen, width,height, x, y, screen_x, screen_y):
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
        self.rect = pygame.rect.Rect(screen_x, screen_y, TILE_WIDTH, TILE_HEIGHT)
