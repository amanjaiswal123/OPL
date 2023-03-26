import os
from random import shuffle
import pygame.display
from gui import DisplayTile, board_display
from time import sleep
from threading import Thread




class Player():
    # The player class is used to create a player object. The player object is used to store the player's data including
    #  their player id, color, boneyard, hand, stacks, score, and rounds won.

    def __init__(self):
        #The playerID is used to identify the player. Primarily used to identify the turn of the player as well as
        #the tile owner within the stacks
        super().__init__()
        #The player's ID used to identify the player
        self.playerID = None
        #The player's color used to identify the player's tiles
        self.color = None
        #The player's boneyard is a list of tile objects in the player's boneyard. A list of tile objects
        self.boneyard = []
        #The player's hand is a list of tile objects inplayer's hand
        self.hand = []
        #The player's stack is a list of tile objects in the stacks
        self.stack = []
        #Represents the score of the player per round. Is reset every new round
        self.score = 0
        #Represents the number of rounds the player has won
        self.rounds_won = 0
        self.rounds_won = 0
        #Used to scroll through the player's hand in gui.hand_listener
        self.hand_offset = 0


    def load_player(self, player_id, color, boneyard, hand, stack, score, rounds_won):
        self.playerID = player_id
        self.color = color
        self.boneyard = boneyard
        self.hand = hand
        self.stack = stack
        self.score = score
        self.rounds_won = rounds_won

    def save_player(self):
        string = ""
        string += "Human:\n"
        string += "   Stacks: "
        for tile_ in self.stack:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Boneyard: "
        for tile_ in self.boneyard:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Hand: "
        for tile_ in self.hand:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Score: " + str(self.score) + "\n"
        string += "   Rounds Won: " + str(self.rounds_won) + "\n"

        return string


    def set_stack(self, stack):
        self.stack = stack

    def add_rounds_won(self):
        self.rounds_won += 1
    def add_score(self, score):
        self.score += score
    def set_color(self, color):
        self.color = color
    def get_player_id(self):
        return self.playerID

    def get_color(self):
        return self.color

    def get_boneyard(self):
        return self.boneyard

    def get_hand(self):
        return self.hand

    def get_stack(self):
        return self.stack

    def get_score(self):
        return self.score

    def get_rounds_won(self):
        return self.rounds_won
    #*********************************************************************
    #Function Name: generate_boneyard
    #Purpose: To create a set of tiles (boneyard) of size n for a given game
    #Parameters:

    #self, a reference to the current instance of the class
    #n, an integer. It refers to the size of the boneyard to be generated
    #Return Value: None
    #Algorithm:

    #1) For x in the range of 0 to n+1:
        #a) For y in the range of 0 to x+1:
            #i) Create a new tile c_tile with coordinates (x, x-y) using the tile constructor
            #ii) Add c_tile to the boneyard list of self
    #Assistance Received: none
    #*********************************************************************
    def generate_boneyard(self, n):
        for x in range(0, n + 1):
            for y in range(0, x + 1):
                c_tile = tile(x, x - y, self)
                self.boneyard.append(c_tile)

    def move_from_boneyard_to_hand_n(self, n):
        for x in range(0, n):
            self.hand.append(self.boneyard.pop(0))

    def move_from_hand_to_stack_n(self, n):
        for x in range(0, n):
            self.stack.append(self.hand.pop(0))
    def assign_player_id(self, ex_player_ids):
        self.playerID = str(len(ex_player_ids) + 1)

    def assign_player_color(self, ex_player_colors):
        valid_colors = ["W", "B", "R", "G"]
        self.color = valid_colors[len(ex_player_colors)]
    #*********************************************************************
    #Function Name: create_new_player
    #Purpose: To create a new player with a unique ID, color, and initial game setup
    #Parameters:

    #self, a reference to the current instance of the class
    #ex_player_ids, a list passed by value. It holds IDs of existing players
    #ex_player_colors, a list passed by value. It holds colors of existing players
    #double_set_length, an integer. It refers to the size of the boneyard to be generated
    #Return Value: None
    #Algorithm:

    #1) Call assign_player_id function with ex_player_ids as input
    #2) Call assign_player_color function with ex_player_colors as input
    #3) Call generate_boneyard function with double_set_length as input
    #4) Initialize self.hand to an empty list
    #5) Call shuffle_boneyard function
    #6) Call move_from_boneyard_to_hand_n function with input 6
    #7) Initialize self.stack to an empty list
    #8) Call move_from_hand_to_stack_n function with input 6
    #9) Set self.score to 0
    #10) Set self.roundsWon to 0
    #Assistance Received: none
    #*********************************************************************
    def create_new_player(self, ex_player_ids, ex_player_colors, double_set_length):
        #Assign a unique player ID
        self.assign_player_id(ex_player_ids)
        #Assign a unique player color
        self.assign_player_color(ex_player_colors)
        #Generate a boneyard of size double_set_length
        self.generate_boneyard(double_set_length)
        #Initialize the player's hand to an empty list
        self.hand = []
        #Shuffle the boneyard
        self.shuffle_boneyard()
        #Move the double set length amount of tiles from the boneyard to the player's hand
        self.move_from_boneyard_to_hand_n(double_set_length)
        #Initialize the player's stack to an empty list
        self.stack = []
        #Move the double set length amount of tiles from the player's hand to the player's stack
        self.move_from_hand_to_stack_n(double_set_length)
        #Set the player's score to 0
        self.score = 0
        #Set the player's rounds won to 0
        self.roundsWon = 0

    def shuffle_boneyard(self):
        shuffle(self.boneyard)

    def display_boneyard(self):
        for x in self.boneyard:
            x.display_tile()
        print()

    def display_hand(self):
        for x in self.hand:
            x.display_tile()
        print()

    def display_stack(self):
        for x in self.stack:
            x.display_tile()
        print()

    def move_from_hand_to_boneyard_n(self, n):
        for x in range(0, n):
            self.boneyard.append(self.hand.pop(0))
    #*********************************************************************
    #Function Name: move_from_hand_to_stack
    #Purpose: To move a tile from the hand to the stack in the game
    #Parameters:

    #self, a reference to the current instance of the class
    #hand_tile, a tile object. It represents the tile to be moved from the hand
    #stack, a list passed by reference. It represents the stack where the tile will be moved to
    #stack_tile, a tile object. It represents the tile on top of the stack where the hand tile will be placed
    #Return Value: None
    #Algorithm:

    #1) Find the index of hand_tile in self.hand
    #2) Replace stack_tile in the stack with hand_tile
    #3) Remove hand_tile from self.hand
    #Assistance Received: none
    #*********************************************************************
    def move_from_hand_to_stack(self, hand_tile, stack, stack_tile):
        #Print the hand tile, stack tile, and the stack
        print("\nHAND TILE:" + str(hand_tile))
        print("\nSTACK TILE"+ str(stack_tile))
        #Find the index of the hand tile in the hand
        tile_index = self.hand.index(hand_tile)
        #Replace the stack tile in the stack with the hand tile
        stack[stack.index(stack_tile)] = self.hand.pop(tile_index)

    #*********************************************************************
    #Function Name: check_valid_move
    #Purpose: To check if a move is valid or not
    #Parameters:

    #self, a reference to the current instance of the class
    #hand_tile, a tile object. It represents the tile to be moved from the hand
    #stack_tile, a tile object. It represents the tile on top of the stack where the hand tile will be placed
    #Return Value: A boolean indicating if the move is valid or not
    #Algorithm:

    #1) If stack_tile is a double and hand_tile is a double, check if hand_tile > stack_tile
    #2) If stack_tile is a double and hand_tile is not a double, check if hand_tile >= stack_tile
    #3) If stack_tile is not a double and hand_tile is a double, the move is valid
    #4) If stack_tile is not a double and hand_tile is not a double, check if hand_tile >= stack_tile
    #Assistance Received: none
    #*********************************************************************
    def check_valid_move(self, hand_tile, stack_tile):
        #By defualt valid_move is false until proven otherwise by the if statements below
        valid_move = False
        if stack_tile.get_double():
            if hand_tile.get_double():
                if hand_tile > stack_tile:
                    #If the hand tile is a double and the stack tile is a double,
                    #we can use it if the hand tuple is greater than the stack tuple
                    valid_move = True
            else:
                if hand_tile >= stack_tile:
                    #If the hand tile is not a double and the stack tile is a double, the hand tile must be greater
                    # than or equal to the stack tile
                    valid_move = True
        else:
            if hand_tile.get_double():
                #If the hand tile is a double and the stack tile is not a double, the move is valid no matter what
                valid_move = True
            else:
                if hand_tile >= stack_tile:
                    #If the hand tile is not a double and the stack tile is not a double, the hand tile must be greater
                    # than or equal to the stack tile
                    valid_move = True
        return valid_move

    #*********************************************************************
    #Function Name: reccomend_move
    #Purpose: To recommend the best move for the current player
    #Parameters:

    #self, a reference to the current instance of the class
    #players, a list of player objects. It represents all the players in the game
    #Return Value: The best move for the current player, represented as a list containing hand_tile, stack, stack_tile, and difference
    #Algorithm:

    #1) For each tile in the players hand, iterate over each player and their stack and check if the move is valid
    #2) If the move is valid, calculate the difference between hand_tile and stack_tile and append the move to a list of valid moves
    #3) Sort the list of valid moves by difference in ascending order
    #4) Check the player ID of the stack_tile. If it is not the current player, recommend the move with the lowest difference
    #5) If all the moves are invalid, return "pass"
    #Assistance Received: none
    #*********************************************************************
    def reccomend_move(self, players):
        valid_moves = []
        #Get all the possible moves by iterating over the hand and stack using the check_valid_move function
        #Iterate over the player's hand
        for hand_tile in self.hand:
            for c_player in players:
                #Iterate over the stack of each player
                for stack_tile in c_player.stack:
                    if self.check_valid_move(hand_tile, stack_tile):
                        #If the move is valid, calculate the difference between the hand tile and the stack tile
                        difference = hand_tile - stack_tile
                        #Append the move to the list of valid moves
                        valid_moves.append([hand_tile, c_player.get_stack(), stack_tile, difference])
        #If there are no valid moves, return "pass"
        if len(valid_moves) == 0:
            return "pass"
        #Sort the list of valid moves by difference in ascending order
        valid_moves.sort(key=lambda x: x[3])
        #By default the best move is the first move in the list as that is the lowest diffrence move
        best_move = valid_moves[0]
        #We iterate through the moves and check if their stack tile is on a opponents stack, which would be preferred
        for move in valid_moves:
            stack_tile = move[2]
            stack_tile_player_id = stack_tile.player.get_player_id()
            #Once the first match is found, we break out of the loop and return the move
            if stack_tile_player_id != self.playerID:
                best_move = move
                break
        #Print the best move
        print("\nThe Best Move is " + str(best_move[0]) + " on " + str(best_move[2]) + " because it has a difference of " + str(best_move[3]) + " which is the lowest difference move on a opponents stack.")
        return best_move

    #*********************************************************************
    #Function Name: ask_to_pass
    #Purpose: To ask the current player if they want to pass their turn
    #Parameters: None
    #Return Value: A boolean value indicating whether the player wants to pass their turn or not
    #Algorithm:

    #1) Get user input for whether the player wants to pass their turn
    #2) If the input is "Y", return True
    #3) If the input is "N", return False
    #4) If the input is neither "Y" nor "N", display an error message and ask for input again
    #Assistance Received: none
    #*********************************************************************

    def ask_to_pass(self):
        user_input = input("Would you like to pass? (Y/N)")
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Error: Please enter Y or N")
            self.ask_to_pass()
    #*********************************************************************
    #Function Name: display_rec_move
    #Purpose: To display the recommended move for the player.
    #Parameters:

    #reccommened_move, a list that contains the recommended move. It has the following structure:
    #- reccommened_move[0] is the hand tile to play
    #- reccommened_move[1] is the stack of the player to play on
    #- reccommened_move[2] is the stack tile to play on
    #- reccommened_move[3] is the difference between the hand tile and the stack tile
    #Return Value: None
    #Algorithm:

    #1) Get the hand tile and the stack tile from the recommended move
    #2) Display the hand tile and stack tile
    #Assistance Received: none
    #*********************************************************************
    def display_rec_move(self, reccommened_move):
        #Display the recommended move
        print("Reccomended Move: ")
        hand_tile = reccommened_move[0]
        stack_tile = reccommened_move[2]
        print("Hand Tile: ", end=": ")
        hand_tile.display_tile()
        print()
        print("Stack Tile: ", end=": ")
        stack_tile.display_tile()
        print()

    #*********************************************************************
    #Function Name: ask_reccomended_move
    #Purpose: To prompt the player to play the recommended move.
    #Parameters:

    #reccommened_move, a list that contains the recommended move. It has the following structure:
    #- reccommened_move[0] is the hand tile to play
    #- reccommened_move[1] is the stack of the player to play on
    #- reccommened_move[2] is the stack tile to play on
    #- reccommened_move[3] is the difference between the hand tile and the stack tile
    #Return Value: None
    #Algorithm:

    #1) Prompt the player to play the recommended move
    #2) If the player chooses to play the move, display the recommended move using the display_rec_move function
    #3) If the player chooses not to play the move, do nothing
    #Assistance Received: none
    #*********************************************************************
    def ask_reccomended_move(self, reccommened_move):
        user_input = input("Would you like to play the reccomended move? (Y/N)")
        if user_input == "Y":
            self.display_rec_move(reccommened_move)
        elif user_input != "N":
            print("Error: Please enter Y or N")
            self.ask_reccomended_move(reccommened_move)


    #*********************************************************************
    #Function Name: get_move
    #Purpose: To get the player's move in the game, including whether they want a recommended move, which tile from their hand and which tile from a stack they want to play, and whether they want to pass.
    #Parameters:

    #players, a list passed by value. It holds all the players in the game and their respective attributes, such as their hand and stack.
    #game_display, an object passed by reference. It holds information about the game's graphics and GUI.
    #Return Value: An array with three elements: the tile from the player's hand they want to play, the stack they want to play it on, and the tile they want to play it on. Alternatively, a string of "pass" may be returned, indicating the player wants to pass.
    #Algorithm:

    #1) Start threads to listen for scrolling on the stacks and the player's hand.
    #2) Use the reccomend_move function to generate a recommended move.(We need it regardless of whether the player
    # wants to use it or not to check if the player can pass)
    #3) Ask the player if they want to use the recommended move.
    #4) Ask the player if they want to pass.
    #5) If the player does not want to pass, wait for them to select a tile from their hand and then a tile from a stack.
    #6) Return the selected tiles.
    #Assistance Received: none
    #*********************************************************************
    def get_move(self, players, game_display):
        #Start threads to listen for scrolling on the stacks
        game_display.set_stack_scroll(True)
        stack_scroll_thread = Thread(target=game_display.stack_scroll, args=[players])
        stack_scroll_thread.start()
        #Start a thread to listen for scrolling on the player's hand
        game_display.set_hand_scroll(True)
        hand_scroll_thread = Thread(target=game_display.hand_listener, args=[self.hand])
        hand_scroll_thread.start()
        #Get the recommended move
        reccommened_move = self.reccomend_move(players)
        #Reset the stack offset to 0 so the player starts from the same place every time
        game_display.set_stack_offset(0)
        #Ask the player if they want to use the recommended move
        rec_move = game_display.draw_yes_no_prompt("Would you like a recommended move?")
        #If the player wants to use the recommended move, display it
        if (len(self.hand) > 0):
            if rec_move:
                #If not pass display normally, else display pass
                if reccommened_move != "pass":
                    rec_hand_tile = reccommened_move[0]
                    rec_stack_tile = reccommened_move[2]
                    #Draw the recommended move
                    game_display.draw_move(players, rec_hand_tile,rec_stack_tile)
                    #Show the reason the computer chose this move
                    prompt = "The computer recommends this move because it has a difference of " + str(
                        rec_hand_tile - rec_stack_tile) \
                             + " Which is the lowest difference after prioritizing opponent tiles"
                    game_display.draw_prompt(prompt)
                else:
                    #Display Pass
                    game_display.draw_prompt_time_delay("PASS")
            #Ask the player if they want to pass
            pass_ = game_display.draw_yes_no_prompt("Would you like to pass?")
            #If the player does not want to pass, get the tiles they want to play,
            if not pass_:
                game_display.set_hand_select(True)
                print("Please enter a tile from your hand: ")


                #Wait for the player to select a tile from their hand, we iterate through the hand and the hand_listener will
                #set the selected attribute to true if the player selects a tile

                #By default, the selected tile is false, until a tile is selected. When it is stop the loop
                selected_tile = False
                while not selected_tile:
                    #Iterate through the player's hand
                    for tile in self.hand:
                        #If the tile is selected, set the hand_tile to that tile and break out of the loop
                        if tile.get_selected():
                            #Set the hand tile to the selected tile
                            hand_tile = tile
                            #Reset the selected attribute to false to make sure it isn't selected next turn.
                            tile.set_selected(False)
                            #Set selected tile to true to stop the while loop
                            selected_tile = True
                            #Break out of the for loop
                            break
                #Set the hand_select attribute to false you cannot select a tile from the hand.
                game_display.hand_select = False
                game_display.set_hand_scroll(False)
                #Draw the first selected tile
                game_display.draw_move(left_tile=hand_tile)
                # Set the stack_select attribute to true so the player can select a tile from a stack
                game_display.stack_select = True

                #Wait for the player to select a tile from a stack, we iterate through the stacks and the stack_listener will
                #set the selected attribute to true if the player selects a tile
                print("Please enter a tile from your stack: ")
                #By default, the selected tile is false, until a tile is selected. When it is stop the loop
                selected_tile = False
                while not selected_tile:
                    #Iterate through the player's so we can access the stacks
                    for c_player in players:
                        #Iterate through the stacks
                        for tile in c_player.get_stack():
                            #If the tile is selected, set the stack_tile to that tile and break out of the loop
                            if tile.get_selected():
                                stack_tile = tile
                                #Reset the selected attribute to false to make sure it isn't selected next turn.
                                tile.set_selected(False)
                                #Set selected tile to true to stop the while loop
                                selected_tile = True
                                #Break out of the for loop
                                break
                #Set the stack_select attribute to false you cannot select a tile from the stack.
                game_display.set_stack_select(False)
                game_display.set_stack_scroll(False)
                #Set the player_move attribute to true so the player can confirm or cancel their move
                game_display.set_player_move(True)
                confirm_move = game_display.draw_move(players, hand_tile, stack_tile)
                #Set the player_move attribute to false as confirmation on computer players turn is not needed
                game_display.set_player_move(False)
                #Get the stack of the tile t player selected
                #Iterate through the players
                for c_player in players:
                    #Iterate through the stacks
                    for c_tile in c_player.get_stack():
                        #If the tile is the same as the tile the player selected, set the stack to that stack
                        if str(stack_tile) == str(c_tile):
                            #Set the stack to the stack of the tile the player selected
                            stack = players[players.index(c_player)].get_stack()
                            break
                #If the player cancels their move, recursively call the function to get a new move
                if not confirm_move:
                    return self.get_move(players, game_display)
                #If the player confirms their move, return the move
                return [hand_tile, stack, stack_tile]
            #If the player wants to pass, return pass
            elif pass_ and reccommened_move == "pass":
                game_display.set_stack_scroll(False)
                game_display.set_hand_scroll(False)
                return "pass"
            #If the player wants to pass but there is a possible move, display an error message and
            #recursively call the function until a valid move is given from the player
            else:
                print("Error: Can only pass if no moves are available")
                game_display.draw_prompt_time_delay("Can only pass if no moves are available",2)
                return self.get_move(players, game_display)
        else:
            return "pass"

    #*********************************************************************
    #Function Name: get_valid_move
    #Purpose: To get a valid move from the player
    #Parameters:

    #players, a list passed by value. It holds all the players in the game.
    #game_display, an object passed by reference. It refers to the game display.
    #Return Value: If a valid move is made, a list containing hand tile, stack, and stack tile is returned. If the player passes, "pass" is returned.
    #Algorithm:

    #1) Call get_move() to get the move from the player.
    #2) If the player passes, "pass" is returned.
    #3) Otherwise, extract the hand tile, stack, and stack tile from the move.
    #4) Call check_valid_move() to check if the move is valid.
    #5) If the move is valid, the list containing hand tile, stack, and stack tile is returned.
    #6) If the move is not valid, an error message is displayed and get_valid_move() is called recursively.
    #Assistance Received: none
    #*********************************************************************
    def get_valid_move(self, players, game_display):
        #Get the move from the player
        move = self.get_move(players, game_display)
        #If the player passes, return pass
        if move == "pass":
            return "pass"
        #Otherwise, extract the hand tile, stack, and stack tile from the move and check if the move is valid
        else:
            #Extract the hand tile, stack, and stack tile from the move
            hand_tile = move[0]
            stack = move[1]
            stack_tile = move[2]
            #Check if the move is valid, if it is, return the move
            if self.check_valid_move(hand_tile, stack_tile):
                return [hand_tile, stack, stack_tile]
            #If the move is not valid, display an error message and call get_valid_move() recursively until a valid
            #move is made
            else:
                print("Error: Invalid move")
                game_display.draw_prompt_time_delay("Invalid move", 2)
                return self.get_valid_move(players, game_display)
    def score_hand(self):
        return sum(self.hand)

    #*********************************************************************
    #Function Name: score_stacks
    #Purpose: To calculate the total score of a player's stacks
    #Parameters:

    #players: a list of Player objects passed by value. It holds all the players in the game
    #Return Value: The total score of a player's stacks, an integer value
    #Algorithm:

    #1) Initialize score to 0
    #2) For each player in players:
    #a) For each tile in the player's stack:
    #i) If the tile's playerID matches the player's ID:
    #- Add the tile's score to the score variable
    #3) Return the score
    #Assistance Received: None
    #*********************************************************************
    def score_stacks(self, players):
        score = 0
        for c_player in players:
            for stack_tile in c_player.get_stack():
                if stack_tile.player.get_player_id() == self.get_player_id():
                    score += stack_tile
        return score

    def clear_hand(self):
        self.hand.clear()

    #*********************************************************************
    #Function Name: reset_player
    #Purpose: To reset a player's state for a new round of the game
    #Parameters:

    #double_set_length, an integer. It represents the length of the double set in the boneyard
    #Return Value: None
    #Algorithm:

    #1) Reset the boneyard to an empty list
    #2) Generate a new boneyard of length double_set_length and append it to the player's boneyard attribute
    #3) Shuffle the boneyard
    #4) Reset the player's hand to an empty list
    #5) Move 6 tiles from the boneyard to the player's hand
    #6) Reset the player's stack to an empty list
    #7) Move 6 tiles from the player's hand to the stack
    #8) Reset the player's score to 0
    #Assistance Received: none
    #*********************************************************************
    def reset_player(self,double_set_length):
        self.boneyard = []
        self.generate_boneyard(double_set_length)
        self.shuffle_boneyard()
        self.hand = []
        self.move_from_boneyard_to_hand_n(6)
        self.stack = []
        self.move_from_hand_to_stack_n(6)
        self.score = 0

