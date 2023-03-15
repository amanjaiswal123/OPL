import os
from random import randint, shuffle
from gui import DisplayTile, display_player_attributes, game_display
from time import sleep
from threading import Thread
class Player(display_player_attributes):
    def __init__(self):
        #The playerID is used to identify the player. Primarily used to identify the turn of the player as well as
        #the tile owner within the stacks
        super().__init__()
        self.playerID = None
        self.color = None
        self.boneyard = []
        self.hand = []
        self.stack = []
        self.score = 0
        self.rounds_won = 0
        self.hand_offset = 0

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
        # user_input = input("Please enter a player name?")
        # CHANGE BEFORE DEMO
        user_input = str(len(ex_player_ids) + 1)
        if user_input in ex_player_ids:
            print("Sorry that id has already been taken please choose another")
            self.assign_player_color(ex_player_ids)
        else:
            self.playerID = user_input

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

    def create_new_player(self, ex_player_ids, ex_player_colors, double_set_length):
        self.assign_player_id(ex_player_ids)
        self.assign_player_color(ex_player_colors)
        self.generate_boneyard(double_set_length)
        self.hand = []
        self.shuffle_boneyard()
        self.move_from_boneyard_to_hand_n(6)
        self.stack = []
        self.move_from_hand_to_stack_n(6)
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


    def check_valid_move(self, hand_tile, stack_tile):
        valid_move = False
        if stack_tile.double:
            if hand_tile.double:
                if hand_tile > stack_tile:
                    valid_move = True
            else:
                if hand_tile >= stack_tile:
                    valid_move = True
        else:
            if hand_tile.double:
                # If the hand tuple is a double, we can use it
                valid_move = True
            else:
                # If the hand tuple is not a double and the stack tuple is not a double, we can use it
                if hand_tile >= stack_tile:
                    valid_move = True
        return valid_move

    def reccomend_move(self, players):
        valid_moves = []
        for hand_tile in self.hand:
            for c_player in players:
                for stack_tile in c_player.stack:
                    if self.check_valid_move(hand_tile, stack_tile):
                        difference = hand_tile - stack_tile
                        valid_moves.append([hand_tile, c_player.stack, stack_tile, difference])
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
    def get_hand_tile(self):
        user_input = input("Please enter a tile from your hand: ")
        for x in self.hand:
            if str(x) == ("|" + user_input + "|"):
                return x
        print("Error: Tile not found in Hand")
        print("Player " + self.playerID + "'s hand", end=": ")
        self.display_hand()
        return self.get_hand_tile()

    def get_stack_tile(self, players):
        user_input = input("Please enter a tile from the stacks to play on: ")
        for c_player in players:
            for x in c_player.stack:
                if str(x) == "|" + user_input + "|":
                    return [c_player.stack, x]
        print("Error: Tile not found in stacks")
        for c_player in players:
            print("Player " + c_player.get_player_id() + "'s stack", end=": ")
            c_player.display_stack()
        return self.get_stack_tile(players)

    def ask_to_pass(self):
        user_input = input("Would you like to pass? (Y/N)")
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Error: Please enter Y or N")
            self.ask_to_pass()

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

    def ask_reccomended_move(self, reccommened_move):
        user_input = input("Would you like to play the reccomended move? (Y/N)")
        if user_input == "Y":
            self.display_rec_move(reccommened_move)
        elif user_input != "N":
            print("Error: Please enter Y or N")
            self.ask_reccomended_move(reccommened_move)

    def get_move(self, players, tournament_):
        stack_scroll_thread = Thread(target=tournament_.stack_scroll, args=[])
        stack_scroll_thread.start()
        hand_scroll_thread = Thread(target=self.hand_listener, args=[tournament_.event_queue, tournament_.screen])
        hand_scroll_thread.start()
        reccommened_move = self.reccomend_move(players)
        rec_move = tournament_.draw_yes_no_prompt("Would you like a recommended move?")
        if rec_move:
            rec_hand_tile = reccommened_move[0]
            rec_stack_tile = reccommened_move[2]
            tournament_.draw_move(rec_hand_tile,rec_stack_tile)
            sleep(3)
        pass_ = tournament_.draw_yes_no_prompt("Would you like to pass?")
        if not pass_:
            self.hand_select = True
            #hand_tile = self.get_hand_tile()
            print("Please enter a tile from your hand: ")
            selected_tile = False
            while not selected_tile:
                for tile in self.hand:
                    if tile.selected:
                        hand_tile = tile
                        tile.selected = False
                        selected_tile = True
                        break
            self.hand_select = False
            tournament_.draw_move(hand_tile)
            tournament_.stack_select = True
            sleep(1)
            print("Please enter a tile from your stack: ")
            selected_tile = False
            while not selected_tile:
                for c_player in tournament_.players:
                    for tile in c_player.stack:
                        if tile.selected:
                            stack_tile = tile
                            tile.selected = False
                            selected_tile = True
                            break
            #stack_stack_tile = self.get_stack_tile(players)
            tournament_.stack_select = False
            tournament_.draw_move(hand_tile,stack_tile)
            sleep(5)
            for c_player in players:
                for tile in c_player.stack:
                    if stack_tile == tile:
                        stack = players[players.index(c_player)].stack
                        break
            return [hand_tile, stack, stack_tile]
        elif pass_ and reccommened_move == "pass":
            return "pass"
        else:
            print("Error: Can only pass if no moves are available")
            return self.get_move(players, tournament_)

    def get_valid_move(self, players, tournament_):
        move = self.get_move(players, tournament_)
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
                tournament_.draw_prompt("Invalid move")
                return self.get_valid_move(players, tournament_)
    def score_hand(self):
        return sum(self.hand)

    def score_stacks(self, players):
        score = 0
        for c_player in players:
            for stack_tile in c_player.stack:
                if stack_tile.player.get_player_id() == self.get_player_id():
                    score += stack_tile
        return score

    def clear_hand(self):
        self.hand = []


    def reset_player(self,double_set_length):
        self.boneyard = []
        self.generate_boneyard(double_set_length)
        self.shuffle_boneyard()
        self.hand = []
        self.move_from_boneyard_to_hand_n(6)
        self.stack = []
        self.move_from_hand_to_stack_n(6)
        self.score = 0

    def seralize(self):
        string = ""
        string += "Player "+str(self.playerID)+": "+"Human"+"\n"
        string += "   Stacks: "
        t_string = ""
        for tile in self.stack:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Boneyard: "
        t_string = ""
        for tile in self.boneyard:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Hand: "
        t_string = ""
        for tile in self.hand:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Score: "+str(self.score) + "\n"
        string += "   Rounds Won: "+str(self.rounds_won) + "\n"
        return string

