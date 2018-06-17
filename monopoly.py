class Monopoly:

    def __init__(self):
        #each player in the list contains information on their name, position, liquid and property holdings
        #players whose net holdings are zero are ignored (might also design to just remove them from the list)
        self.players = []
        self.chance_deck = Deck(sub_type='Chance').make_deck()
        self.community_deck = Deck(sub_type='Community').make_deck()

    def roll_dice(self):
        pass

    def add_player(self, name):
        self.players.append(Player(name))

    def go_to_jail(self):
        pass

    #Checks value of net value of assets for each player, if sum(player.debts) >= player.liquid_holdings (ie the net worth of the player is zero), then they are removed from the list of players
    def eject_bankrupt_players(self):
        pass

    #Moves liquid assets of ejected players
    def redistribute_assets(self, player_index):
        pass

    #Reads the list of players, starting from the list of all possible actions the player can take, as a function of the other player's positions and assets, the action list is paired down to just those the player can legally perform.
    
    def generate_tree(self):
        pass


class Card:

    def __init__(self, face, action):
        self.face = face
        self.action = action

class Deck:

    #sub_type can either be community or chance
    def __init__(self, sub_type):
        self.sub_type = sub_type

    def make_deck(self):
        pass

    def shuffle_deck(self):
        pass

    def deal_from_deck(self):
        pass

class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        self.property_holdings = None
        #keys can either be player names, or the bank
        self.debts = {}
        self.consecutive_turns = 0


class Board:

    def make_board(self):
        #key is position number, value is
        self.pieces = {1: []}


        # def run_game(self):
        #     pass
        # self.player_positions = {}
        # self.player_liquid_holdings = {}
        # self.player_property_holdings = {}
        # self.community_chest_deck = []
        # self.chance_deck = []
        # self.board_position_states = {}