class tile(DisplayTile):
    #The tile class stores the value of the left and right side of a tile aswell as overriding some basic operators
    #to make it easier to work with. It takes in Display Tile which adds attributes and methods to the tile class to
    #make it easier to display it on the game board.
    def __init__(self, left, right, player: Player):
        super().__init__()
        #The left and right attributes store the value of the left and right side of the tile
        self.left = left
        self.right = right
        #The player attribute stores the player object that owns the tile, useful for scoring
        self.player = player
        #If both sides of the tile are the same, the tile is a double
        self.double = self.left == self.right
    def set_selected(self, selected):
        self.selected = selected
    def get_selected(self):
        return self.selected
    def get_double(self):
        return self.double
    def __radd__(self, other):
        return self.left + self.right + other
    def __sub__(self, other):
        return (self.left + self.right) - (other.left + other.right)

    def __add__(self, other):
        return (self.left + self.right) + (other.left + other.right)

    def __lt__(self, other):
        return self.left + self.right < other.left + other.right

    def __gt__(self, other):
        return self.left + self.right > other.left + other.right

    def __eq__(self, other):
        return self.left + self.right == other.left + other.right

    def __le__(self, other):
        return self.left + self.right <= other.left + other.right

    def __ge__(self, other):
        return self.left + self.right >= other.left + other.right

    def __ne__(self, other):
        return self.left + self.right != other.left + other.right

    def __str__(self):
        return "|" + self.player.get_color() + str(self.left) + str(self.right) + "|"

    def display_tile(self):
        print("|" + self.player.get_color() + str(self.left) + str(self.right) + "|", end=" ")