class Computer_Player(Player):

    def get_move(self, players, tournament_):
        move = self.reccomend_move(players)
        hand_tile = move[0]
        stack_tile = move[2]
        tournament_.draw_move(hand_tile, stack_tile)
        sleep(5)
        return move

    def seralize(self):
        string = ""
        string += "Player "+str(self.playerID) + ": " + "Computer" + "\n"
        string += "   Stacks: "
        t_string = ""
        for tile in self.stack:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Boneyard: "
        t_string = ""
        for tile in self.boneyard:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Hand: "
        t_string = ""
        for tile in self.hand:
            t_string += str(tile.player.get_color()) + str(tile.left) + str(tile.right) + " "
        string += t_string + "\n"
        string += "   Score: " + str(self.score) + "\n"
        string += "   Rounds Won: " + str(self.rounds_won) + "\n"
        return string
class tile(DisplayTile):

    def __init__(self, left, right, player: Player):
        super().__init__()
        self.left = left
        self.right = right
        self.player = player
        self.double = self.left == self.right

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

    def ask_to_save_game(self):
        user_input = input("Would you like to save the game? (Y/N)")
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Error: Please enter Y or N")
            self.ask_to_save_game()

    def play_hand(self, players, tournament_):
        consecutive_passes = 0
        all_empty_hands = all([len(x.hand) == 0 for x in players])
        while consecutive_passes != len(players) and not all_empty_hands:
            for c_player in players:
                print("\nPlayer " + c_player.get_player_id() + "'s turn\n")
                self.display_hand(c_player)
                print()
                tournament_.draw_all_stacks()
                c_player.draw_hand(tournament_.screen)
                self.display_stacks(players)
                move = c_player.get_valid_move(players, tournament_)
                if move != "pass":
                    hand_tile = move[0]
                    stack_tile = move[2]
                    for c_player_ in players:
                        for tile_ in c_player_.stack:
                            if str(tile_) ==  str(stack_tile):
                                stack = c_player_.stack
                    print()
                    print("Player " + c_player.get_player_id() + " played tile ", end="")
                    hand_tile.display_tile()
                    print("to tile ", end="")
                    stack_tile.display_tile()
                    print("in the stacks")
                    c_player.move_from_hand_to_stack(hand_tile, stack, stack_tile)
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
        for c_player in players:
            score = stack_scores[c_player.get_player_id()]-hand_scores[c_player.get_player_id()]
            c_player.score += score
            print("Player " + c_player.get_player_id() + " scored " + str(score) + " points")
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

    def play_serialized_hand(self, players, hand_num=1):
        pass






