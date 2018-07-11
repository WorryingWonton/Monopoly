import random
from distutils.util import strtobool
#This feels like I might be creating a circular dependency between these modules and monopoly, since these import from monopoly and monopoly imports from them
from community_chest_functions import *
from chance_deck_functions import *

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

    def add_player(self, name):
        self.players.append(Player(name))

    #Checks value of net value of assets for each player, if sum(player.debts) >= player.liquid_holdings (ie the net worth of the player is zero), then they are removed from the list of players
    def eject_bankrupt_players(self):
        for player in self.players:
            if player.find_gross_worth() - sum(player.debts) <= 0:
                self.players.remove(player)

    def advance_turn(self):
        active_player = self.players[self.turns % len(self.players)]
        self.turns += 1
        return active_player


class Card:

    def __init__(self, face, action, holdable):
        self.face = face
        self.action = action
        self.holdable = holdable

class Deck:

    #sub_type can either be community or chance
    def __init__(self, sub_type):
        self.sub_type = sub_type
        self.cards = []

    def make_deck(self):
        if self.sub_type.lower() == 'chance':
            self.cards = []
        elif self.sub_type.lower() == 'community':
            self.cards = []
        else:
            raise Exception(f'Unhandled subtype {self.sub_type}, acceptable subtypes are Chance and Community')

    def shuffle_deck(self):
        pass
    #Cards are read from the bottom of each deck
    def deal_from_deck(self):
        pass

class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        #Contains a list of Tile objects the player currently owns properties on
        self.property_holdings = None
        #keys can either be player names, or the bank
        self.debts = {}
        self.consecutive_turns = 0
        #Might axe this attribute after finishing the Tile subclasses, I don't think anything in the game is dependent upon knowing if the player is jailed or not jailed, aside from the dice roll method
        self.jailed = False
        self.hand = []


    def find_gross_worth(self):
        gross_worth = self.liquid_holdings
        for property in self.property_holdings:
            if property.mortgaged:
                gross_worth += property.mortgage_price
            else:
                gross_worth += property.price
            for structure in property.structures:
                gross_worth += structure[1]

    #Returns a list containing property colors where a given player can build on
    #Should not be called on rail road or utility tiles
    @staticmethod
    def determine_buildable_tiles(player):
        #Number of each colored tile
        color_group_dict = {'brown': 2, 'cyan': 3, 'pink': 3, 'orange': 3, 'red': 3, 'yellow': 3, 'green': 3, 'blue': 2}
        buildable_list = []
        for color in color_group_dict:
            count = 0
            for tile in player.property_holdings:
                if tile.color == color:
                    count += 1
            if color_group_dict[color] == count:

                buildable_list.append(color)
        return buildable_list


#A board object is a list of Tile objects,
class Board:

    def __init__(self):
        self.board = [GoTile(0, None, None, 'go'),
                      CardTile(2, None, None, 'chance'),
                      IncomeTaxTile(4, None, None, 'income_tax'),
                      RailRoadTile(5, None, Property(name='Reading Railroad', price=200, mortgage_price=100 , possible_structures=Structure('train station', 100, 50), base_rent=25), tile_type = 'railroad'),
                      CardTile(7, None, None, 'community'),
                      JailTile(10, None, None, 'jail'),
                      GoToJailTile(30, None, None, 'gotojail'),
                      LuxuryTaxTile(38, None, None, 'luxury_tax')]

class Tile:

    def __init__(self, position, color, property, tile_type):
        self.position = position
        self.color = color
        self.property = property
        #can be color, chance, community, jail, gotojail, utility, income_tax, luxury_tax, railroad, go
        self.tile_type = tile_type


    #Find owner of the tile in question, if no owner, return None
    def find_owner(self, players):
        for player in players:
            for property in player.property_holdings:
                if property.position == self.position:
                    return player
        return None

    def if_owned(self, player, owner, dice_roll):
        pass

    def if_not_owned(self, player):
        if player.liquid_holdings >= self.property.price:
            buy_decision = strtobool(input(f'{self.property.name} is available.  \nYou can buy it for {self.property.price} or mortage it for {self.property.mortgage_price}\n Enter \'Buy\' \'Mortgage\' or \'Pass\'').lower())
            if buy_decision == 'buy':
                player.property_holdings.append(self)
                player.liquid_holdings -= self.property.price
            elif buy_decision == 'mortgage':
                player.liquid_holdings -= self.property.mortgage_price
                self.property.mortgaged = True
                player.property_holdings.append(self)
            else:
                pass

    #Below method finds out how many similar properties an owner has
    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if tile.tile_type == self.tile_type:
                num_tiles += 1
        return num_tiles

class RailRoadTile(Tile):

    def if_owned(self, player, owner, dice_roll=None):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        #If the current tile has a trainstation on it
        if self.property.existing_structures[0].type == 'train station':
            player.liquid_holdings -= self.property.base_rent * 4**(num_owned_railroads - 1)
            owner.liquid_holdings += self.property.base_rent * 4**(num_owned_railroads - 1)
        else:
            player.liquid_holdings -= self.property.base_rent * 2**(num_owned_railroads - 1)
            owner.liquid_holdings += self.property.base_rent * 2**(num_owned_railroads - 1)

    def build_train_station(self, player):
        if player.liquid_holdings >= self.property.possible_structures.price:
            player.liquid_holdings -= self.property.possible_structures.price
            self.property.existing_structures.append(self.property.possible_structures)