class Computer_Player(Player):
    #*********************************************************************
    #Function Name: get_move
    #Purpose: To get a move recommendation from the computer player and display it on the game board.
    #Parameters:

    #players, an array passed by value. It holds all the player objects in the game.
    #game_display, an object passed by reference. It represents the display for the current game.
    #Return Value: The move recommendation from the computer player.
    #Algorithm:

    #1) Get a move from the recommend move function
    #2) If the move is not "pass", get the hand tile and stack tile from the move.
    #3) Draw the move on the game board using the game_display object.
    #4) Otherwise, display "PASS" on the game board.
    #5) Return the move recommendation.
    #Assistance Received: none
    #*********************************************************************

    #Overriding the get_move function from the Player class to simply use the rec-move to get a move
    def get_move(self, players, game_display):
        #Get a move from the recommend move function
        move = self.reccomend_move(players)
        #If the move is not "pass", get the hand tile and stack tile from the move.
        if move != "pass":
            hand_tile = move[0]
            stack_tile = move[2]
            #Draw the move on the game board using the game_display object.
            game_display.draw_move(players, hand_tile, stack_tile)
            #Display the move reasoning on the game board
            prompt = "The computer picked this move because it has a difference of " + str(hand_tile-stack_tile)\
                     + " Which is the lowest difference after prioritizing opponent tiles"
            game_display.draw_prompt(prompt)
        #If the move is pass, display "PASS" on the game board.
        #Return the move recommendation.
        return move

    def save_player(self):
        string = ""
        string += "Computer:\n"
        string += "   Stacks: "
        for tile_ in self.stack:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Boneyard: "
        for tile_ in self.boneyard:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Hand: "
        for tile_ in self.hand:
            string += str(tile_)[1:4]+" "
        string += "\n"
        string += "   Score: " + str(self.score) + "\n"
        string += "   Rounds Won: " + str(self.rounds_won) + "\n"

        return string


