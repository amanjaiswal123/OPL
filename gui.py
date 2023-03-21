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
        #Player move is used to determine if this is a player move or computer move as they are handled diffrently by
        #by the event handler
        self.player_move = False
        #The display thread is the thread that runs the display, it will take events from the event queue and add them
        #to the event queue object
        self.display_thread = Thread(target=self.run)
        #Start the thread
        self.display_thread.start()
        #The event queue object used to store all the events
        self.event_queue = events_queue()
        #The stack offset is used to scroll through the stacks. 9 tiles are displayed at a time, if the offset was 2
        #then it would show tiles 10-18
        self.stack_offset = 0
        #The hand offset is used to scroll through the hand. 3 tiles are displayed at a time, if the offset was 2
        #then it would show tiles 6-8
        self.hand_offset = 0
        #The hand select is used to allow and disallow the player to select a tile from their hand. This is used so that
        #the player does not select two tiles from the hand
        self.hand_select = False
        #The stack select is used to allow and disallow the player to select a tile from the stack. This is used so that
        #the player does not select two tiles from the stack
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

    def set_stack_offset(self, n):
        self.stack_offset = n

    def set_hand_select(self, n):
        self.hand_select = n

    def set_stack_select(self, n):
        self.stack_select = n

    def set_player_move(self, n):
        self.player_move = n

    # *********************************************************************
    # Function Name: draw_all_stacks
    # Purpose: To display all the tiles in a stack of tiles for each player
    # Parameters:
    #            players, a list of player objects. It holds information about each player and their respective tiles
    # Return Value: None
    # Algorithm:
    #            1) Retrieve the tiles for each player using the player's get_stack method
    #            2) Calculate the dimensions and font size for each tile to be displayed
    #            3) Determine the maximum number of tile rows to be displayed based on the screen size
    #            4) Determine the starting and ending indices for the tiles to be displayed based on the stack offset
    #            5) Create a surface to display the tiles on
    #            6) Draw each tile on the surface
    #            7) Update the display with the tiles surface
    # Assistance Received: None
    # *********************************************************************
    def draw_all_stacks(self, players):
        #We combine all the stacks into one list so we can display them all at once
        stacks = []
        #We get the stack for each player and add it to the stacks list
        #Iterate through the players
        for c_player in players:
            #Iterate through the stacks
            for tile in c_player.get_stack():
                #Add the tile to the combined stacks list
                stacks.append(tile)
        #Set the padding between tiles
        padding = 10
        #Set the number of tiles per row
        tiles_per_row = 3
        #Set the total number of rows
        total_rows = 3
        #Calculate the width and height of each tile based on the screen size
        tile_width = (self.screen.get_width() - padding*tiles_per_row-padding) // tiles_per_row
        tile_height = (self.screen.get_height() - padding*total_rows*2) // 5
        #The font size for the numbers on the tiles
        font_size = 36

        #Create a font object
        font = pygame.font.SysFont(None, font_size)
        #Calculate the maximum offset for the stacks. If there are 18 tiles it should be 2. If there was 9 it would be 1
        #As only 9 tiles can fit on the display at once
        max_offset = round((len(stacks) / (tiles_per_row * total_rows)) + .5)
        #If the offset is greater than the max offset, set it to the max offset
        if self.stack_offset > max_offset:
            self.stack_offset = max_offset
        #If the offset is less than 0, set it to 0
        if self.stack_offset < 0:
            self.stack_offset = 0
        #Calculate the starting and ending indices for the tiles to be displayed, based on the offset
        start_index = int(self.stack_offset * tiles_per_row * total_rows)
        #Calcuate the end index.
        end_index = int(start_index + (tiles_per_row * total_rows))

        #Create the tile surface
        tiles_surface = pygame.Surface((self.screen.get_width(), (tile_height*total_rows + (padding * total_rows))+padding))
        #Fill the tile surface with a light grey color
        tiles_surface.fill((200, 200, 200))
        #Create a counter to keep track of how many tiles are displayed as every 3 tiles we need to start a new row
        #We also need to keep track whether it will be on the left, middle or right
        i = 0
        #Iterate through the stacks and display each tile
        for tile in stacks[start_index:end_index]:
            #Set the tiles x.
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            #Set the tiles y which will start a new row every 3 tiles
            y = ((i // tiles_per_row) * (tile_height + padding)) + padding
            #Draw the tile on the surface
            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y, x, y)
            #Increment the counter
            i += 1
        #Set the hitboxes for all tiles that are not dispalyed to None so they are not registered when clicked
        for tile in stacks[0:start_index]:
            tile.set_rect(None)
        for tile in stacks[end_index:]:
            tile.set_rect(None)

        #Update the display with the tiles surface
        self.screen.blit(tiles_surface, (0, 0))
        pygame.display.flip()

    def draw_winner(self, winner):

        # Load the background image
        background = pygame.image.load("win.jpg")
        # Get the dimensions of the screen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        # Scale the background image to the size of the screen
        background = pygame.transform.scale(background, (screen_width, screen_height))
        # Display the background on the screen
        self.screen.blit(background, (0, 0))
        # Set the font for the winner text
        font = pygame.font.SysFont(None, 36)
        # Render the winner text with a black outline
        winner_text = font.render(f"Winner: {winner}", True, (255, 255, 255), (0, 0, 0))
        winner_text_outline = font.render(f"Winner: {winner}", True, (0, 0, 0), (255, 255, 255))
        # Get the rectangle for the winner text
        winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2))
        # Display the winner text and its outline on the screen
        self.screen.blit(winner_text, winner_rect)
        pygame.display.flip()

    #*********************************************************************
    #Function Name: draw_yes_no_prompt
    #Purpose: To display a prompt to the user and ask them to respond with either "yes" or "no"
    #Parameters:

    #prompt, a string. It represents the prompt to be displayed to the user
    #Return Value: A boolean value indicating whether the user responded "yes" or "no"
    #Algorithm:

    #1) Create a surface for the prompt with a specified width and height
    #2) Render the prompt text on the surface using a specified font
    #3) Load and scale "yes" and "no" button images
    #4) Display the prompt surface with the "yes" and "no" buttons on the screen
    #5) Wait for a key event from the user
    #6) If the user presses "n", return False
    #7) If the user presses "y", return True
    #Assistance Received: None
    #*********************************************************************
    def draw_yes_no_prompt(self, prompt:str):
        #Set the width and height of the buttons
        button_width = 45
        button_height = 45

        #Create the prompt surface
        width = self.screen.get_width()
        #The height of the prompt surface is 1/5 of the screen height
        height = (self.screen.get_height()-10) / 5
        #Create the surface
        prompt_surface = pygame.Surface((width, height))
        #Fill the surface with a light grey color
        prompt_surface.fill((200, 200, 200))
        #Set the font for the prompt
        prompt_font = pygame.font.SysFont(None, 24)
        #Render the prompt text on the surface
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, 40))
        prompt_surface.blit(prompt_text, prompt_rect)


        #Load and scale the "yes" and "no" button images
        yes_button_image = pygame.image.load("n.png").convert_alpha()
        #Scale the image
        scaled_yes_button_image = pygame.transform.scale(yes_button_image, (button_width, button_height))
        #Get the rect for the image
        yes_button_rect = scaled_yes_button_image.get_rect()
        #Set the top left corner of the rect for the hitbox
        yes_button_rect.topleft = ((self.screen.get_width())/2-35-25, 80)


        #Load and scale the "no" button image
        no_button_image = pygame.image.load("y.png").convert_alpha()
        #Scale the image
        scaled_no_button_image = pygame.transform.scale(no_button_image, (button_width, button_height))
        #Get the rect for the image
        no_button_rect = scaled_no_button_image.get_rect()
        #Set the top left corner of the rect for the hitbox
        no_button_rect.topleft = ((self.screen.get_width())/2-35+25, 80)


        #Display the prompt surface with the "yes" and "no" buttons on the screen
        prompt_surface.blit(scaled_yes_button_image, yes_button_rect)
        prompt_surface.blit(scaled_no_button_image, no_button_rect)
        self.screen.blit(prompt_surface, (0, int(self.screen.get_height()//5*3-5)))

        pygame.display.flip()

        #Listen for a Y or N key press and return the appropriate value
        #Clear the event queue to prevent the user from pressing a key before the prompt is displayed
        self.event_queue.clear()
        while True:
            #Iterate through the event queue
            for event in self.event_queue.peek_events():
                #If the user presses a key on the keyboard
                if event.type == pygame.KEYDOWN:
                    #If the user presses "n", return False
                    if event.key == pygame.K_n:
                        print('N')
                        #We remove the event from the queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        prompt_surface = pygame.Surface((width, height))
                        prompt_surface.fill((200, 200, 200))
                        self.screen.blit(prompt_surface, (0, int(self.screen.get_height() // 5 * 3 - 5)))
                        pygame.display.flip()
                        return False
                    #If the user presses "y", return True
                    if event.key == pygame.K_y:
                        print('Y')
                        prompt_surface = pygame.Surface((width, height))
                        prompt_surface.fill((200, 200, 200))
                        self.screen.blit(prompt_surface, (0, int(self.screen.get_height() // 5 * 3 - 5)))
                        pygame.display.flip()
                        #We remove the event from the queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return True

    #*********************************************************************
    #Function Name: draw_prompt
    #Purpose: To display a prompt on the screen and wait for the user to press enter
    #Parameters:
    #            prompt, a string representing the prompt to be displayed
    #            font_size, an optional integer representing the font size of the prompt text
    #Return Value: None
    #Algorithm:
    #            1) Create a surface for the prompt
    #            2) Fill the surface with a light grey color
    #            3) Set the font for the prompt
    #            4) Render the prompt text and center it on the surface
    #            5) Display the prompt surface on the screen
    #            6) Clear the event queue to prevent the user from pressing a key before the prompt is displayed
    #            7) Listen for the user to press enter
    #Assistance Received: None
    #*********************************************************************
    def draw_prompt(self, prompt: str, font_size=20):
        # Get the width and height of the screen
        width = self.screen.get_width()
        height = (self.screen.get_height() - 10) / 5
        # Create the surface
        prompt_surface = pygame.Surface((width, height))
        # Fill the surface with a light grey color
        prompt_surface.fill((200, 200, 200))
        # Set the font for the prompt
        prompt_font = pygame.font.SysFont(None, font_size)

        lines = []
        line = ""
        words = prompt.split(" ")
        for word in words:
            if prompt_font.size(line + " " + word)[0] <= width:
                line += " " + word
            else:
                lines.append(line)
                line = word
        lines.append(line)

        y_offset = 0
        for line in lines:
            prompt_text = prompt_font.render(line, True, (0, 0, 0))
            prompt_rect = prompt_text.get_rect(center=(width // 2, 40 + y_offset))
            prompt_surface.blit(prompt_text, prompt_rect)
            y_offset += 40

        # Display the prompt surface on the screen
        self.screen.blit(prompt_surface, (0, int(self.screen.get_height() // 5 * 3 - 5)))
        pygame.display.flip()

        # Clear the event queue to prevent the user from pressing a key before the prompt is displayed
        self.event_queue.clear()
        # Listen for the user to press enter before continuing
        while True:
            # Iterate through the event queue
            for event in self.event_queue.peek_events():
                # If the user presses a key on the keyboard
                if event.type == pygame.KEYDOWN:
                    # If the user presses "enter", return True
                    if event.key == pygame.K_RETURN:
                        # We remove the event from the queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return


    #*********************************************************************
    #Function Name: draw_play_another_round
    #Purpose: To ask the user if they want to play another round and display "yes" or "no" buttons for their response
    #Parameters: None
    #Return Value: A boolean value indicating whether the user wants to play another round or not
    #Algorithm:

    #1) Create a surface for the prompt with the width and height of the screen
    #2) Render the "play another round?" prompt text on the surface using a specified font
    #3) Load and scale "yes" and "no" button images
    #4) Display the prompt surface with the "yes" and "no" buttons on the screen
    #5) Wait for a mouse event from the user
    #6) If the user clicks on the "yes" button, return True
    #7) If the user clicks on the "no" button, return False
    #Assistance Received: None
    #*********************************************************************
    def draw_play_another_round(self):
        #Set the button sizes
        button_width = 80
        button_height = 80
        #Set the prompt text
        prompt = "Play another round?"
        #Get the width and height of the screen
        width = self.screen.get_width()
        height = self.screen.get_height()
        #Create the surface
        prompt_surface = pygame.Surface((width, height))
        #Fill the surface with a light grey color
        prompt_surface.fill((200, 200, 200))
        #Set the font for the prompt
        prompt_font = pygame.font.SysFont(None, 36)
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2 - 50))
        #Render the prompt text on the surface
        prompt_surface.blit(prompt_text, prompt_rect)

        #Load and scale the "yes" and "no" button images
        yes_button_image = pygame.image.load("yes.png").convert_alpha()
        #Scale the image to the specified button size
        scaled_yes_button_image = pygame.transform.scale(yes_button_image, (button_width, button_height))
        yes_button_rect = scaled_yes_button_image.get_rect()
        #Set the top left corner for the hitbox
        yes_button_rect.topleft = (width // 2 - button_width - 50, height // 2)


        #Load and scale the "no" button image
        no_button_image = pygame.image.load("no.png").convert_alpha()
        #Scale the image to the specified button size
        scaled_no_button_image = pygame.transform.scale(no_button_image, (button_width, button_height))
        no_button_rect = scaled_no_button_image.get_rect()
        # Set the top left corner for the hitbox
        no_button_rect.topleft = (width // 2 + 50, height // 2)

        prompt_surface.blit(scaled_yes_button_image, yes_button_rect)
        prompt_surface.blit(scaled_no_button_image, no_button_rect)

        #Display the prompt surface on the screen
        self.screen.blit(prompt_surface, (0, 0))

        pygame.display.flip()

        #Clear the event queue to prevent the user from pressing a key before the prompt is displayed
        self.event_queue.clear()
        while True:
            #Iterate through the event queue
            for event in self.event_queue.peek_events():
                #If the user clicks on the screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If the user clicks on the "yes" button, return True
                    if yes_button_rect.collidepoint(event.pos):
                        print('N')
                        #We remove the event from the queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return True
                    #If the user clicks on the "no" button, return False
                    elif no_button_rect.collidepoint(event.pos):
                        print('Y')
                        #We remove the event from the queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return False



    #*********************************************************************
    #Function Name: draw_prompt_time_delay
    #Purpose: To display a prompt on the screen for a specified amount of time
    #Parameters:

    #prompt, a string. It holds the text to be displayed as the prompt
    #display_time, a float. It refers to the time in seconds to display the prompt
    #Return Value: None
    #Algorithm:

    #1) Create a surface for the prompt with the width and height of the screen
    #2) Render the prompt text on the surface using a specified font
    #3) Display the prompt surface on the screen
    #4) Wait for the specified amount of time before removing the prompt from the screen
    #Assistance Received: None
    #*********************************************************************
    def draw_prompt_time_delay(self, prompt:str, display_time=3):

        #Get the width and height of the screen
        width = self.screen.get_width()
        height = (self.screen.get_height()-10) / 5
        #Create the surface
        prompt_surface = pygame.Surface((width, height))
        #Fill the surface with a light grey color
        prompt_surface.fill((200, 200, 200))
        #Set the font for the prompt
        prompt_font = pygame.font.SysFont(None, 24)
        #Render the prompt text on the surface
        prompt_text = prompt_font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2))
        #Render the prompt text on the surface
        prompt_surface.blit(prompt_text, prompt_rect)

        #Display the prompt surface on the screen
        self.screen.blit(prompt_surface, (0, int(self.screen.get_height()//5*3-5)))
        pygame.display.flip()
        #Wait for the specified amount of time before removing the prompt from the screen
        sleep(display_time)

    #*********************************************************************
    #Function Name: draw_move
    #Purpose: To display the tiles on the screen and handle user input events
    #Parameters:

    #self, the instance of the object calling this function
    #players, a list of player objects. It holds the information about all players and their tiles
    #left_tile, a tile object passed by reference. It holds the information about the left tile to be displayed
    #right_tile, a tile object passed by reference. It holds the information about the right tile to be displayed
    #Return Value: A boolean value indicating whether the user has pressed the enter key or the escape key
    #Algorithm:

    #1) If players and right_tile are not None, search for the right_tile in all players' stacks and get its index
    #We do this because we want to shift the screen to the area where the tile is in the stacks so the user can see the move
    #2) Calculate the stack_offset using the index and draw all stacks on the screen
    #3) If players and left_tile are not None, search for the left_tile in all players' hands and get its index
    #4) Calculate the hand_offset using the index and draw the hand on the screen
    # We do this to shift the screen to the area where the tile is in the hand is so the user can see the move
    #5) Load and display the right arrow button on the screen
    #6) Display the left and right tiles on the screen
    #7) Handle the user input events and return a boolean value based on whether the user has pressed the enter key
    #or the escape key to confirm or cancel the move respectively
    #Assistance Received: None
    #*********************************************************************
    def draw_move(self, players=None, left_tile=None, right_tile="None"):
        #If players and right_tile are not None, search for the right_tile in all players' stacks and get its index
        #We do this so we can skip to the area where the tile is in the stacks so the user can see the move
        if players != None and str(right_tile) != "None":
            #Set Stack to None
            stack_tile_index = None
            #Set Index to 0
            index = 0
            #Iterate through the players and their stacks to find the right tile
            #Iterate through the players
            for c_player in players:
                #Iterate through the stack
                for c_tile in c_player.get_stack():
                    #If the tile is found, set the stack_tile_index to the index of the tile
                    if str(c_tile) == str(right_tile):
                        #Set the stack_tile_index to the index of the tile
                        stack_tile_index = index
                        #Break out of the inner loop
                        break
                    #Increment the index
                    index += 1
                #If the tile is found, break out of the outer loop
                if stack_tile_index != None:
                    break
            #Calculate the stack_offset using the index and draw all stacks on the screen
            self.stack_offset = stack_tile_index // 9
            self.draw_all_stacks(players)

        #If players and left_tile are not None, search for the left_tile in all players' hands and get its index
        #We do this so we can skip to the area where the tile is in the hand so the user can see the move
        if players != None and str(left_tile) != "None":
            #Set Hand to None
            hand_tile_index = None
            #Iterate through the players and their hands to find the left tile
            for c_player in players:
                #Set Index to 0
                index = 0
                # Iterate through the hand
                for c_tile in c_player.get_hand():
                    # If the tile is found, set the hand_tile_index to the index of the tile
                    if str(c_tile) == str(left_tile):
                        hand_tile_index = index
                        player_hand = c_player.get_hand()
                        # Break out of the inner loop
                        break
                    # Increment the index
                    index += 1
                # If the tile is found, break out of the outer loop
                if hand_tile_index != None:
                    break
            #Calculate and set the hand_offset using the index and draw the hand on the screen
            self.hand_offset = hand_tile_index // 3
            #Draw the hand
            self.draw_hand(player_hand)


        #Load and display the right arrow button on the screen
        button_width = 45
        button_height = 45

        #Load the right arrow image
        right_arrow = pygame.image.load("right-arrow.png").convert_alpha()
        #Scale the image to the specified width and height
        right_arrow_button_image = pygame.transform.scale(right_arrow, (button_width, button_height))
        #Get the rectangle of the image
        right_arrow_rect = right_arrow_button_image.get_rect()
        #Set the top left corner of the rectangle to the specified coordinates for the hitbox
        right_arrow_rect.topleft = ((self.screen.get_width())/2-25, 60)

        #Get the width and height of the screen and create a surface to draw the tiles on
        width = self.screen.get_width()
        height = (self.screen.get_height()-10) / 5
        #Create a surface to draw the tiles on
        tiles_surface = pygame.Surface((width, height))
        #Fill the surface with a light gray color
        tiles_surface.fill((200, 200, 200))
        #Draw the surface on the screen
        tiles_surface.blit(right_arrow_button_image, right_arrow_rect)

        #Set the padding width and hegiht of the tiles
        padding = 10
        tile_width = (self.screen.get_width() - padding*3-padding) // 3
        tile_height = ((self.screen.get_height() - padding*3*4) // 5)


        #Set the hitboxes for the left and right tiles
        left_x = padding
        y = padding
        screen_x = left_x
        screen_y = y
        t_rect = left_tile.get_rect()
        left_tile.draw_tile(tiles_surface, tile_width, tile_height, left_x, y, screen_x, screen_y)
        left_tile.set_rect(t_rect)
        #If the right tile is not None, draw it on the screen
        if str(right_tile) != "None":
            right_x = tile_width * 2 + padding * 3
            t_rect = right_tile.get_rect()
            right_tile.draw_tile(tiles_surface, tile_width, tile_height, right_x, y, screen_x, screen_y)
            right_tile.set_rect(t_rect)
        self.screen.blit(tiles_surface, (0, int(self.screen.get_height()//5*3-5)))
        pygame.display.flip()
        #If the right tile is not None, this is a complete move we need to wait for the user to press
        # enter or escape to confirm or cancel the move only if it is the player's turn
        if str(right_tile) is not "None":
            #Clear the event queue so we don't get any events from before the prompt is displayed
            self.event_queue.clear()
            #Wait for the user to press enter or escape
            while True:
                #Iterate through the events in the event queue
                for event in self.event_queue.peek_events():
                    #If the event is a keydown event
                    if event.type == pygame.KEYDOWN:
                        #If the key is the enter key
                        if event.key == pygame.K_RETURN:
                            print('Enter')
                            #Remove the event from the event queue so it doesn't get processed again
                            if event in self.event_queue:
                                self.event_queue.pop(self.event_queue.index(event))
                            return True
                        #If the key is the escape key
                        if event.key == pygame.K_ESCAPE and self.player_move:
                            print('Escape')
                            #Remove the event from the event queue so it doesn't get processed again
                            if event in self.event_queue:
                                self.event_queue.pop(self.event_queue.index(event))
                            return False

    #*********************************************************************
    #Function Name: wait_for_enter
    #Purpose: To wait for the user to press the enter key and handle the event
    #Parameters:

    #self, the instance of the object calling this function
    #Return Value: A boolean value indicating whether the user has pressed the enter key
    #Algorithm:

    #1) Clear the event queue
    #2) Continuously check for new events in the queue
    #3) If a KEYDOWN event is detected, check if the key is the enter key
    #4) If the enter key is pressed, remove the event from the queue and return True
    #Assistance Received: None
    #*********************************************************************
    def wait_for_enter(self):
        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        #Wait for the user to press enter or escape
        while True:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.KEYDOWN:
                    #If the key is the enter key
                    if event.key == pygame.K_RETURN:
                        print('Enter')
                        #Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return

    #*********************************************************************
    #Function Name: draw_scores
    #Purpose: To display the scores in a table format on the screen
    #Parameters:

    #self, the instance of the object calling this function
    #ict, a dictionary passed by reference. It holds the player ID and score as key-value pairs
    #key_col_name, a string. It refers to the header for the column holding the player IDs
    #val_col_name, a string. It refers to the header for the column holding the player scores
    #header, a string. It refers to the header for the entire table
    #Return Value: None
    #Algorithm:

    #1) Clear the screen and fill it with black color
    #2) Render the title of the table
    #3) Render the headers of the two columns
    #4) Render the player IDs and scores in their respective columns
    #5) Update the display and wait for the user to press the enter key to continue
    #Assistance Received: None
    #*********************************************************************
    def draw_scores(self, dict, key_col_name, val_col_name, header):
        #Clear the screen and fill it with black color
        self.screen.fill((0, 0, 0))
        #Set the x coordinates for the two columns
        col1_x = self.screen.get_width() // 4
        col2_x = self.screen.get_width() * 3 // 4
        #Render the title of the table
        title_font = pygame.font.SysFont(None, 36)
        title_text = header
        title_color = (255, 255, 255)
        title_surface = title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 20))
        self.screen.blit(title_surface, title_rect)

        #Set the render attributes for the column
        header_font = pygame.font.SysFont(None, 24)
        header_text = [key_col_name, val_col_name]
        header_color = (255, 255, 255)
        header_height = 60


        #Render the headers of the two columns
        for i, text in enumerate(header_text):
            #Render the header text
            header_surface = header_font.render(text, True, header_color)
            #Get the rectangle for the header text
            header_rect = header_surface.get_rect()
            #Set the x coordinate of the header text
            header_rect.midtop = (col1_x if i == 0 else col2_x, title_rect.bottom + 10)
            #Draw the header text on the screen
            self.screen.blit(header_surface, header_rect)

        #Set the font
        content_font = pygame.font.SysFont(None, 20)
        #Set the color of the text
        content_color = (255, 255, 255)
        #Set the height of the rows
        row_height = 30


        #Render the player IDs and scores in their respective columns
        for index, (player_id, player_score) in enumerate(dict.items()):
            #Render the player ID
            player_id_surface = content_font.render(str(player_id), True, content_color)
            #Get the rectangle for the player ID
            player_id_rect = player_id_surface.get_rect()
            #Set the hitbox
            player_id_rect.midtop = (col1_x, header_height + index * row_height)
            #Draw the player ID on the screen
            self.screen.blit(player_id_surface, player_id_rect)

            #Render the player score
            score_surface = content_font.render(str(player_score), True, content_color)
            #Get the rectangle for the player score
            score_rect = score_surface.get_rect()
            #Set the hitbox
            score_rect.midtop = (col2_x, header_height + index * row_height)
            #Draw the player score on the screen
            self.screen.blit(score_surface, score_rect)

        #Update the display
        pygame.display.flip()
        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        #Wait for the user to press enter
        while True:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.KEYDOWN:
                    #If the key is the enter key
                    if event.key == pygame.K_RETURN:
                        print('Enter')
                        #Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return


    #*********************************************************************
    #Function Name: start_game_screen
    #Purpose: To display the start game screen and wait for the player to start the game
    #Parameters: None
    #Return Value: None
    #Algorithm:

    #1) Load and display background image
    #2) Load and display start button image
    #3) Wait for player to click the start button
    #Assistance Received: None
    #*********************************************************************
    def start_game_screen(self):
        #Load and display background image
        background_image = pygame.image.load("background.jpg").convert()
        #Scale the background image to fit the screen
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())

        #Load and display start button image
        start_button_image = pygame.image.load("start_button.png").convert_alpha()
        #Scale the start button image to fit the screen
        button_width = round(self.screen.get_size()[0] * 0.3)
        button_height = round(self.screen.get_size()[1] * 0.2)
        #Scale the start button image to fit the screen
        scaled_start_button_image = pygame.transform.scale(start_button_image, (button_width, button_height))
        #Get the rectangle for the start button
        self.start_button_rect = scaled_start_button_image.get_rect()
        #Set the center of the start button
        self.start_button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        #Display the background image and start button image
        self.screen.blit(scaled_background_image, (0, 0))
        #Display the start button image
        self.screen.blit(scaled_start_button_image, self.start_button_rect)

        #Update the display
        pygame.display.flip()
        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        #Wait for the user to press enter
        while True:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If the key is the enter key
                    if self.start_button_rect.collidepoint(event.pos):
                        check = False
                        # Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return
    def gray_screen(self):
        width = self.screen.get_width()
        height = (self.screen.get_height())
        prompt_surface = pygame.Surface((width, height))
        prompt_surface.fill((200, 200, 200))
        self.screen.blit(prompt_surface, (0, 0))
        pygame.display.flip()


    #*********************************************************************
    #Function Name: game_config_screen_players
    #Purpose: Display a screen to configure the number of players in the game
    #Parameters: None
    #Return Value: An integer representing the number of players selected (2 or 4)
    #Algorithm:

    #1) Display a screen with two buttons, one for two players and one for four players
    #2) Wait for user interaction with the buttons
    #3) Return the number of players selected by the user (2 or 4)
    #Assistance Received: None
    #*********************************************************************
    def game_config_screen_players(self):
        #Set the button width and height
        button_width = 70
        button_height = 70


        #Load and display background image
        width = self.screen.get_width()
        height = self.screen.get_height()
        #Load and display background image
        background_image = pygame.image.load("background.jpg").convert()
        #Scale the background image to fit the screen
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())
        #Display the background image
        self.screen.blit(scaled_background_image, (0, 0))

        #Load and display start button image
        prompt_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

        #Load and display four player button image
        four_player = pygame.image.load("4.png").convert_alpha()
        #Scale the four player image to fit the screen
        scaled_four_player_button_image = pygame.transform.scale(four_player, (button_width, button_height))
        #Get the rectangle for the four player button
        four_player_button_rect = scaled_four_player_button_image.get_rect()
        #Set the center of the four player button
        four_player_button_rect.center = (width // 2 - button_width // 2 - button_width, height // 2)

        #Load and display two player button image
        two_player_button_image = pygame.image.load("2.png").convert_alpha()
        #Scale the two player image to fit the screen
        scaled_two_player_button_image = pygame.transform.scale(two_player_button_image, (button_width, button_height))
        #Get the rectangle for the two player button
        two_player_button_rect = scaled_two_player_button_image.get_rect()
        #Set the center of the two player button for the hitbox
        two_player_button_rect.center = (width // 2 + button_width // 2 + button_width, height // 2)

        #Display the four player button image
        prompt_surface.blit(scaled_four_player_button_image, four_player_button_rect)
        prompt_surface.blit(scaled_two_player_button_image, two_player_button_rect)


        #Display the background image and start button image
        self.screen.blit(prompt_surface, (0, 0))

        #Update the display
        pygame.display.flip()


        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        #Wait for the user to press click one of the buttons
        while True:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If the key is the enter key
                    if four_player_button_rect.collidepoint(event.pos):
                        print('Two players selected')
                        # Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return 2

                    #If the key is the enter key
                    elif two_player_button_rect.collidepoint(event.pos):
                        print('Four players selected')
                        # Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return 4

    #*********************************************************************
    #Function Name: ask_player_type
    #Purpose: To display a prompt asking the user to select the type of player they want to create (human or computer)
    #Parameters: None
    #Return Value: A string representing the type of player selected by the user ("Human" or "Computer")
    #Algorithm:

    #1) Set the button width and height
    #2) Load and display background image
    #3) Load and display start button image
    #4) Display "Human" text box
    #5) Display "Computer" text box
    #6) Load and display human.png image
    #7) Load and display computer.png image
    #8) Display the prompt "Which player type would you like to create?"
    #9) Wait for the user to press click one of the buttons
    #10) If the user selects "Human", return "Human". If the user selects "Computer", return "Computer"
    #Assistance Received: None
    #*********************************************************************

    def ask_player_type(self):
        # Set the button width and height
        button_width = 70
        button_height = 70

        # Load and display background image
        width = self.screen.get_width()
        height = self.screen.get_height()
        # Load and display background image
        background_image = pygame.image.load("background.jpg").convert()
        # Scale the background image to fit the screen
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())
        # Display the background image
        self.screen.blit(scaled_background_image, (0, 0))

        # Load and display start button image
        prompt_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

        # Display "Human" text box
        human_text = pygame.font.Font(None, 20)
        human_text_surface = human_text.render("Human", True, (255, 255, 255))
        human_text_rect = human_text_surface.get_rect()
        human_text_rect.center = (width // 2 - button_width // 2 - button_width, height // 2 + button_height + 20)

        # Display "Computer" text box
        computer_text = pygame.font.Font(None, 20)
        computer_text_surface = computer_text.render("Computer", True, (255, 255, 255))
        computer_text_rect = computer_text_surface.get_rect()
        computer_text_rect.center = (width // 2 + button_width // 2 + button_width, height // 2 + button_height + 20)

        # Load and display human.png image
        human_image = pygame.image.load("human.png").convert_alpha()
        # Scale the human image to fit the screen
        scaled_human_image = pygame.transform.scale(human_image, (button_width, button_height))
        # Get the rectangle for the human image
        human_image_rect = scaled_human_image.get_rect()
        # Set the center of the human image
        human_image_rect.center = (width // 2 - button_width // 2 - button_width, height // 2)

        # Load and display computer.png image
        computer_image = pygame.image.load("robot.png").convert_alpha()
        # Scale the computer image to fit the screen
        scaled_computer_image = pygame.transform.scale(computer_image, (button_width, button_height))
        # Get the rectangle for the computer image
        computer_image_rect = scaled_computer_image.get_rect()
        # Set the center of the computer image
        computer_image_rect.center = (width // 2 + button_width // 2 + button_width, height // 2)


        #Create the surfaces for the computer and human text boxes
        human_text_background = pygame.Surface((human_text_rect.width, human_text_rect.height))
        #Fill the background of the surfaces with black
        human_text_background.fill((0, 0, 0))
        #Create the surfaces for the computer text boxe
        computer_text_background = pygame.Surface((computer_text_rect.width, computer_text_rect.height))
        #Fill the background of the surfaces with black
        computer_text_background.fill((0, 0, 0))
        #Render the text and backgrounds
        prompt_surface.blit(human_text_background, human_text_rect)
        prompt_surface.blit(human_text_surface, human_text_rect)
        prompt_surface.blit(computer_text_background, computer_text_rect)
        prompt_surface.blit(computer_text_surface, computer_text_rect)
        prompt_surface.blit(scaled_human_image, human_image_rect)
        prompt_surface.blit(scaled_computer_image, computer_image_rect)

        # render the prompt "Which player type would you like to create?"
        prompt_text = pygame.font.Font(None, 20)
        prompt_text_surface = prompt_text.render("Which player type would you like to create?", True, (255, 255, 255))
        prompt_text_rect = prompt_text_surface.get_rect()
        prompt_text_rect.center = (width // 2, height // 2 - button_height - 40)

        # Create a black surface for the background of the text
        black_surface = pygame.Surface((prompt_text_rect.width, prompt_text_rect.height))
        black_surface.fill((0, 0, 0))

        # Render the black surface and text surface onto the prompt surface
        prompt_surface.blit(black_surface, prompt_text_rect)
        prompt_surface.blit(prompt_text_surface, prompt_text_rect)

        # Display the all the surfaces
        self.screen.blit(prompt_surface, (0, 0))

        # Update the display
        pygame.display.flip()

        # Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        # Wait for the user to press click one of the buttons
        while True:
            # Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                # If the event is a keydown event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the key is the enter key
                    if human_text_rect.collidepoint(event.pos) or human_image_rect.collidepoint(event.pos):
                        print("Human selected")
                        # Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return "Human"

                    # If the key is the enter key
                    elif computer_text_rect.collidepoint(event.pos) or computer_image_rect.collidepoint(event.pos):
                        print("Computer selected")
                        # Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                        return "Computer"

        #*********************************************************************
    #Function Name: input_number_screen
    #Purpose: To allow the user to input the number of sets to be played in the game
    #Parameters: None
    #Return Value: The number of sets to be played, an integer
    #Algorithm:

    #1) Display a text prompt on the screen asking the user to enter the number of sets they want to play
    #2) Create an input box where the user can enter their number
    #3) Check if the input is valid (an integer greater than 5)
    #4) If the input is not valid, display an error message
    #5) Repeat the process until a valid input is provided
    #6) Return the number of sets
    #Assistance Received: None
    #*********************************************************************
    def input_number_screen(self):
        #Set the button width and height
        width = self.screen.get_width()
        height = self.screen.get_height()
        #Load and display background image
        background_image = pygame.image.load("background.jpg").convert()
        #Scale the background image to fit the screen
        scaled_background_image = pygame.transform.scale(background_image, self.screen.get_size())
        #Display the background image
        self.screen.blit(scaled_background_image, (0, 0))

        #Load and Display the font
        font = pygame.font.Font(None, 24)
        #Create the input box
        input_box = pygame.Rect(width // 2 - 100, height // 2 - 20, 200, 40)
        #Set the color of the input box
        color_inactive = pygame.Color('gray')
        color_active = pygame.Color('black')
        color = color_inactive
        #Set the active state of the input box, meaning whether it is clicked or not
        active = False
        #Set the text in the input box
        text = ''
        #Set done to false
        done = False
        #Set the error message to false
        error_message = False


        #Display the text prompt
        prompt_text = "What length would you like the double sets?"
        prompt_surface = font.render(prompt_text, True, pygame.Color('black'))
        prompt_rect = prompt_surface.get_rect(center=(width // 2, height // 2 - 60))

        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        while not done:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If the mouse is clicked on the input box set active to true
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                    # Remove the event from the event queue so it doesn't get processed again
                    if event in self.event_queue:
                        self.event_queue.pop(self.event_queue.index(event))
                #If the event is a keydown event and active is true
                if event.type == pygame.KEYDOWN and active:
                    #If active
                    if active:
                        #If the key is the enter ke
                        if event.key == pygame.K_RETURN:
                            try:
                                #Try to convert the text to an integer
                                number = int(text)
                                #If the number is less than 5, display an error message
                                if number < 5:
                                    error_surface = font.render("Please enter only numbers greater than 5", True, pygame.Color('red'))
                                    error_rect = error_surface.get_rect(center=(width // 2, height // 2 + 40))
                                    error_message = True
                                else:
                                    done = True
                            #If the text cannot be converted to an integer, display an error message
                            except ValueError:
                                text = ''
                                error_surface = font.render("Please enter only numbers", True, pygame.Color('red'))
                                error_rect = error_surface.get_rect(center=(width // 2, height // 2 + 40))
                                error_message = True
                                done = False
                        #If the key is the backspace key, remove the last character from the text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                            error_message = False
                        #If the key is any other key, add the character to the text
                        else:
                            text += event.unicode
                # Remove the event from the event queue so it doesn't get processed again
                if event in self.event_queue:
                    self.event_queue.pop(self.event_queue.index(event))

            #Update the display with the new text continuously
            self.screen.blit(scaled_background_image, (0, 0))
            self.screen.blit(prompt_surface, prompt_rect)
            txt_surface = font.render(text, True, pygame.Color('white'))
            width_box = max(200, txt_surface.get_width() + 10)
            input_box.w = width_box
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.draw.rect(self.screen, pygame.Color('black'), input_box)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            #Display the error message if there is one
            if error_message:
                self.screen.blit(error_surface, error_rect)
            #Update the display
            pygame.display.flip()

        return number

    #*********************************************************************
    #Function Name: stack_scroll
    #Purpose: To handle the scrolling of game stacks and selecting a tile from a stack
    #Parameters:

    #players, an array passed by reference. It holds individual players and their stack of tiles
    #Return Value: None
    #Algorithm:

    #1) Listen for events of keyboard or mouse input
    #2) If a right arrow key is pressed, increase the stack offset and redraw the stacks
    #3) If a left arrow key is pressed, decrease the stack offset and redraw the stacks
    #4) If a mouse click is detected, loop through the stacks of all players and check if any tile's rect is clicked
    #If a tile's rect is clicked, set that tile as selected and return
    #Assistance Received: None
    #*********************************************************************
    def stack_scroll(self, players):
        #Clear the event queue so we don't get any events from before the prompt is displayed
        self.event_queue.clear()
        #Listen for inputs on the stack
        while True:
            #ITerate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a keydown event
                if event.type == pygame.KEYDOWN:
                    #If the right arrow key is pressed, increase the stack offset and redraw the stacks
                    if event.key == pygame.K_RIGHT:
                        print('RIGHT')
                        #Increase the stack offset
                        self.stack_offset += 1
                        #Redraw the stacks
                        self.draw_all_stacks(players)
                        #Update the display
                        pygame.display.flip()
                        #Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                    #If the left arrow key is pressed, decrease the stack offset and redraw the stacks
                    if event.key == pygame.K_LEFT:
                        print('LEFT')
                        #Decrease the stack offset
                        self.stack_offset -= 1
                        #Redraw the stacks
                        self.draw_all_stacks(players)
                        #Update the display
                        pygame.display.flip()
                        #Remove the event from the event queue so it doesn't get processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                #If the event is a mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Iterate through the stacks of all players
                    for c_player in players:
                        #Iterate through the tiles in the current player's stack
                        for tile in c_player.get_stack():
                            #If the tile has a rect(It is currently displayed)
                            if tile.get_rect() != None:
                                #If the tile's rect is clicked
                                if tile.get_rect().collidepoint(event.pos):
                                    #If the stack select flag is set, loop through the stack and deselect all other
                                    #tiles to prevent false positives.
                                    if self.stack_select:
                                        for tile_ in c_player.get_stack():
                                            #Set tile selected to true so that it will be selected within the game
                                            tile_.selected = False
                                        tile.set_selected(True)
                                        print(tile)
                                        return
                                        #Remove the event from the event queue so it doesn't get processed again
                                    if event in self.event_queue:
                                        self.event_queue.pop(self.event_queue.index(event))
    #*********************************************************************
    #Function Name: draw_hand
    #Purpose: To draw the hand of tiles in a given screen
    #Parameters:

    #hand[], an array passed by value. It holds the tiles in the hand.
    #Return Value: None
    #Algorithm:

    #1) Calculate the size and position of each tile based on the screen size and the number of tiles per row.
    #2) Create a surface for the tiles and fill it with a specific color.
    #3) Draw each tile in the hand on the surface.
    #4) Draw the surface onto the screen.
    #5) Reset the rectangles of tiles that are not displayed on the screen.
    #Assistance Received: None
    #*********************************************************************
    def draw_hand(self, hand):

        #Set the total rows
        total_rows = 1
        #Set the padding between tiles
        padding = 10
        #Set the number of tiles per row
        tiles_per_row = 3
        #Calculate the size of each tile
        tile_width = (self.screen.get_width() - padding*tiles_per_row-padding) // tiles_per_row
        tile_height = (self.screen.get_height() - padding*total_rows-padding) // 5

        #Set the font size
        font_size = 36
        #Set the font
        font = pygame.font.SysFont(None, font_size)
        #Set the max offset
        max_offset = (len(hand) // tiles_per_row)
        #Make sure the offset does not dip below 0 and does not exceed the max offset
        if self.hand_offset > max_offset:
            self.hand_offset = max_offset
        if self.hand_offset < 0:
            self.hand_offset = 0
        #Calculate the start and end index of the tiles to be displayed based on the offset
        start_index = self.hand_offset * tiles_per_row * total_rows
        end_index = start_index + tiles_per_row * total_rows

        #Create a surface for the tiles and fill it with a specific color
        tiles_surface = pygame.Surface((self.screen.get_width(), tile_height+padding*2))
        #Set the tiles surface to be light gray
        tiles_surface.fill((200, 200, 200))

        #We keep track of the number of tiles drawn so that we can calculate whether this should be on the left, middle
        #or right
        #Set the number of tiles drawn to 0
        i = 0
        #Iterate through the tiles in the hand and display them
        for tile in hand[start_index:end_index]:
            x = padding + (i % tiles_per_row) * (tile_width + padding)
            y = ((i // tiles_per_row) * (tile_height + padding))+padding
            screen_x = x
            screen_y = self.screen.get_height() - tiles_surface.get_height() + y
            tile.draw_tile(tiles_surface, tile_width, tile_height, x, y, screen_x, screen_y)
            #Increment the number of tiles drawn
            i += 1
        #Draw the surface onto the screen
        self.screen.blit(tiles_surface, (0, self.screen.get_height() - tiles_surface.get_height()))
        #Update the display
        pygame.display.flip()
        #Reset the rectangles of tiles that are not displayed on the screen so they are not clickable
        for tile in hand[0:start_index]:
            tile.set_rect(None)
        for tile in hand[end_index:]:
            tile.set_rect(None)

    #*********************************************************************
    #Function Name: hand_listener
    #Purpose: To listen for events related to the hand and respond to them
    #Parameters:

    #hand[], an array passed by value. It holds individual tiles in the hand
    #Return Value: None
    #Algorithm:

    #1) Clear the event queue
    #2) Listen for events related to the hand
        #a) If the event is a KEYDOWN event
        #i) If the key is 'UP', increment the hand offset and redraw the hand
        #ii) If the key is 'DOWN', decrement the hand offset and redraw the hand
    #b) If the event is a MOUSEBUTTONDOWN event
        #i) Check if the mouse click collides with any of the tiles in the hand
        #ii) If a collision occurs, set the selected tile and return
    #Assistance Received: None
    #*********************************************************************
    def hand_listener(self, hand):
        #Clear the event queue so that we don't process events that have already been processed
        self.event_queue.clear()
        #Listen for events related to the hand
        while True:
            #Iterate through the events in the event queue
            for event in self.event_queue.peek_events():
                #If the event is a KEYDOWN event
                if event.type == pygame.KEYDOWN:
                    #If the key is 'UP', increment the hand offset and redraw the hand
                    if event.key == pygame.K_UP:
                        print('UP')
                        #Increment the hand offset
                        self.hand_offset += 1
                        #Redraw the hand
                        self.draw_hand(hand)
                        #Update the display
                        pygame.display.flip()
                        #Remove the event from the event queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                    #If the key is 'DOWN', decrement the hand offset and redraw the hand
                    if event.key == pygame.K_DOWN:
                        print('DOWN')
                        #Decrement the hand offset
                        self.hand_offset -= 1
                        #Redraw the hand
                        self.draw_hand(hand)
                        #Update the display
                        pygame.display.flip()
                        #Remove the event from the event queue so that it is not processed again
                        if event in self.event_queue:
                            self.event_queue.pop(self.event_queue.index(event))
                #If the event is a MOUSEBUTTONDOWN event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Check if the mouse click collides with any of the tiles in the hand
                    for tile in hand:
                        #If the tile has a hitbox, check if the mouse click it
                        if tile.get_rect() != None:
                            #If the mouse click the tile, set the selected tile and return, also result all other tiles
                            #to false to prevent any false positives
                            if tile.get_rect().collidepoint(event.pos) and self.hand_select:
                                #Set all tiles to not selected to prevent any false positives
                                for tile_ in hand:
                                    tile_.selected = False
                                #Set the selected tile to true
                                tile.set_selected(True)
                                print(tile)
                                #Remove the event from the event queue so that it is not processed again
                                if event in self.event_queue:
                                    self.event_queue.pop(self.event_queue.index(event))
                                return
class DisplayTile:

    def __init__(self):
        #The rect is the hitbox
        self.rect = None
        #Whether the tile has been selected or not
        self.selected = False

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    #*********************************************************************
    #Function Name: draw_tile
    #Purpose: To draw a single tile on the screen with the given specifications
    #Parameters:

    #screen, a Pygame screen object passed by reference. The tile will be drawn on this screen.
    #width, an integer. The width of the tile to be drawn.
    #height, an integer. The height of the tile to be drawn.
    #x, an integer. The x-coordinate on the screen where the top-left corner of the tile will be drawn.
    #y, an integer. The y-coordinate on the screen where the top-left corner of the tile will be drawn.
    #screen_x, an integer. The x-coordinate on the screen where the top-left corner of the tile will be drawn.
    #screen_y, an integer. The y-coordinate on the screen where the top-left corner of the tile will be drawn.
    #Return Value: None
    #Algorithm:

    #1) Determine the primary and alternate colors for the tile based on the color of the player.
    #2) Create a Pygame surface for the tile with the given width and height and fill it with the primary color.
    #3) Draw a line across the tile surface with the alternate color.
    #4) Render the top and bottom numbers of the tile and blit them on the tile surface.
    #5) Blit the tile surface on the screen at the given x and y coordinates.
    #6) Update the Pygame display.
    #7) Store the rectangle of the tile with its position and size.
    #Assistance Received: None
    #*********************************************************************
    def draw_tile(self, screen, width,height, x, y, screen_x, screen_y):
        #Determine the primary and alternate colors for the tile based on the color of the player
        if self.player.get_color() == "B":
            primary_color = (0, 0, 0)
            alt_color = (255, 255, 255)
        elif self.player.get_color() == "R":
            primary_color = (255, 96, 96)
            alt_color = (0, 0, 0)
        elif self.player.get_color() == "G":
            primary_color = (96, 255, 95)
            alt_color = (0, 0, 0)
        else:
            primary_color = (255, 255, 255)
            alt_color = (0, 0, 0)
        #Set the tile width and height
        TILE_WIDTH = width
        TILE_HEIGHT = height

        #Set the font size
        font_size = 30
        #Set the font style
        font = pygame.font.SysFont('Arial', font_size)
        #Create a Pygame surface for the tile with the given width and height and fill it with the primary color
        tile_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        #Set the tiles primary color
        tile_surface.fill(primary_color)
        #Draw a line across the tile surface with the alternate color
        pygame.draw.line(tile_surface, alt_color, (0, TILE_HEIGHT // 2), (TILE_WIDTH, TILE_HEIGHT // 2), 2)
        #Render the top and bottom numbers of the tile and blit them on the tile surface with the alternate color
        top_num = font.render(str(self.left), True, alt_color)
        #Set the top number center position
        top_num_center = (TILE_WIDTH // 3, 0)
        #Render the bottom number with the alternate color
        bottom_num = font.render(str(self.right), True, alt_color)
        #Set the bottom number center position
        bottom_num_center = (TILE_WIDTH // 3, TILE_HEIGHT-bottom_num.get_height())
        #Render the top and bottom numbers on the tile surface
        tile_surface.blit(top_num, top_num_center)
        tile_surface.blit(bottom_num, bottom_num_center)
        screen.blit(tile_surface, (x, y))
        #Update the Pygame display
        pygame.display.flip()
        #Store the rectangle of the tile with its position and size
        self.rect = pygame.rect.Rect(screen_x, screen_y, TILE_WIDTH, TILE_HEIGHT)
