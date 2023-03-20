import os
from random import randint, shuffle
from gui import DisplayTile, board_display
from time import sleep
from threading import Thread
import copy
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
    #*********************************************************************
    #Function Name: assign_player_id
    #Purpose: To assign a unique ID to a player for a game
    #Parameters:

    #self, a reference to the current instance of the class
    #ex_player_ids, a list passed by value. It holds IDs of existing players
    #Return Value: None
    #Algorithm:

    #1) Prompt the user to enter a player name (This line is commented out and should be changed before demo)
    #2) Set the user input to a string representing the length of the ex_player_ids list plus 1
    #3) If the user input is in ex_player_ids, print an error message and call assign_player_color recursively
    #4) Otherwise, set the playerID attribute of self to the user input
    #Assistance Received: none
    #*********************************************************************
    def assign_player_id(self, ex_player_ids):
        # user_input = input("Please enter a player name?")
        # CHANGE BEFORE DEMO
        user_input = str(len(ex_player_ids) + 1)
        if user_input in ex_player_ids:
            print("Sorry that id has already been taken please choose another")
            self.assign_player_color(ex_player_ids)
        else:
            self.playerID = user_input
#*********************************************************************
#Function Name: assign_player_color
#Purpose: To assign a unique color to a player for a game
#Parameters:

#self, a reference to the current instance of the class
#ex_player_colors, a list passed by value. It holds colors of existing players
#Return Value: None
#Algorithm:

