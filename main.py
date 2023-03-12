import random
from random import randint, shuffle
import collections
class player:
    def __init__(self):
        self.playerID = None
        self.color = None
        self.boneyard = []
        self.hand = []
        self.stack = []
        self.score = 0
        self.roundsWon = 0

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
    def get_roundsWon(self):
        return self.roundsWon
    def generate_boneyard(self, n):
        for x in range(0, n+1):
            for y in range(0, n+1):
                c_tile = tile(x, n-y, self)
                self.boneyard.append(c_tile)

    def move_from_boneyard_to_hand_n(self, n):
        for x in range(0, n):
            self.hand.append(self.boneyard.pop(0))

    def move_from_hand_to_stack_n(self, n):
        for x in range(0, n):
            self.stack.append(self.hand.pop(0))

    def assign_player_id(self, ex_player_ids):
        #user_input = input("Please enter a player name?")
        #CHANGE BEFORE DEMO
        user_input = str(len(ex_player_ids)+1)
        if user_input in ex_player_ids:
            print("Sorry that id has already been taken please choose another")
            self.assign_player_color(ex_player_ids)
        else:
            self.playerID = user_input

    def assign_player_color(self, ex_player_colors):
   #     user_input = input("Please enter a player color(B/W/R/G)?")
        valid_colors = ["B", "W", "R", "G", "b", "w", "r", "g"]
        #CHANGE BEFORE DEMO
        user_input = valid_colors[randint(0, 3)]
        if user_input not in valid_colors:
            print("Please enter a either B, W, R, or G")
            self.assign_player_color()
        elif user_input.upper() in ex_player_colors:
            print("Sorry that color has already been taken please choose another")
            self.assign_player_color(ex_player_colors)
        else:
            self.color = user_input.upper()
    def create_new_player(self, ex_player_ids,ex_player_colors,double_set_length):
        self.assign_player_id(ex_player_ids)
        self.assign_player_color(ex_player_colors)
        self.generate_boneyard(double_set_length)
        self.hand = []
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
        stack[stack.index(stack_tile)] = self.hand.pop(self.hand.index(hand_tile))

    def check_valid_move(self, hand_tile, stack, stack_tile):
        valid_move = False
        if stack_tile.double:
            if hand_tile.double:
                if hand_tile > stack_tile:
                    valid_move = True
            else:
                if hand_tile >= stack_tile:
                    valid_move = True
        else:
            if hand.double:
                # If the hand tuple is a double, we can use it
                valid_move = True
            else:
                # If the hand tuple is not a double and the stack tuple is not a double, we can use it
                if hand_tile >= stack_tile:
                    valid_move = True
        return valid_move

    def get_best_move(self,players):
        return "INCOMPLETE"

    def get_hand_tile(self):
        user_input = input("Please enter a tile from your hand to play")
        for x in self.hand:
            if str(x) == user_input:
                return x
        print("Error: Tile not found in hand")
        print("Player " + self.playerID + "'s hand", end=": ")
        self.display_hand()

    def get_stack_tile(self,players):
        user_input = input("Please enter a tile from the stacks to play on")
        for c_player in players:
            for x in c_player.stack:
                if str(x) == user_input:
                    return x
        print("Error: Tile not found in stacks")
        for c_player in players:
            print("Player " + c_player.get_player_id() + "'s stack", end=": ")
            c_player.display_stack()

    def get_move(self,players):
        reccommened_move = self.get_best_move(players)
        print("Reccomended move: " + str(reccommened_move))
        hand_tile = self.get_hand_tile()
        stack_tile = self.get_stack_tile(players)
        return 1

    def get_valid_move(self,players):
        move = self.get_move(self,players)








class tile():
    def __init__(self, left, right, player:player):
        self.left = left
        self.right = right
        self.player = player
        self.double = self.left == self.right

    def __lt__(self, other):
        return self.left+self.right < other.left+other.right

    def __gt__(self, other):
        return self.left+self.right > other.left+other.right

    def __eq__(self, other):
        return self.left+self.right == other.left+other.right

    def __le__(self, other):
        return self.left+self.right <= other.left+other.right

    def __ge__(self, other):
        return self.left+self.right >= other.left+other.right

    def __ne__(self, other):
        return self.left+self.right != other.left+other.right

    def __str__(self):
        return "|" + self.player.get_color()+str(self.left)+str(self.right)+"|"

    def display_tile(self):
        print("|"+self.player.get_color()+str(self.left)+str(self.right)+"|", end=" ")

class hand():

    def play_hand(self,players):
        for c_player in players:
            self.display_hand(c_player)
            print()
            self.display_stacks(players)
            c_player.get_valid_move(players)
    def display_stacks(self,players):
        for c_player_stack in players:
            print("Player " + c_player_stack.get_player_id() + "'s stack", end=": ")
            c_player_stack.display_stack()

    def display_hand(self,player):
        print("Player " + player.get_player_id() + "'s hand", end=": ")
        player.display_hand()
    def play_serialized_hand(self, players, hand_num=1):
        pass
    def score_hand(self):
        pass

class Round():
    def play_round(self,players,hand_num):
        #CLI
        print("\n\nStarting New Round: ")
        if hand_num == 1:
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(5)
        elif hand_num == 2:
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(6)
        elif hand_num == 3:
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(6)
        elif hand_num == 4:
            for c_player in players:
                c_player.move_from_boneyard_to_hand_n(4)
        else:
            self.score_round(players)
            self.play_again()
        c_hand = hand()
        # CLI
        print("\nHand "+str(hand_num)+":")
        c_hand.play_hand(players)
    def get_winner(self,players):
        return players[0]
class tournament():
    def __init__(self,player_num=4,double_set_length=9):
        self.players = []
        ask_to_serialize = self.ask_to_seralize()
        if ask_to_serialize:
            self.load_game()
        else:
            self.start_new_tournament(player_num, double_set_length)
    def load_game(self):
        pass
    def start_new_tournament(self,player_num, double_set_length):
        for x in range(0, player_num):
            temp_player = player()
            ex_player_colors = [x.get_color() for x in self.players]
            ex_player_ids = [x.get_player_id() for x in self.players]
            temp_player.create_new_player(ex_player_ids,ex_player_colors,double_set_length)
            self.players.append(temp_player)
        self.determine_order()

        round = Round()
        round.play_round(self.players,hand_num=1)
        round.get_winner()
        self.play_again()
    def play_again(self):
        pass
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
                        print("\n\nPlayer " + comp_player.get_player_id() + " and Player " + c_player.get_player_id() + " have equal tiles re-shuffling")
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


tournament = tournament()