class hand():

    #*********************************************************************
    #Function Name: play_hand
    #Purpose: To play a single hand of the game
    #Parameters:

    #self, a reference to the current object
    #players, a list of player objects, passed by reference. It holds the players in the current game
    #game_display, a GameDisplay object, passed by reference. It holds the GUI object to display the game.
    #Return Value: None
    #Algorithm:

    #1) Initialize consecutive_passes to 0 and all_empty_hands to False
    #2) While consecutive_passes is less than the number of players and not all hands are empty
        #a) For each player in players:
            #i) Display player's turn
            #ii) Display player's hand and stacks of all players
            #iii) Get a valid move from the player
            #iv) If the move is not "pass":
                #1) Get hand_tile and stack_tile from move
                #2) Find the stack corresponding to stack_tile
                #3) Display the tile that was played
                #4) Move the tile from hand to the corresponding stack
                #5) Reset consecutive_passes to 0
            #v) Else:
                #1) Display that the player passed
                #2) Increment consecutive_passes
                #3) Display the final hands, stacks and scores of the players
    #Assistance Received: None
    #*********************************************************************
    def play_hand(self, players, game_display):
        #Initialize consecutive_passes to 0 and all_empty_hands
        consecutive_passes = 0
        #Iterates through the players to see if all hands are empty
        all_empty_hands = all([len(x.hand) == 0 for x in players])
        #Set the color of the screen to gray, which is the main color of the game board
        game_display.gray_screen()
        #While all the players have not passed and all the hands are not empty
        while consecutive_passes < len(players) and not all_empty_hands:
            #Iterate through the players
            for c_player in players:
                print("\nPlayer " + c_player.get_player_id() + "'s turn\n")
                #Display Which Player's turn it is
                game_display.draw_prompt_time_delay("Player " + c_player.get_player_id() + "'s turn", 1)
                self.display_hand(c_player)
                print()
                game_display.draw_all_stacks(players)
                #Display the hand of the player
                game_display.draw_hand(c_player.get_hand())
                #Display the stacks of all the players
                self.display_stacks(players)
                #Get a valid move from the player
                move = c_player.get_valid_move(players, game_display)
                #If the move is not "pass", place the tile
                if move != "pass":
                    hand_tile = move[0]
                    stack_tile = move[2]
                    #Find the stack corresponding to stack_tile
                    for c_player_ in players:
                        for tile_ in c_player_.stack:
                            if str(tile_) == str(stack_tile):
                                stack = c_player_.stack
                    print()
                    print("Player " + c_player.get_player_id() + " played tile ", end="")
                    hand_tile.display_tile()
                    print("to tile ", end="")
                    stack_tile.display_tile()
                    print("in the stacks")
                    #Move the tile from hand to the corresponding stack
                    c_player.move_from_hand_to_stack(hand_tile, stack, stack_tile)
                    #Draw the stacks again to show the move
                    game_display.draw_all_stacks(players)
                    #Draw the hand again to show the move
                    game_display.draw_hand(c_player.get_hand())
                    #Wait for the user to press enter
                    game_display.wait_for_enter()
                    #Reset consecutive_passes to 0
                    consecutive_passes = 0
                else:
                    print()
                    print("Player " + c_player.get_player_id() + " passed")
                    #Display Pass on the screen
                    game_display.draw_prompt_time_delay("PASS")
                    #Increment consecutive_passes
                    consecutive_passes += 1
                    #If consecutive_passes is equal to the number of players, break out of the for loop and the
                    # while loop since all the players have passed
                    if consecutive_passes >= len(players):
                        break
                if len(players) == 2:
                    player1 = type(players[0])
                    player2 =  type(players[1])
                    if (player1 == Player and player2 == Computer_Player) or (player1 == Computer_Player and player2 == Player):
                        if game_display.draw_yes_no_prompt_ws("Save Game to File?"):
                            string = ""
                            for c_player_ in players:
                                string += c_player_.save_player()
                                string += "\n"
                            if players.index(c_player) == len(players)-1:
                                string += "Turn: "+str(players[0])
                            else:
                                string += "Turn: "+str(players[players.index(c_player)+1].get_player_id())
                            filename = game_display.get_filename_save()
                            text_file = open(filename, "w")
                            # write string to file
                            text_file.write(string)
                            # close file
                            text_file.close()
                            game_display.turn_off_display()
                            exit(0)
                if consecutive_passes >= len(players):
                    break
            #Check if all hands are empty
            all_empty_hands = all([len(x.hand) == 0 for x in players])


        print("\n\nHand Over")
        print("Final Hands")
        for c_player in players:
            self.display_hand(c_player)
        print("Final Stacks")
        self.display_stacks(players)
        #Score the hand
        print("Scoring Hands:")
        #Get the scores for the hand
        hand_scores = self.score_hand(players)
        #Get the scores for the stacks
        stack_scores = self.score_stacks(players)
        #Create a dictionary to hold the final scores of the players
        final_scores = {}
        #Iterate through the players and add the scores to the final_scores dictionary
        for c_player in players:
            #The final score is the stack score minus the hand score,
            score = stack_scores[c_player.get_player_id()] - hand_scores[c_player.get_player_id()]
            #set the player id as the key and the score as the value
            final_scores[c_player.get_player_id()] = score
            #Add the score to the player's total score
            c_player.add_score(score)
            print("Player " + c_player.get_player_id() + " scored " + str(score) + " points")
        #Display the final scores to the screen
        game_display.draw_scores(final_scores, "Player ID's", "Scores", "Scores")
        #Discard the tiles remaining in the hands for all the players
        for c_player in players:
            c_player.clear_hand()


    def score_stacks(self, players):
        scores = {}
        for c_player in players:
            scores[c_player.get_player_id()] = c_player.score_stacks(players)
        return scores
    def score_hand(self, players):
        scores = {}
        for c_player in players:
            scores[c_player.get_player_id()] = c_player.score_hand()
        return scores
    def display_stacks(self, players):
        for c_player_stack in players:
            print("Player " + c_player_stack.get_player_id() + "'s stack", end=": ")
            c_player_stack.display_stack()

    def display_hand(self, player):
        print("Player " + player.get_player_id() + "'s hand", end=": ")
        player.display_hand()