#1) Create a list of valid colors ["B", "W", "R", "G", "b", "w", "r", "g"]
#2) Set the user input to a random color from the valid_colors list (This line is commented out and should be changed before demo)
#3) If the user input is not in valid_colors, print an error message and call assign_player_color recursively
#4) If the user input (uppercased) is in ex_player_colors, print an error message and call assign_player_color recursively
#5) Otherwise, set the color attribute of self to the user input (uppercased)
#Assistance Received: none
#*********************************************************************
    def assign_player_color(self, ex_player_colors):
        #     user_input = input("Please enter a player color(B/W/R/G)?")
        valid_colors = ["B", "W", "R", "G", "b", "w", "r", "g"]
        # CHANGE BEFORE DEMO
        user_input = valid_colors[randint(0, 3)]
        if user_input not in valid_colors:
            print("Please enter a either B, W, R, or G")
            self.assign_player_color()
        elif user_input.upper() in ex_player_colors:
            print("Sorry that color has already been taken please choose another")
            self.assign_player_color(ex_player_colors)
        else:
            self.color = user_input.upper()
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
        self.assign_player_id(ex_player_ids)
        self.assign_player_color(ex_player_colors)
        self.generate_boneyard(double_set_length)
        self.hand = []
        self.shuffle_boneyard()
        self.move_from_boneyard_to_hand_n(double_set_length)
        self.stack = []
        self.move_from_hand_to_stack_n(double_set_length)
        self.score = 0
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
        print("\nHAND TILE:" + str(hand_tile))
        print("\nSTACK TILE"+ str(stack_tile))
        print("\nSTACK:")
        for x in stack:
            print(x)
        tile_index = self.hand.index(hand_tile)
        stack[stack.index(stack_tile)] = self.hand.pop(tile_index)
        print("\nMOD STACK:")
        for x in stack:
            print(x)
        x = 1

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
        valid_move = False
        if stack_tile.get_double():
            if hand_tile.get_double():
                if hand_tile > stack_tile:
                    valid_move = True
            else:
                if hand_tile >= stack_tile:
                    valid_move = True
        else:
            if hand_tile.get_double():
                # If the hand tuple is a double, we can use it
                valid_move = True
            else:
                # If the hand tuple is not a double and the stack tuple is not a double, we can use it
                if hand_tile >= stack_tile:
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

    #1) For each tile in self.hand, iterate over each player and their stack and check if the move is valid
    #2) If the move is valid, calculate the difference between hand_tile and stack_tile and append the move to a list of valid moves
    #3) Sort the list of valid moves by difference in ascending order
    #4) Check the player ID of the stack_tile. If it is not the current player, recommend the move with the lowest difference
    #5) If all the moves are invalid, return "pass"
    #Assistance Received: none
    #*********************************************************************
    def reccomend_move(self, players):
        valid_moves = []
        for hand_tile in self.hand:
            for c_player in players:
                for stack_tile in c_player.stack:
                    if self.check_valid_move(hand_tile, stack_tile):
                        difference = hand_tile - stack_tile
                        valid_moves.append([hand_tile, c_player.get_stack(), stack_tile, difference])
        if len(valid_moves) == 0:
            return "pass"
        valid_moves.sort(key=lambda x: x[3])
        best_move = valid_moves[0]
        for move in valid_moves:
            stack_tile = move[2]
            stack_tile_player_id = stack_tile.player.get_player_id()
            if stack_tile_player_id != self.playerID:
                best_move = move
                break

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
    #2) Use the reccomend_move function to generate a recommended move.
    #3) Ask the player if they want to use the recommended move.
    #4) Ask the player if they want to pass.
    #5) If the player does not want to pass, wait for them to select a tile from their hand and then a tile from a stack.
    #6) Return the selected tiles.
    #Assistance Received: none
    #*********************************************************************
    def get_move(self, players, game_display):
        stack_scroll_thread = Thread(target=game_display.stack_scroll, args=[players])
        stack_scroll_thread.start()
        hand_scroll_thread = Thread(target=game_display.hand_listener, args=[self.hand])
        hand_scroll_thread.start()
        reccommened_move = self.reccomend_move(players)
        game_display.stack_offset = 0
        rec_move = game_display.draw_yes_no_prompt("Would you like a recommended move?")
        if rec_move:
            if reccommened_move != "pass":
                rec_hand_tile = reccommened_move[0]
                rec_stack_tile = reccommened_move[2]
                game_display.draw_move(players, rec_hand_tile,rec_stack_tile)
                prompt = "The computer recommends this move because it has a difference of " + str(
                    rec_hand_tile - rec_stack_tile) \
                         + " Which is the lowest difference after prioritizing opponent tiles"
                game_display.draw_prompt(prompt)
            else:
                game_display.draw_prompt_time_delay("PASS")
        pass_ = game_display.draw_yes_no_prompt("Would you like to pass?")
        if not pass_:
            game_display.hand_select = True
            #hand_tile = self.get_hand_tile()
            print("Please enter a tile from your hand: ")
            selected_tile = False
            while not selected_tile:
                for tile in self.hand:
                    if tile.get_selected():
                        hand_tile = tile
                        tile.set_selected(False)
                        selected_tile = True
                        break
            game_display.hand_select = False
            game_display.draw_move(left_tile=hand_tile)
            game_display.stack_select = True
            sleep(1)
            print("Please enter a tile from your stack: ")
            selected_tile = False
            while not selected_tile:
                for c_player in players:
                    for tile in c_player.get_stack:
                        if tile.get_selected():
                            stack_tile = tile
                            tile.set_selected(False)
                            selected_tile = True
                            break
            #stack_stack_tile = self.get_stack_tile(players)
            game_display.stack_select = False
            game_display.player_move = True
            confirm_move = game_display.draw_move(players, hand_tile, stack_tile)
            game_display.player_move = False
            for c_player in players:
                for tile in c_player.get_stack():
                    if stack_tile == tile:
                        stack = players[players.index(c_player)].stack
                        break
            if not confirm_move:
                return self.get_move(players, game_display)
            return [hand_tile, stack, stack_tile]
        elif pass_ and reccommened_move == "pass":
            return "pass"
        else:
            print("Error: Can only pass if no moves are available")
            game_display.draw_prompt_time_delay("Can only pass if no moves are available",2)
            return self.get_move(players, game_display)

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
        move = self.get_move(players, game_display)
        if move == "pass":
            return "pass"
        else:
            hand_tile = move[0]
            stack = move[1]
            stack_tile = move[2]
            if self.check_valid_move(hand_tile, stack_tile):
                return [hand_tile, stack, stack_tile]
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
        self.hand = []

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
    def get_move(self, players, game_display):
        move = self.reccomend_move(players)
        if move != "pass":
            hand_tile = move[0]
            stack_tile = move[2]
            game_display.draw_move(players, hand_tile, stack_tile)
            prompt = "The computer picked this move because it has a difference of " + str(hand_tile-stack_tile)\
                     + " Which is the lowest difference after prioritizing opponent tiles"
            game_display.draw_prompt(prompt)
        else:
            game_display.draw_prompt_time_delay("PASS")
        return move

