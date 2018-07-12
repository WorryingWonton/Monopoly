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

    def __init__(self, face, action, holdable, passes_go):
        self.face = face
        self.action = action
        self.holdable = holdable
        self.passes_go = passes_go

class Deck:

    #sub_type can either be community or chance
    def __init__(self, sub_type):
        self.sub_type = sub_type
        self.cards = []

    def make_deck(self):
        if self.sub_type.lower() == 'chance':
            self.cards = [Card('Advance to Go', advance_to_go, False, False),
                          Card('Bank error in your favor', bank_error_in_your_favor, False, False),
                          Card('Doctor\'s fees', doctors_fee, False, False),
                          Card('From sale of stock you get $50', from_sale_of_stock_50, False, False),
                          Card('Get out of Jail Free', get_out_jail_free, True, False),
                          Card('Go to Jail', go_to_jail, False, False),
                          Card('Grand Opera Night', grand_opera_night, False, False),
                          Card('Holiday', holiday_fund_matures, False, False),
                          Card('Income tax refund', income_tax_refund, False, False),
                          Card('Life insurance matures', life_insurace_matures, False, False),
                          Card('Pay hospital fees', pay_hospital_fees, False, False),
                          Card('Pay school fees', pay_school_fees, False, False),
                          Card('Receive $25 consultancy fee', receive_25_consultancy_fee, False, False),
                          Card('Your are assessed for street repairs', you_are_assessed_for_street_repairs, False, False),
                          Card('You have won second prize in a beauty contest', you_have_won_second_prize_in_a_beauty_contest, False, False),
                          Card('You inherit $100', you_inherit_100, False, False)
                          ]
        elif self.sub_type.lower() == 'community':
            self.cards = [Card('Advance to Go', advance_to_go, False, False),
                          Card('Advance to Illinois Ave.', advance_to_illinois_ave, False, True),
                          Card('Advance to St. Charles Place', advance_to_st_charles_place, False, True),
                          Card('Advance toklen to nearest Utility', advance_to_nearest_utility, False, False),
                          Card('Advance token to the nearest Railraod', advance_token_to_nearset_railroad, False, False),
                          Card('Bank pays you dividend of $50', bank_pays_you_50_dividend, False, False),
                          Card('Get out of Jial Free', get_out_jail_free, True, False),
                          Card('Go back 3 Spaces', go_back_3_spaces, False, False),
                          Card('Go to Jail', go_to_jail, False, False),
                          Card('Make general repairs on all your property', make_general_repairs_on_all_property, False, False),
                          Card('Pay poor tax of $15', pay_poor_tax, False, False),
                          Card('Take a trip to Reading Railroad', take_trip_to_reading_railroad, False, True),
                          Card('Take a walk on the Boardwalk', take_a_walk_on_boardwalk, False, False),
                          Card('You have been elected Chairman of the Board', chairman_of_the_board, False, False),
                          Card('Your building loan matures', your_building_loan_matures, False, False),
                          Card('You have won a crossword competition', you_have_won_a_crossword_competition, False, False)]
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
        self.board = [GoTile(0, None, None),
                      ColorTile(1, 'brown', property=Property(name='Mediterranean Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 10), Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 160), Structure('hotel', 50, 250)], base_rent=2)),
                      CardTile(2, None, None),
                      ColorTile(3, 'brown', property=Property(name='Baltic Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 20), Structure('house', 50, 60), Structure('house', 50, 180), Structure('house', 50, 320), Structure('hotel', 50, 450)], base_rent=4)),
                      IncomeTaxTile(4, None, None),
                      RailRoadTile(5, None, Property(name='Reading Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(6, 'cyan', property=Property(name='Oriental Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      CardTile(7, None, None),
                      ColorTile(8, 'cyan', property=Property(name='Vermont Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      ColorTile(9, 'cyan', property=Property(name='Connecticut Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 40), Structure('house', 50, 100), Structure('house', 50, 300), Structure('house', 50, 450), Structure('hotel', 50, 600)], base_rent=8)),
                      JailTile(10, None, None),
                      ColorTile(11, 'pink', property=Property(name='St. Charles Place', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      UtilityTile(12, None, property=Property(name='Electric Company', price=150, mortgage_price=75, possible_structures=None, base_rent=None)),
                      ColorTile(13, 'pink', property=Property(name='States Avenue', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      ColorTile(14, 'pink', property=Property(name='Virginia Avenue', price=160, mortgage_price=80, possible_structures=[Structure('house', 100, 60), Structure('house', 100, 180), Structure('house', 100, 500), Structure('house', 100, 700), Structure('hotel', 100, 900)], base_rent=12)),
                      RailRoadTile(15, None, Property(name='Pennsylvania Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(16, 'orange', property=Property(name='St. James Place', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      CardTile(17, None, None),
                      ColorTile(18, 'orange', property=Property(name='Tennessee Avenue', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      ColorTile(19, 'orange', property=Property(name='New York Avenue', price=200, mortgage_price=100, possible_structures=[Structure('house', 100, 80), Structure('house', 100, 220), Structure('house', 100, 600), Structure('house', 100, 800), Structure('hotel', 100, 1000)], base_rent=16)),
                      FreeParking(20, None, None),
                      ColorTile(21, 'red', property=Property(name='Kentucky Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      CardTile(22, None, None),
                      ColorTile(23, 'red', property=Property(name='Indiana Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      ColorTile(24, 'red', property=Property(name='Illinois Avenue', price=240, mortgage_price=120, possible_structures=[Structure('house', 150, 100), Structure('house', 150, 300), Structure('house', 150, 750), Structure('house', 150, 925), Structure('hotel', 150, 1100)], base_rent=20)),
                      RailRoadTile(25, None, Property(name='B. & O. Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(26, 'yellow', property=Property(name='Atlantic Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      ColorTile(27, 'yellow', property=Property(name='Ventnor Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      UtilityTile(28, None, property=Property(name='Water Works', price=150, mortgage_price=75, possible_structures=None, base_rent=None)),
                      ColorTile(29, 'yellow', property=Property(name='Marvin Gardens', price=280, mortgage_price=140, possible_structures=[Structure('house', 150, 120), Structure('house', 150, 360), Structure('house', 150, 850), Structure('house', 150, 1025), Structure('hotel', 150, 1200)], base_rent=24)),
                      GoToJailTile(30, None, None),
                      ColorTile(31, 'green', property=Property(name='Pacific Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 200, 1275)], base_rent=26)),
                      ColorTile(32, 'green', property=Property(name='North Carolina Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 150, 1275)], base_rent=26)),
                      CardTile(33, None, None),
                      ColorTile(34, 'green', property=Property(name='Pennsylvania Avenue', price=320, mortgage_price=150, possible_structures=[Structure('house', 200, 150), Structure('house', 200, 450), Structure('house', 200, 1000), Structure('house', 200, 1200), Structure('hotel', 200, 1400)], base_rent=28)),
                      RailRoadTile(35, None, Property(name='Short Line', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      CardTile(36, None, None),
                      ColorTile(37, 'blue', property=Property(name='Park Place', price=350, mortgage_price=175, possible_structures=[Structure('house', 200, 175), Structure('house', 200, 500), Structure('house', 200, 1100), Structure('house', 200, 1300), Structure('hotel', 200, 1500)], base_rent=35)),
                      LuxuryTaxTile(38, None, None),
                      ColorTile(39, 'blue', property=Property(name='Boardwalk', price=400, mortgage_price=200, possible_structures=[Structure('house', 200, 200), Structure('house', 200, 600), Structure('house', 200, 1400), Structure('house', 200, 1700), Structure('hotel', 200, 2000)], base_rent=50)),
                      ]

class Tile:

    def __init__(self, position, color, property):
        self.position = position
        self.color = color
        self.property = property

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
            if isinstance(self, tile):
                num_tiles += 1
        return num_tiles

class RailRoadTile(Tile):

    def if_owned(self, player, owner, dice_roll=None):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        #If the current tile has a trainstation on it
        if self.property.existing_structures[0].type == 'trainstation':
            player.liquid_holdings -= self.property.base_rent * 4**(num_owned_railroads - 1)
            owner.liquid_holdings += self.property.base_rent * 4**(num_owned_railroads - 1)
        else:
            player.liquid_holdings -= self.property.base_rent * 2**(num_owned_railroads - 1)
            owner.liquid_holdings += self.property.base_rent * 2**(num_owned_railroads - 1)

    def build_train_station(self, player):
        if player.liquid_holdings >= self.property.possible_structures[0].price:
            player.liquid_holdings -= self.property.possible_structures[0].price
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
            #Structures Case
            if len(self.property.existing_structures) > 1:
                return self.property.existing_structures[-1].rent
            #Monopoly case (But not yet any structures)
            else:
                return self.property.base_rent * 2
        #Base case
        else:
            return self.property.base_rent

    #If possible, returns the next buildable structure object from the Tile's list of possible structure
    def build_evenly(self, player):
        if len(self.property.existing_structures) == 0:
            return self.property.possible_structures[0]
        else:
            struct_count = [len(x.property.existing_structrues) for x in filter(lambda x: x.color == self.color, player.property_holdings)]
            if max(struct_count) - min(struct_count) > 1:
                raise Exception(f'The difference between the minimum and maximum number of structures on the {self.color} tiles has exceeded 1.  Min: {min(struct_count)} Max: {max(struct_count)}')
            elif len(self.property.existing_structures) == min(struct_count) and min(struct_count) != max(struct_count):
                return self.property.possible_structures[min(struct_count)]
            else:
                return None

    def build_structues(self, player):
        if self.color in player.determine_buildable_tiles():
            new_structure = self.build_evenly(player)
            if new_structure:
                if new_structure.price <= player.liquid_holdings:
                    self.property.existing_structures.append(new_structure)
                    player.liquid_holdings -= new_structure.price
                else:
                    return f'Insufficent funds.  Your liquid holdings total {player.liquid_holdings}, the structure\'s price is {new_structure.price}'

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








    

        