class Round():
    #*********************************************************************
    #Function Name: play_round
    #Purpose: To play a full game, and score the round.
    #Parameters:

    #players, a list passed by reference. It holds all the players in the tournament.
    #hand_num, an integer passed by value. It refers to the number of the hand being played.
    #game_display, an object of the GameDisplay class, passed by reference. It is used to display the state of the game on the screen.
    #Return Value: None
    #Algorithm:

    #1) Initialize a new hand.
    #2) If hand_num is 1, deal 5 tiles to each player and play the hand.
        #a) Play the round
        #b) Increment hand_num
    #3) If hand_num is 2, deal 6 tiles to each player and play the hand.
        #a) Play the round
        #b) Increment hand_num
    #4) If hand_num is 3, deal 6 tiles to each player and play the hand.
        #a) Play the round
        #b) Increment hand_num
    #5) If hand_num is 4, deal 4 tiles to each player and play the hand.
        #a) Play the round
        #b) Increment hand_num
    #6) Score the round using the score_round()
    #Assistance Received: none
    #*********************************************************************
    def play_round(self, players, hand_num, game_display, double_set_length=6):
        print("\n\nStarting New Round: ")
        #Initialize a new hand object
        c_hand = hand()
        #Check which hand_num it is and play the hand with the according number of tiles dealt
        #Then increment hand_num so that the next if statement is hit and the next hand is played
        if hand_num == 1:
            print("\nHand: 1")
            if len(players[0].get_hand()) == 1:
                for c_player in players:
                    c_player.move_from_boneyard_to_hand_n(double_set_length-1)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 2:
            print("\nHand: 2")
            if len(players[0].get_hand()) == 0:
                for c_player in players:
                    c_player.move_from_boneyard_to_hand_n(double_set_length)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 3:
            print("\nHand: 3")
            if len(players[0].get_hand()) == 0:
                for c_player in players:
                    c_player.move_from_boneyard_to_hand_n(double_set_length)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 4:
            print("\nHand: 4")
            if len(players[0].get_hand()) == 0:
                for c_player in players:
                    c_player.move_from_boneyard_to_hand_n(len(c_player.get_hand()))
            c_hand.play_hand(players, game_display)
            hand_num += 1
        #Score the round
        self.score_round(players, game_display)

    #*********************************************************************
    #Function Name: score_round
    #Purpose: To calculate and display the final scores and rankings for a round of the game.
    #Parameters:

    #players_, a list of Player objects passed by reference. It holds the players who are playing the game.
    #game_display, a Display object passed by reference. It holds the game display that is used to show the output.
    #Return Value: None
    #Algorithm:

    #1) Print the message "Round Over".
    #2) Make a copy of the players list and sort it based on each player's score in descending order.
    #3) Print the final scores of each player.
    #4) Print the player who won the round.
    #5) Increment the number of rounds won for the winning player and update the players_ list with the change.
    #6) Sort the players list based on the number of rounds won in descending order.
    #7) Print the final rankings of each player.
    #8) Display the current leader and the scores of each player on the game display.
    #Assistance Received: none
    #*********************************************************************
    def score_round(self, players_, game_display):
        print("\n\nRound Over")
        #Make a copy of the players list and sort it based on each player's score in descending order without
        #changing the original list as the order in the orginal list is the order of the players in the game.
        players = players_.copy()
        #Sort the players list based on the points scored in descending order
        players = sorted(players, key=lambda x: x.score, reverse=True)
        print()
        print("Final Scores:")
        for c_player in players:
            print("Player " + c_player.get_player_id() + " scored " + str(c_player.get_score()) + " points")
        print()
        print("Player "+players[0].get_player_id()+" wins the round")
        #Increment the number of rounds won for the winning player and update the players_ list with the change.
        players_[players_.index(players[0])].add_rounds_won()
        #Sort the players list based on the number of rounds won in descending order
        players = sorted(players, key=lambda x: x.rounds_won, reverse=True)
        print()
        print("Final Rankings: ")
        final_scores = {}
        for c_player in players:
            final_scores[c_player.get_player_id()] = c_player.get_rounds_won()
            print("Player " + c_player.get_player_id() + " has " + str(c_player.get_rounds_won()) + " rounds won")
        print()
        print("Player "+players[0].get_player_id()+" is the current leader")
        #Display the current leader and the scores of each player on the game display.
        game_display.draw_scores(final_scores, "Player ID's", "Round Wins", "Final Rankings")