class tile(DisplayTile):

    def __init__(self, left, right, player: Player):
        super().__init__()
        self.left = left
        self.right = right
        self.player = player
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
        consecutive_passes = 0
        all_empty_hands = all([len(x.hand) == 0 for x in players])
        game_display.gray_screen()
        while consecutive_passes < len(players) and not all_empty_hands:
            for c_player in players:
                print("\nPlayer " + c_player.get_player_id() + "'s turn\n")
                game_display.draw_prompt_time_delay("Player " + c_player.get_player_id() + "'s turn", 1)
                self.display_hand(c_player)
                print()
                game_display.draw_all_stacks(players)
                game_display.draw_hand(c_player.get_hand())
                self.display_stacks(players)
                move = c_player.get_valid_move(players, game_display)
                if move != "pass":
                    hand_tile = move[0]
                    stack_tile = move[2]
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
                    c_player.move_from_hand_to_stack(hand_tile, stack, stack_tile)
                    game_display.draw_all_stacks(players)
                    game_display.draw_hand(c_player.get_hand())
                    game_display.wait_for_enter()
                    consecutive_passes = 0
                else:
                    print()
                    print("Player " + c_player.get_player_id() + " passed")
                    consecutive_passes += 1
              #  if self.ask_to_save_game():
              #      c_player_pos = players.index(c_player)
               #     if c_player_pos != (len(players) - 1):
               #         next_player = players[c_player_pos + 1]
               #     else:
               #         next_player = players[0]
                #    tournament_.save_game(next_player)
            all_empty_hands = all([len(x.hand) == 0 for x in players])
        print("\n\nHand Over")
        print("Final Hands")
        for c_player in players:
            self.display_hand(c_player)
        print("Final Stacks")
        self.display_stacks(players)
        print("Scoring Hands:")
        hand_scores = self.score_hand(players)
        stack_scores = self.score_stacks(players)
        final_scores = {}
        for c_player in players:
            score = stack_scores[c_player.get_player_id()] - hand_scores[c_player.get_player_id()]
            final_scores[c_player.get_player_id()] = score
            c_player.add_score(score)
            print("Player " + c_player.get_player_id() + " scored " + str(score) + " points")
        game_display.draw_scores(final_scores, "Player ID's", "Scores", "Scores")
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
        c_hand = hand()
        if hand_num == 1:
            print("\nHand: 1")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(double_set_length-1)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 2:
            print("\nHand: 2")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(double_set_length)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 3:
            print("\nHand: 3")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(double_set_length)
            c_hand.play_hand(players, game_display)
            hand_num += 1
        if hand_num == 4:
            print("\nHand: 4")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(len(c_player.get_hand()))
            c_hand.play_hand(players, game_display)
            hand_num += 1
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
        players = players_.copy()
        players = sorted(players, key=lambda x: x.score, reverse=True)
        print()
        print("Final Scores:")
        for c_player in players:
            print("Player " + c_player.get_player_id() + " scored " + str(c_player.get_score()) + " points")
        print()
        print("Player "+players[0].get_player_id()+" wins the round")
        players_[players_.index(players[0])].rounds_won += 1
        players = sorted(players, key=lambda x: x.rounds_won, reverse=True)
        print()
        print("Final Rankings: ")
        final_scores = {}
        for c_player in players:
            final_scores[c_player.get_player_id()] = c_player.get_rounds_won()
            print("Player " + c_player.get_player_id() + " has " + str(c_player.get_rounds_won()) + " rounds won")
        print()
        print("Player "+players[0].get_player_id()+" is the current leader")
        game_display.draw_scores(final_scores, "Player ID's", "Scores", "Scores")



    def get_winner(self, players):
        return players[0]


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
    def __init__(self, player_num=4, double_set_length=6):
        self.game_display = board_display()
        self.players = []
        sleep(1)
        self.game_display.start_game_screen()
        self.player_num = self.game_display.game_config_screen_players()
        self.double_set_length = self.game_display.input_number_screen()
        self.start_new_tournament(self.player_num, self.double_set_length)

    def load_game(self):
        pass

    def is_path_available(self, path):
        if not os.path.exists(path):
            return True
        else:
            return False

    def get_filename(self):
        filename = input("Please enter a filename: ")+".txt"
        if not self.is_path_available(filename):
            print("Filename already exists")
            return self.get_filename()
        return filename
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
    def start_new_tournament(self, player_num, double_set_length):
        last = Player()
        for x in range(0, player_num):
            ex_player_colors = [x.get_color() for x in self.players]
            ex_player_ids = [x.get_player_id() for x in self.players]
            if type(last) == Player:
                temp_player = Computer_Player()
                temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
                print("Player " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
            else:
                temp_player = Player()
                temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
                print("Player Human " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
            self.players.append(temp_player)
            last = temp_player
        round = Round()
        while True:
            self.determine_order()
            round.play_round(self.players, hand_num=1, game_display=self.game_display, double_set_length=double_set_length)
            if not board_display.draw_play_another_round():
                break
            else:
                for c_player in self.players:
                    c_player.reset_player(double_set_length)
        self.get_winner()
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
        players = self.players.copy()
        players = sorted(players, key=lambda x: x.rounds_won, reverse=True)
        print()
        print("Final Rankings: ")
        for c_player in players:
            print("Player " + c_player.get_player_id() + " has " + str(c_player.get_rounds_won()) + " rounds won")
        print()
        if players[0].get_rounds_won() == players[1].get_rounds_won():
            print("\nIts a Draw!")
        else:
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
        equal = True
        while equal:
            equal = False
            # CLI
            print("\nDetermining Order:")
            for c_player in self.players:
                print("Player " + c_player.get_player_id() + " boneyard")
                c_player.display_boneyard()
                print("Shuffling Boneyard...")
                c_player.shuffle_boneyard()
                print("Player " + c_player.get_player_id() + " shuffled boneyard")
                c_player.display_boneyard()
                c_player.move_from_boneyard_to_hand_n(1)
            print("\nPlayers hands:")
            for c_player in self.players:
                print("Player " + c_player.get_player_id() + " has tile ", end="")
                c_player.display_hand()
            print("\nComparing Tiles...")
            self.players.sort(key=lambda x: x.hand[0], reverse=True)
            for comp_player in self.players:
                for c_player in self.players:
                    if comp_player.get_hand()[0] == c_player.get_hand()[0] and comp_player != c_player:
                        print(
                            "\n\nPlayer " + comp_player.get_player_id() + " and Player " + c_player.get_player_id() + " have equal tiles re-shuffling")
                        equal = True
                        for c_player in self.players:
                            c_player.move_from_hand_to_boneyard_n(1)
                        break
                if equal == True:
                    break
        print("\nOrder is:")
        for c_player in self.players:
            print("Player " + c_player.get_player_id() + " with tile ", end="")
            c_player.display_hand()
