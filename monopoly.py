import random
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
        self.turns = 0

    def roll_dice(self, jailed):
        if jailed:
            return (random.randint(1, 6), random.randint(1, 6))
        else:
            return random.randint(1, 6) + random.randint(1, 6)

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

    #finds the price of the property given a Tile object
        #If the property is owned, the owner will be given a prompt to enter their selling price
            #If the price is too high, the active player can type 'rn' to renegotiate
                #rn can be used a maximum of three times before the turn ends
    def find_property_price(self, tile, rn):
        pass

    #Moves liquid assets of ejected players
    def redistribute_assets(self, player_index):
        pass

    def determine_buildable_structures(self, player):
        #This is where Monopoly gets complicated.  If a player owns all four tiles of a particular color group, then they can (for a fee) build houses on their tiles.
        #They can build one house per turn
        #The player can build a maximum of four houses per tile, at which point they can place a hotel on the tile
        #The player cannot unevenly increase the number of houses on a particular tile:
        #The difference between the number of houses on each tile cannot exceed one.  So something like (0, 0, 1), (0, 0, 0), (1, 2, 1) are all fine, but (0, 2, 0) or (1, 4, 1) are not okay.
        pass

    def advance_turn(self):
        active_player = self.players[self.turns % len(self.players)]
        active_player.position += self.roll_dice(False)

    #Recursive
    def build_decision_tree(self, active_player):
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
        #Can be utility, property, rail road, jail, go_deck, or chance_deck
        self.type = type

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        #Contains a list of Tile objects the player currently owns properties on, each Tile object contains a list of Structures the player has built upon it, for determining rent/resale value
        self.property_holdings = None
        #keys can either be player names, or the bank
        self.debts = {}
        self.consecutive_turns = 0
        #Might axe this attribute after finishing the Tile subclasses, I don't think anything in the game is dependent upon knowing if the player is jailed or not jailed, aside from the dice roll method
        self.jailed = False

#A board object is a list of Tile objects,
class Board:
    def __init__(self):
        self.board = [RailRoadTile(5, None, Property(name='Reading Railroad', price=200, type='railroad'))]

class Tile:
    def __init__(self, position, color, property):
        self.position = position
        self.color = color
        self.property = property
        self.structures = []

    #Find owner of the tile in question, if no owner, return None
    def find_owner(self, players):
        for player in players:
            for property in player.property_holdings:
                if property.position == self.position:
                    return player
        return None

    #TODO come up with base case for if_owned
    def if_owned(self, player, owner, dice_roll):
        pass

    #I think the base case for is_not_owned is to treat it like Free Parking, or do nothing.
    def if_not_owned(self, player):
        pass

    #Below method finds out how many similar properties an owner has
    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if tile.property.type == self.property.type:
                num_tiles += 1
        return num_tiles


class RailRoadTile(Tile):

    def if_owned(self, player, owner, dice_roll=None):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        player.liquid_holdings -= 25 * 2**(num_owned_railroads - 1)
        owner.liquid_holdings += 25 * 2**(num_owned_railroads - 1)

    def if_not_owned(self, player):
        if player.liquid_holdings >= self.property.price:
            buy_decision = input(f'{self.property.name} is unoccupied, you can buy it for ${self.property.price}, do you want to?')
            if buy_decision.lower() in ['true', 'yes', 'y', 't', '1']:
                player.property_holdings.append(self)
                player.liquid_holdings -= self.property.price


#This gets a bit weird...  So I need to know the size of the dice roll that caused the player to land on this tile
class UtilityTile(Tile):

    def if_owned(self, player, owner, dice_roll):
        num_owned_utilites = self.count_similar_owned_properties(owner)
        if num_owned_utilites == 1:
            owner.liquid_holdings += dice_roll * 4
            player.liquid_holdings -= dice_roll * 4
        if num_owned_utilites == 2:
            owner.liquid_holdings += dice_roll * 10
            player.liquid_holdings -= dice_roll * 10

    def if_not_owned(self, player):
        if player.liquid_holdings >= self.property.price:
            buy_decision = input(f'{self.property.name} is available, you can buy it for ${self.property.price}, do you want to?')
            if buy_decision.lower() in ['true', 'yes', 'y', 't', '1']:
                player.property_holdings.append(self)
                player.liquid_holdings -= self.property.price


#Tax, Jail, Card, and Go Tiles cannot be purchased
class TaxTile(Tile):
    pass

class JailTile(Tile):

    def jailed_dice_roll(self, player):
        if player.consecutive_turns == 3:
            dice_roll = Monopoly().roll_dice(True)
            if dice_roll[1] == dice_roll[2]:
                player.position += dice_roll[1] + dice_roll[2]
            else:
                player.position += dice_roll[1] + dice_roll[2]
                player.consecutive_turns = 0
                player.liquid_holdings -= 50
                player.jailed = False
        if player.consecutive_turns < 3:
            dice_roll = Monopoly().roll_dice(True)
            if dice_roll[1] == dice_roll[2]:
                player.position += dice_roll[1] + dice_roll[2]
            else:
                player.consecutive_turns += 1

    def pay_fine(self, player):
        player.liquid_holdings -= 50
        player.position += Monopoly().roll_dice(False)
        player.jailed = False

class GoTile(Tile):

    def give_funds(self, player):
        player.liquid_holdings += 200

class ColorTile(Tile):

    def build_structues(self, player):
        pass

class CardTile(Tile):

    def draw_card(self, player):
        pass