#This gets a bit weird...  So I need to know the size of the dice roll that caused the player to land on this tile
class UtilityTile(Tile):

    def if_owned(self, player, owner, dice_roll):
        num_owned_utilites = self.count_similar_owned_properties(owner)
        if num_owned_utilites == 1:
            if self.property.mortgaged:
                player.liquid_holdings -= sum(dice_roll) * 4
            else:
                owner.liquid_holdings += sum(dice_roll) * 4
                player.liquid_holdings -= sum(dice_roll) * 4
        if num_owned_utilites == 2:
            if self.property.mortgaged:
                player.liquid_holdings -= sum(dice_roll) * 10
            else:
                owner.liquid_holdings += sum(dice_roll) * 10
                player.liquid_holdings -= sum(dice_roll) * 10


#Tax, Jail, Card, and Go Tiles cannot be purchased
class IncomeTaxTile(Tile):

    @staticmethod
    def deduct_taxes(player):
        gross_worth = player.find_gross_worth()
        if gross_worth < 200:
            player.liquid_holdings -= .1 * gross_worth
        if gross_worth >= 200:
            tax_decision =input(f'Your net worth is {gross_worth}, which is >= 200, would you like to pay $200, or ten percent of your net worth, which totals ${0.1 * gross_worth}\n Enter 200 to pay $200, or 10 to pay 10%')
            if tax_decision == '200':
                player.liquid_holdings -= 200
            else:
                player.liquid_holdings *= .9


class JailTile(Tile):

    @staticmethod
    def jailed_dice_roll(player):
        if player.consecutive_turns == 3:
            dice_roll = HelperFunctions.roll_dice()
            if dice_roll[1] == dice_roll[2]:
                player.position += dice_roll[1] + dice_roll[2]
            else:
                player.position += dice_roll[1] + dice_roll[2]
                player.consecutive_turns = 0
                player.liquid_holdings -= 50
                player.jailed = False
        if player.consecutive_turns < 3:
            dice_roll = HelperFunctions.roll_dice()
            if dice_roll[1] == dice_roll[2]:
                player.position += dice_roll[1] + dice_roll[2]
            else:
                player.consecutive_turns += 1

    @staticmethod
    def pay_fine(player):
        player.liquid_holdings -= 50
        player.position += sum(HelperFunctions.roll_dice())
        player.jailed = False

class GoTile(Tile):

    @staticmethod
    def give_funds(player):
        player.liquid_holdings += 200

class ColorTile(Tile):
    #Determine how many tiles the owner of this tile has, determine the number of structures on this tile, determine if mortgaged, deduct rent
    def if_owned(self, player, owner, dice_roll=None):
        rent = self.assess_rent(owner)
        player.liquid_holdings -= rent
        if not self.property.mortgaged:
            owner.liquid_holdings += rent

    def assess_rent(self, owner):
        if self.color in owner.determine_buildable_tiles():
            #Structures case
            if len(self.property.existing_structures) > 0:
                return self.property.existing_structures[-1].rent
            #Monopoly case
            else:
                return self.property.base_rent * 2
        #Base case
        else:
            return self.property.base_rent

    def build_structues(self, player):
        target_structure = self.property.possible_structures[len(self.property.existing_structures)]
        cost = target_structure.price
        if cost <= player.liquid_holdings:
            player.liquid_holdings -= cost
            self.property.existing_structures.append(target_structure)
        else:
            return f'Insufficent funds.  Your liquid holdings total {player.liquid_holdings}, the structure\'s price is {cost}'

class CardTile(Tile):

    @staticmethod
    def draw_card(player, deck):
        card = deck[-1]
        card.action(player)

class GoToJailTile(Tile):

    @staticmethod
    def go_to_jail(player):
        player.jailed = True
        player.position = 10

class LuxuryTaxTile(Tile):

    @staticmethod
    def pay_luxury_tax(player):
        player.liquid_holdings -= 75

#This Tile does nothing, however it is the only Tile which truly does nothing, therefore it gets its own class
class FreeParking(Tile):
    pass


class Property:

    def __init__(self, name, price, mortgage_price, possible_structures, base_rent):
        self.name = name
        self.price = price
        self.mortgage_price = mortgage_price
        #List of structure objects that can be built on the property
        self.possible_structures = possible_structures
        self.base_rent = base_rent
        self.existing_structures = []
        self.mortgaged = False

    def add_structure(self, structure):
        if structure in self.possible_structures:
            self.existing_structures += structure
        else:
            raise Exception('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')


class Structure():
    def __init__(self, type, price, rent):
        self.type = type
        self.price = price
        self.rent = rent


class HelperFunctions:
    
    @staticmethod
    def roll_dice():
        return (random.randint(1, 6), random.randint(1, 6))

    @staticmethod
    def afforadable(object, player):
        if player.liquid_holdings >= object.price:
            return True








    

        