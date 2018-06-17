class Monopoly:

    def __init__(self):
        #each player in the list contains information on their name, position, liquid and property holdings
        #players whose net holdings are zero are ignored (might also design to just remove them from the list)
        self.players = []
        self.chance_deck = Deck(sub_type='Chance').make_deck()
        self.community_deck = Deck(sub_type='Community').make_deck()

    def roll_dice(self):
        pass

    def run_game(self):
        pass
        # self.player_positions = {}
        # self.player_liquid_holdings = {}
        # self.player_property_holdings = {}
        # self.community_chest_deck = []
        # self.chance_deck = []
        # self.board_position_states = {}

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

    def __init__(self, name, position, liquid_holdings, property_holdings):
        self.name = name
        self.position = position
        self.liquid_holdings = liquid_holdings
        self.property_holdings = property_holdings

class Board:

    def make_board(self):
        self.pieces = {1: []}



