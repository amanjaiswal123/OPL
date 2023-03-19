import threading
from time import sleep
import pygame
from threading import Thread
from queue import Queue




# The gui works by having a thread run iterate through the event queue which takes the events and adds them to
# the event queue object. Which can then be accessed by the main thread. The main thread then calls the gui functions.
# this is done because pygame must have a thread running to handle events. But the pygame.getevents() function removes
# the events from the queue. So the events must be stored in a seperate object that allows two functions to read at the
# same time without removing the events from the queue.


#The listeners work by having a thread iterate through the event queue object and checkk if the event is matching.



class events_queue(list):

    def get_events(self):
        events = self
        self.clear()
        return events

    def peek_events(self):
        return list(self)

class board_display():
    def __init__(self):
        self.display_thread = Thread(target=self.run)
        self.display_thread.start()
        self.event_queue = events_queue()
        self.stack_offset = 0
        self.hand_offset = 0
        self.hand_select = False
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
    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def draw_all_stacks(self, players):
        stacks = []
        for c_player in players:
            for tile in c_player.stack:
                stacks.append(tile)
        padding = 10
        tiles_per_row = 3
        total_rows = 3
        tile_width = (self.screen.get_width() - padding*tiles_per_row-padding) // tiles_per_row
        tile_height = (self.screen.get_height() - padding*total_rows*2) // 5
        font_size = 36

        font = pygame.font.SysFont(None, font_size)
        max_offset = round((len(stacks) / (tiles_per_row * total_rows)) + .5) -1
        if self.stack_offset > max_offset:
            self.stack_offset = max_offset
        if self.stack_offset < 0:
            self.stack_offset = 0
        start_index = int(self.stack_offset * tiles_per_row * total_rows)
        end_index = int(start_index + (tiles_per_row * total_rows))

        tiles_surface = pygame.Surface((self.screen.get_width(), (tile_height*total_rows + (padding * total_rows))+padding))
        tiles_surface.fill((200, 200, 200))
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

    def draw_yes_no_prompt(self, prompt:str):
        button_width = 45
        button_height = 45

        width = self.screen.get_width()
        height = (self.screen.get_height()-10) / 5
        prompt_surface = pygame.Surface((width, height))
        prompt_surface.fill((200, 200, 200))
        prompt_font = pygame.font.SysFont(None, 24)
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, 40))
        prompt_surface.blit(prompt_text, prompt_rect)

        yes_button_image = pygame.image.load("yes.png").convert_alpha()
        scaled_yes_button_image = pygame.transform.scale(yes_button_image, (button_width, button_height))
        yes_button_rect = scaled_yes_button_image.get_rect()
        yes_button_rect.topleft = ((self.screen.get_width())/2-35-25, 80)

        no_button_image = pygame.image.load("no.png").convert_alpha()
        scaled_no_button_image = pygame.transform.scale(no_button_image, (button_width, button_height))
        no_button_rect = scaled_no_button_image.get_rect()
        no_button_rect.topleft = ((self.screen.get_width())/2-35+25, 80)



        prompt_surface.blit(scaled_yes_button_image, yes_button_rect)
        prompt_surface.blit(scaled_no_button_image, no_button_rect)

        self.screen.blit(prompt_surface, (0, int(self.screen.get_height()//5*3-5)))

        pygame.display.flip()

        check = True
        while check:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print('N')
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        prompt_surface = pygame.Surface((width, height))
                        prompt_surface.fill((200, 200, 200))
                        self.screen.blit(prompt_surface, (0, int(self.screen.get_height() // 5 * 3 - 5)))
                        pygame.display.flip()
                        return False
                    if event.key == pygame.K_y:
                        print('Y')
                        prompt_surface = pygame.Surface((width, height))
                        prompt_surface.fill((200, 200, 200))
                        self.screen.blit(prompt_surface, (0, int(self.screen.get_height() // 5 * 3 - 5)))
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return True

    def draw_play_another_round(self):
        button_width = 80
        button_height = 80
        prompt = "Play another round?"
        width = self.screen.get_width()
        height = self.screen.get_height()
        prompt_surface = pygame.Surface((width, height))
        prompt_surface.fill((200, 200, 200))
        prompt_font = pygame.font.SysFont(None, 36)
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2 - 50))
        prompt_surface.blit(prompt_text, prompt_rect)

        yes_button_image = pygame.image.load("yes.png").convert_alpha()
        scaled_yes_button_image = pygame.transform.scale(yes_button_image, (button_width, button_height))
        yes_button_rect = scaled_yes_button_image.get_rect()
        yes_button_rect.topleft = (width // 2 - button_width - 50, height // 2)

        no_button_image = pygame.image.load("no.png").convert_alpha()
        scaled_no_button_image = pygame.transform.scale(no_button_image, (button_width, button_height))
        no_button_rect = scaled_no_button_image.get_rect()
        no_button_rect.topleft = (width // 2 + 50, height // 2)

        prompt_surface.blit(scaled_yes_button_image, yes_button_rect)
        prompt_surface.blit(scaled_no_button_image, no_button_rect)

        self.screen.blit(prompt_surface, (0, 0))

        pygame.display.flip()

        check = True
        while check:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print('N')
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return False
                    if event.key == pygame.K_y:
                        print('Y')
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return True
    def draw_prompt(self, prompt:str, display_time=3):


        width = self.screen.get_width()
        height = (self.screen.get_height()-10) / 5
        prompt_surface = pygame.Surface((width, height))
        prompt_surface.fill((200, 200, 200))
        prompt_font = pygame.font.SysFont(None, 24)
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2))
        prompt_surface.blit(prompt_text, prompt_rect)

        self.screen.blit(prompt_surface, (0, int(self.screen.get_height()//5*3-5)))

        pygame.display.flip()
        sleep(display_time)

    def draw_move(self, left_tile, right_tile="None"):
        button_width = 45
        button_height = 45

        right_arrow = pygame.image.load("right-arrow.png").convert_alpha()
        right_arrow_button_image = pygame.transform.scale(right_arrow, (button_width, button_height))
        right_arrow_rect = right_arrow_button_image.get_rect()
        right_arrow_rect.topleft = ((self.screen.get_width())/2-25, 60)

        width = self.screen.get_width()
        height = (self.screen.get_height()-10) / 5
        tiles_surface = pygame.Surface((width, height))
        tiles_surface.fill((200, 200, 200))
        tiles_surface.blit(right_arrow_button_image, right_arrow_rect)


        padding = 10
        total_rows = 1
        tile_width = (self.screen.get_width() - padding*3-padding) // 3
        tile_height = ((self.screen.get_height() - padding*3*4) // 5)
        font_size = 36

        left_x = padding

        y = padding
        screen_x = left_x
        screen_y = y
        t_rect = left_tile.rect
        left_tile.draw_tile(tiles_surface, tile_width, tile_height, left_x, y, screen_x, screen_y)
        left_tile.rect = t_rect
        if str(right_tile) != "None":
            right_x = tile_width * 2 + padding * 3
            t_rect = right_tile.rect
            right_tile.draw_tile(tiles_surface, tile_width, tile_height, right_x, y, screen_x, screen_y)
            right_tile.rect = t_rect
        self.screen.blit(tiles_surface, (0, int(self.screen.get_height()//5*3-5)))
        pygame.display.flip()

        if str(right_tile) is not "None":
            while True:
                for event in self.event_queue.peek_events():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            print('Enter')
                            if event in self.event_queue:
                                self.event_queue.pop(self.event_queue.index(event))
                            return


    def draw_scores(self, dict, key_col_name, val_col_name, header):
        self.screen.fill((0, 0, 0))
        col1_x = self.screen.get_width() // 4
        col2_x = self.screen.get_width() * 3 // 4
        title_font = pygame.font.SysFont(None, 36)
        title_text = header
        title_color = (255, 255, 255)
        title_surface = title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 20))
        self.screen.blit(title_surface, title_rect)

        header_font = pygame.font.SysFont(None, 24)
        header_text = [key_col_name, val_col_name]
        header_color = (255, 255, 255)
        header_height = 60

        for i, text in enumerate(header_text):
            header_surface = header_font.render(text, True, header_color)
            header_rect = header_surface.get_rect()
            header_rect.midtop = (col1_x if i == 0 else col2_x, title_rect.bottom + 10)
            self.screen.blit(header_surface, header_rect)

        content_font = pygame.font.SysFont(None, 20)
        content_color = (255, 255, 255)
        row_height = 30

        for index, (player_id, player_score) in enumerate(dict.items()):
            player_id_surface = content_font.render(str(player_id), True, content_color)
            player_id_rect = player_id_surface.get_rect()
            player_id_rect.midtop = (col1_x, header_height + index * row_height)
            self.screen.blit(player_id_surface, player_id_rect)

            score_surface = content_font.render(str(player_score), True, content_color)
            score_rect = score_surface.get_rect()
            score_rect.midtop = (col2_x, header_height + index * row_height)
            self.screen.blit(score_surface, score_rect)

        pygame.display.flip()
        while True:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print('Enter')
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return



    def start_game_screen(self):
        background_image = pygame.image.load("background.jpg").convert()
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())

        start_button_image = pygame.image.load("start_button.png").convert_alpha()
        button_width = round(self.screen.get_size()[0] * 0.3)
        button_height = round(self.screen.get_size()[1] * 0.2)
        scaled_start_button_image = pygame.transform.scale(start_button_image, (button_width, button_height))
        self.start_button_rect = scaled_start_button_image.get_rect()
        self.start_button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        self.screen.blit(scaled_background_image, (0, 0))
        self.screen.blit(scaled_start_button_image, self.start_button_rect)


        pygame.display.flip()
        check = True
        while check:
            for event in self.event_queue.peek_events():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        check = False
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return


    def stack_scroll(self, players):
        while True:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('RIGHT')
                        self.stack_offset += 1
                        self.draw_all_stacks(players)
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                    if event.key == pygame.K_LEFT:
                        print('LEFT')
                        self.stack_offset -= 1
                        self.draw_all_stacks(players)
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for c_player in players:
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
    def draw_hand(self, hand):

        total_rows = 1
        padding = 10
        tiles_per_row = 3
        tile_width = (self.screen.get_width() - padding*tiles_per_row-padding) // tiles_per_row
        tile_height = (self.screen.get_height() - padding*total_rows-padding) // 5
        font_size = 36

        font = pygame.font.SysFont(None, font_size)
        max_offset = (len(hand) // tiles_per_row)-1
        if self.hand_offset > max_offset:
            self.hand_offset = max_offset
        if self.hand_offset < 0:
            self.hand_offset = 0
        start_index = self.hand_offset * tiles_per_row * total_rows
        end_index = start_index + tiles_per_row * total_rows

        tiles_surface = pygame.Surface((self.screen.get_width(), tile_height+padding*2))
        tiles_surface.fill((200, 200, 200))
        i = 0
        for tile in hand[start_index:end_index]:
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            y = ((i // tiles_per_row) * (tile_height + padding))+padding
            screen_x = x
            screen_y = self.screen.get_height() - tiles_surface.get_height() + y
            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y, screen_x, screen_y)
            i += 1
        self.screen.blit(tiles_surface, (0, self.screen.get_height() - tiles_surface.get_height()))
        pygame.display.flip()
        for tile in hand[0:start_index]:
            tile.rect = None
        for tile in hand[end_index:]:
            tile.rect = None
    def hand_listener(self, hand):
        while True:
            for event in self.event_queue.peek_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print('UP')
                        self.hand_offset += 1
                        self.draw_hand(hand)
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                    if event.key == pygame.K_DOWN:
                        print('DOWN')
                        self.hand_offset -= 1
                        self.draw_hand(hand)
                        pygame.display.flip()
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for tile in hand:
                        if tile.rect != None:
                            if tile.rect.collidepoint(event.pos) and self.hand_select:
                                for tile_ in hand:
                                    tile_.selected = False
                                tile.selected = True
                                print(tile)
                                if event in self.event_queue:
                                    self.event_queue.pop(self.event_queue.index(event))
                                return
class DisplayTile:

    def __init__(self):
        self.rect = None
        self.selected = False

    def draw_tile(self, screen, width,height, x, y, screen_x, screen_y):
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