class tournament():
    #*********************************************************************
    #Function Name: init
    #Purpose: Initializes a new instance of the tournament class and starts a new tournament with given number of players and set length.
    #Parameters:

    #player_num, an integer, indicating the number of players in the tournament. Default is 4.
    #double_set_length, an integer, indicating the number of tiles in each double set. Default is 6.
    #Return Value: None
    #Algorithm:

    #1) Create a new board_display object
    #2) Set the double_set_length and player_num attributes of the object
    #3) Start the game display screen
    #4) Call the start_new_tournament method with the given parameters after start has been pressed.
    #Assistance Received: none
    #*********************************************************************
    def __init__(self):
        #Create a new board_display object
        self.game_display = board_display()
        #The player list will hold all the players, the order of the players in the list will be the order of the
        #players in the game.
        self.players = []
        #Wait 1 second for the screen to intialize
        sleep(1)
        #Show the start game_screen
        self.game_display.start_game_screen()
        if self.game_display.ask_load_game():
            root = os.path.join(os.path.dirname(__file__))
            options = self.list_files_with_extension(root+"/Seralize", ".txt")
            filepath = self.game_display.get_filename_load()
            self.player_num = 2
            self.double_set_length = 6
            self.load_seralized_tournament(filepath)
        else:
        #Get the amount of players
            self.player_num = self.game_display.game_config_screen_players()

        #Get the double set length
            self.double_set_length = self.game_display.input_number_screen("What length would you like the double sets?", min_=5)


        #Start the tournament
            self.start_new_tournament(self.player_num, self.double_set_length)

    def list_files_with_extension(self, directory_path, file_extension):
        file_names = []
        for file in os.listdir(directory_path):
            if file.endswith(file_extension):
                file_names.append(file)
        return file_names

    #*********************************************************************
    #Function Name: start_new_tournament
    #Purpose: To start a new tournament, create players and initiate the game rounds.
    #Parameters:

    #player_num: integer, the number of players in the tournament.
    #double_set_length: integer, the number of tiles each player has at the start.
    #Return Value: None
    #Algorithm:

    #1) Create three computer players and one human player.
    #2) Create a new round.
    #3) Determine the order of players.
    #4) Play the round.
    #5) Check if the players want to play another round.
    #6) If the players want to play another round, reset the game and start a new round.
    #7) If not, end the game and declare the winner.
    #Assistance Received: none
    #*********************************************************************

    def extract_player_data(self, file_path):
        players = []
        with open(file_path) as f:
            current_player = None
            for line in f:
                if line.startswith("Computer:"):
                    current_player = "Computer"
                    players.append(
                        {"name": current_player, "stacks": [], "boneyard": [], "hand": [], "score": 0, "rounds_won": 0})
                elif line.startswith("Human:"):
                    current_player = "Human"
                    players.append(
                        {"name": current_player, "stacks": [], "boneyard": [], "hand": [], "score": 0, "rounds_won": 1})
                elif line.startswith("   Stacks:"):
                    stacks = line.split(":")[1].strip().split()
                    players[-1]["stacks"] = stacks
                elif line.startswith("   Boneyard:"):
                    boneyard = line.split(":")[1].strip().split()
                    players[-1]["boneyard"] = boneyard
                elif line.startswith("   Hand:"):
                    hand = line.split(":")[1].strip().split()
                    players[-1]["hand"] = hand
                elif line.startswith("   Score:"):
                    score = int(line.split(":")[1].strip())
                    players[-1]["score"] = score
                elif line.startswith("   Rounds Won:"):
                    rounds_won = int(line.split(":")[1].strip())
                    players[-1]["rounds_won"] = rounds_won
                elif line.startswith("Turn:"):
                    turn = line.split(":")[1].strip()
        return [players, turn]

    def load_seralized_tournament(self, filepath):
        data = self.extract_player_data(filepath)
        human_player = Player()
        computer_player = Computer_Player()
        for player in data[0]:
            if player["name"] == "Computer":
                computer_player_boneyard = []
                for x in player["boneyard"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    computer_player_boneyard.append(tile_)


                computer_player_hand = []
                for x in player["hand"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    computer_player_hand.append(tile_)

                computer_player_stack = []
                for x in player["stacks"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    computer_player_stack.append(tile_)

                computer_player.playerID = 'Computer'
                computer_player.color = 'W'
                computer_player.boneyard = computer_player_boneyard
                computer_player.hand = computer_player_hand
                computer_player.stack = computer_player_stack
                computer_player.score = player["score"]
                computer_player.rounds_won = player["rounds_won"]
            else:
                human_player_boneyard = []
                for x in player["boneyard"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    human_player_boneyard.append(tile_)

                human_player_hand = []
                for x in player["hand"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    human_player_hand.append(tile_)

                human_player_stack = []
                for x in player["stacks"]:
                    if x[0] == 'B':
                        tile_ = tile(int(x[1]), int(x[2]), human_player)
                    else:
                        tile_ = tile(int(x[1]), int(x[2]), computer_player)
                    human_player_stack.append(tile_)

                human_player.playerID = "Human"
                human_player.color = 'B'
                human_player.boneyard = human_player_boneyard
                human_player.hand = human_player_hand
                human_player.stack = human_player_stack
                human_player.score = player["score"]
                human_player.rounds_won = player["rounds_won"]

        c_hand = 4 - (len(human_player_boneyard) // 6 )
        round = Round()
        # Loop until the player does not want to play any more rounds
        if data[1] == "Computer":
            self.players = [computer_player, human_player]
        else:
            self.players = [human_player, computer_player]
            # Determine the order of the players
            if data[1] == "":
                self.determine_order()
        while True:
            # Play the round
            round.play_round(self.players, hand_num=c_hand, game_display=self.game_display,
                             double_set_length=6)
            # Check if the players want to play another round
            # If not, end the game by breaking the loop
            if not self.game_display.draw_yes_no_prompt_ws("Do you want to play another round?"):
                # If not, end the game by breaking the loop
                break
            # If the players want to play another round, reset the game and start a new round
            else:
                for c_player in self.players:
                    c_player.reset_player(6)
                c_hand = 1
                self.determine_order()
        # End the game and declare the winner
        self.get_winner()
        self.game_display.wait_for_enter()
        self.game_display.turn_off_display()
        exit()
        print("\nGoodbye! Thanks for playing!")


    def start_new_tournament(self, player_num, double_set_length):
        #Create the correct amount of computer and human players
        #The loop alternates between creating a computer player and a human player so an even number of
        # human and computer players are always created. The first player is always a human player.
        #Loop for the specified number of players
        for x in range(0, player_num):
            #Create a list of existing player colors
            ex_player_colors = [x.get_color() for x in self.players]
            #Create a list of existing player ids
            ex_player_ids = [x.get_player_id() for x in self.players]
            #If the last player created was a human player, create a computer player
            if self.game_display.ask_player_type() == "Computer":
                #Create a new computer player
                temp_player = Computer_Player()
                #Create a new player
                temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
                print("Computer Player " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
            #If the last player created was a computer player, create a human player
            else:
                #Create a new human player object
                temp_player = Player()
                #Load in necessary data
                temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
                print("Human Player " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
            #Add the player to the list of players
            self.players.append(temp_player)
            self.game_display.screen.fill((0,0,0))
            pygame.display.flip()
            sleep(.5)
            #Set the last player created to the current player so it alternates next iteration
        #Create a new round object
        round = Round()
        #Loop until the player does not want to play any more rounds
        while True:
            #Determine the order of the players
            self.determine_order()
            #Play the round
            round.play_round(self.players, hand_num=1, game_display=self.game_display, double_set_length=double_set_length)
            #Check if the players want to play another round
            #If not, end the game by breaking the loop
            if not self.game_display.draw_yes_no_prompt_ws("Do you want to play another round?"):
                #If not, end the game by breaking the loop
                break
            #If the players want to play another round, reset the game and start a new round
            else:
                for c_player in self.players:
                    c_player.reset_player(double_set_length)
        #End the game and declare the winner
        self.get_winner()
        self.game_display.wait_for_enter()
        self.game_display.turn_off_display()
        exit()
        print("\nGoodbye! Thanks for playing!")

    #*********************************************************************
    #Function Name: get_winner
    #Purpose: To determine the winner of the tournament based on the number of rounds won
    #Parameters: None
    #Return Value: None
    #Algorithm:

    #1) Make a copy of the list of players
    #2) Sort the list in descending order based on the number of rounds won by each player
    #3) Print the final rankings for all players
    #4) If the first two players have won the same number of rounds, print "Its a Draw!"
    #Otherwise, print the winner
    #Assistance Received: none
    #*********************************************************************
    def get_winner(self):
        #Make a copy of the list of players so the original list is not modified
        players = self.players.copy()
        #Sort the list in descending order based on the number of rounds won by each player
        players = sorted(players, key=lambda x: x.rounds_won, reverse=True)
        print()
        print("Final Rankings: ")
        for c_player in players:
            print("Player " + c_player.get_player_id() + " has " + str(c_player.get_rounds_won()) + " rounds won")
        print()
        if players[0].get_rounds_won() == players[1].get_rounds_won():
            self.game_display.draw_winner("Draw!")
            print("\nIts a Draw!")
        else:
            self.game_display.draw_winner(players[0].get_player_id())
            print("\nPlayer "+players[0].get_player_id()+" is the winner!")

    #*********************************************************************
    #Function Name: determine_order
    #Purpose: To determine the order of play for a new round of the game.
    #Parameters: None
    #Return Value: None
    #Algorithm:

    #1) Shuffle the boneyard for each player and have them move a tile from the boneyard to their hand.
    #2) Display the players' hands.
    #3) Sort the players by the value of the tile in their hand in descending order.
    #4) If there are any ties, reshuffle the boneyard and have players draw new tiles until there are no ties.
    #5) Print the order of play based on the sorted order.
    #Assistance Received: None
    #*********************************************************************
    def determine_order(self):
        #Keep re-shuffling until no equal tiles are found
        #Set equal to true so the loop runs at least once
        equal = True
        while equal:
            #Set equal to false so the loop will only run again if there are ties
            equal = False
            print("\nDetermining Order:")
            #Iterate through each player and add a tile to their hand
            for c_player in self.players:
                print("Player " + c_player.get_player_id() + " boneyard")
                c_player.display_boneyard()
                print("Shuffling Boneyard...")
                c_player.shuffle_boneyard()
                print("Player " + c_player.get_player_id() + " shuffled boneyard")
                c_player.display_boneyard()
                #Move a tile from the boneyard to the player's hand
                c_player.move_from_boneyard_to_hand_n(1)
            print("\nPlayers hands:")
            for c_player in self.players:
                print("Player " + c_player.get_player_id() + " has tile ", end="")
                c_player.display_hand()
            #We sort the players by the value of the tile in their hand in descending order, that will be the order
            #of the game
            print("\nComparing Tiles...")
            # Sort the players by the value of the tile in their hand in descending order
            self.players.sort(key=lambda x: x.hand[0], reverse=True)
            #Check if there are any ties by iterating through the players twice, and comparing the first tile in each
            #player's hand against each other
            #Iterate through each player once as the player we are comparing against
            for comp_player in self.players:
                #Iterate through each player again to the comp_players hand against all the other players' hands
                for c_player in self.players:
                    #If the two players have the same tile, re-shuffle the boneyard and have them draw new tiles
                    #Set equal to true so the loop runs again
                    if comp_player.get_hand()[0] == c_player.get_hand()[0] and comp_player != c_player:
                        print(
                            "\n\nPlayer " + comp_player.get_player_id() + " and Player " + c_player.get_player_id() + " have equal tiles re-shuffling")
                        equal = True
                        #Move the tiles back to the boneyard
                        for c_player in self.players:
                            c_player.move_from_hand_to_boneyard_n(1)
                        #Break out of the inner loop
                        break
                #If equal is true, break out of the outer loop
                if equal == True:
                    break
        print("\nOrder is:")
        for c_player in self.players:
            print("Player " + c_player.get_player_id() + " with tile ", end="")
            c_player.display_hand()
        #The list of players will now be in the order they will play in, which we will be reflected within the the
        #play_hand when we iterate through the list of players to play their turn