class Monopoly:

    def __init__(self):
        #each player in the list contains information on their name, position, liquid and property holdings
        #players whose net holdings are zero are ignored (might also design to just remove them from the list)
        self.players = []
        self.chance_deck = Deck(sub_type='Chance').make_deck()
        self.community_deck = Deck(sub_type='Community').make_deck()
        #key = Property object, value = Player object
        self.property_owners = {}
        self.board = Board

    def roll_dice(self):
        pass

    def add_player(self, name):
        self.players.append(Player(name))

    #Checks value of net value of assets for each player, if sum(player.debts) >= player.liquid_holdings (ie the net worth of the player is zero), then they are removed from the list of players
    def eject_bankrupt_players(self):
        for player in self.players:
            if player.liquid_holdings - sum(player.debts.values()) <= 0:
                self.players.remove(player)

    def determine_tile_state(self, tile):
        pass

    def find_property_owner_of_tile(self, tile):
        pass

    #Moves liquid assets of ejected players
    def redistribute_assets(self, player_index):
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

class Property:
    def __init__(self, name, price, type):
        self.name = name
        self.price = price
        self.type = type

class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        self.property_holdings = None
        #keys can either be player names, or the bank
        self.debts = {}
        self.consecutive_turns = 0
        self.jailed = False

class Board:
    def __init__(self):
        self.board = {}
        self.make_board()


    def make_board(self):
        #key is position number, value is a list containing the space name, and the action to take at said space
        self.spaces = []

class Tile:
    def __init__(self, position, color, action, property):
        self.position = position
        self.color = color
        self.action = action
        self.property = property
        self.structures = []