class Round():
    def play_round(self, players, hand_num, tournament_):
        # CLI
        print("\n\nStarting New Round: ")
        c_hand = hand()
        if hand_num == 1:
            print("\nHand: 1")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(5)
            c_hand.play_hand(players, tournament_)
            hand_num += 1
        if hand_num == 2:
            print("\nHand: 2")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(6)
            c_hand.play_hand(players, tournament_)
            hand_num += 1
        if hand_num == 3:
            print("\nHand: 3")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(6)
            c_hand.play_hand(players, tournament_)
            hand_num += 1
        if hand_num == 4:
            print("\nHand: 4")
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(4)
            c_hand.play_hand(players, tournament_)
            hand_num += 1
        self.score_round(players)


    def score_round(self, players_):
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
        for c_player in players:
            print("Player " + c_player.get_player_id() + " has " + str(c_player.get_rounds_won()) + " rounds won")
        print()
        print("Player "+players[0].get_player_id()+" is the current leader")



    def get_winner(self, players):
        return players[0]


class tournament(game_display):
    def __init__(self, player_num=4, double_set_length=6):
        super().__init__()
        self.double_set_length = double_set_length
        self.player_num = player_num
        self.players = []
        sleep(1)
        self.start_game_screen()



    def save_game(self,next:Player):
        string = ""
        for c_player in self.players:
            string += c_player.seralize()
        string += "\nTurn: "+str(next.get_player_id())
        filename = self.get_filename()
        with open(filename, "w") as f:
            f.write(string)
        exit()
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

    def start_new_tournament(self, player_num, double_set_length):
        for x in range(0, 3):
            temp_player = Computer_Player()
            ex_player_colors = [x.get_color() for x in self.players]
            ex_player_ids = [x.get_player_id() for x in self.players]
            temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
            print("Player " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
            self.players.append(temp_player)
        ex_player_colors = [x.get_color() for x in self.players]
        ex_player_ids = [x.get_player_id() for x in self.players]
        temp_player = Player()
        temp_player.create_new_player(ex_player_ids, ex_player_colors, double_set_length)
        print("Player Human " + temp_player.get_player_id() + " has been created with color " + temp_player.get_color())
        self.players.append(temp_player)

        round = Round()
        while True:
            self.determine_order()
            round.play_round(self.players, hand_num=1, tournament_=self)
            if not self.play_again():
                break
            else:
                for c_player in self.players:
                    c_player.reset_player(double_set_length)
        self.get_winner()
        print("\nGoodbye! Thanks for playing!")


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

    def play_again(self):
        play_again = input("Play again? (y/n): ")
        if play_again == "y":
            return True
        elif play_again == "n":
            return False
        else:
            print("Error: Please enter y or n")
            return self.play_again()

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
                    if comp_player.hand[0] == c_player.hand[0] and comp_player != c_player:
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

    def ask_to_seralize(self):
        return False
