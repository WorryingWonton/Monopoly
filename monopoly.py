from distutils.util import strtobool
#This feels like I might be creating a circular dependency between these modules and monopoly, since these import from monopoly and monopoly imports from them
from community_chest_functions import *
from chance_deck_functions import *
import attr
import monopoly_helper_functions
import random

class Monopoly:

    def __init__(self):
        #each player in the list contains information on their name, position, liquid and property holdings
        #players whose net holdings are zero are ignored (might also design to just remove them from the list)
        self.players = []
        self.board = Board().board
        self.chance_deck = Deck.build_chance_deck()
        self.community_deck = Deck.build_communbity_deck()
        self.turns = 0

    def add_player(self, name):
        self.players.append(Player(name, game=self))

    #Checks value of net value of assets for each player, if sum(player.debts) >= player.liquid_holdings (ie the net worth of the player is zero), then they are removed from the list of players
    def eject_bankrupt_players(self):
        for player in self.players:
            if player.find_gross_worth() - player.debts <= 0:
                self.players.remove(player)

    def advance_turn(self):
        self.turns += 1

    @property
    def active_player(self):
        return self.players[self.turns % len(self.players)]



    #Auto execute the correct initial action for each Tile object when landed upon, or when occupied by the active_player
        #Returns a list of possible actions the player can perform
    def perform_tile_actions(self, active_player):
        option_list = []
        return option_list

    def run_turn(self):
        dice_roll = HelperFunctions.roll_dice()
        option_list = self.board[self.active_player.position].tile_actions(self.active_player, self.players, dice_roll)
        #active_player_decision = interface.get_decision(option_list)
        #self.execute_player_decision(active_player_decision)
        pass

    def execute_player_decision(self, active_player_decision):
        pass



    #Requries that all players that are going to participate have been added
        #Runs until someone wins, more precisely that the number of players is wittled down to one.
        #Returns the last remaining player
    def run_game(self):
        while len(self.players) > 1:
            self.run_turn()
            self.eject_bankrupt_players()
            self.advance_turn()
        return self.players[0]


#The board object is a list of Tile objects
class Board:

    def __init__(self):
        self.board = [GoTile(position=0),
                      ColorTile(position=1, color='brown', property=Property(name='Mediterranean Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 10), Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 160), Structure('hotel', 50, 250)], base_rent=2)),
                      CardTile(position=2),
                      ColorTile(position=3, color='brown', property=Property(name='Baltic Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 20), Structure('house', 50, 60), Structure('house', 50, 180), Structure('house', 50, 320), Structure('hotel', 50, 450)], base_rent=4)),
                      IncomeTaxTile(position=4),
                      RailRoadTile(position=5, property=Property(name='Reading Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(position=6, color='cyan', property=Property(name='Oriental Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      CardTile(position=7),
                      ColorTile(position=8, color='cyan', property=Property(name='Vermont Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      ColorTile(position=9, color='cyan', property=Property(name='Connecticut Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 40), Structure('house', 50, 100), Structure('house', 50, 300), Structure('house', 50, 450), Structure('hotel', 50, 600)], base_rent=8)),
                      JailTile(position=10),
                      ColorTile(position=11, color='pink', property=Property(name='St. Charles Place', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      UtilityTile(position=12, property=Property(name='Electric Company', price=150, mortgage_price=75, possible_structures=None, base_rent=None)),
                      ColorTile(position=13, color='pink', property=Property(name='States Avenue', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      ColorTile(position=14, color='pink', property=Property(name='Virginia Avenue', price=160, mortgage_price=80, possible_structures=[Structure('house', 100, 60), Structure('house', 100, 180), Structure('house', 100, 500), Structure('house', 100, 700), Structure('hotel', 100, 900)], base_rent=12)),
                      RailRoadTile(position=15, property=Property(name='Pennsylvania Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(position=16, color='orange', property=Property(name='St. James Place', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      CardTile(position=17),
                      ColorTile(position=18, color='orange', property=Property(name='Tennessee Avenue', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      ColorTile(position=19, color='orange', property=Property(name='New York Avenue', price=200, mortgage_price=100, possible_structures=[Structure('house', 100, 80), Structure('house', 100, 220), Structure('house', 100, 600), Structure('house', 100, 800), Structure('hotel', 100, 1000)], base_rent=16)),
                      FreeParking(position=20),
                      ColorTile(position=21, color='red', property=Property(name='Kentucky Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      CardTile(position=22),
                      ColorTile(position=23, color='red', property=Property(name='Indiana Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      ColorTile(position=24, color='red', property=Property(name='Illinois Avenue', price=240, mortgage_price=120, possible_structures=[Structure('house', 150, 100), Structure('house', 150, 300), Structure('house', 150, 750), Structure('house', 150, 925), Structure('hotel', 150, 1100)], base_rent=20)),
                      RailRoadTile(position=25, property=Property(name='B. & O. Railroad', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      ColorTile(position=26, color='yellow', property=Property(name='Atlantic Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      ColorTile(position=27, color='yellow', property=Property(name='Ventnor Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      UtilityTile(position=28, property=Property(name='Water Works', price=150, mortgage_price=75, possible_structures=None, base_rent=None)),
                      ColorTile(position=29, color='yellow', property=Property(name='Marvin Gardens', price=280, mortgage_price=140, possible_structures=[Structure('house', 150, 120), Structure('house', 150, 360), Structure('house', 150, 850), Structure('house', 150, 1025), Structure('hotel', 150, 1200)], base_rent=24)),
                      GoToJailTile(position=30),
                      ColorTile(position=31, color='green', property=Property(name='Pacific Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 200, 1275)], base_rent=26)),
                      ColorTile(position=32, color='green', property=Property(name='North Carolina Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 150, 1275)], base_rent=26)),
                      CardTile(position=33),
                      ColorTile(position=34, color='green', property=Property(name='Pennsylvania Avenue', price=320, mortgage_price=150, possible_structures=[Structure('house', 200, 150), Structure('house', 200, 450), Structure('house', 200, 1000), Structure('house', 200, 1200), Structure('hotel', 200, 1400)], base_rent=28)),
                      RailRoadTile(position=35, property=Property(name='Short Line', price=200, mortgage_price=100 , possible_structures=Structure('trainstation', 100, 50), base_rent=25)),
                      CardTile(position=36),
                      ColorTile(position=37, color='blue', property=Property(name='Park Place', price=350, mortgage_price=175, possible_structures=[Structure('house', 200, 175), Structure('house', 200, 500), Structure('house', 200, 1100), Structure('house', 200, 1300), Structure('hotel', 200, 1500)], base_rent=35)),
                      LuxuryTaxTile(position=38),
                      ColorTile(position=39, color='blue', property=Property(name='Boardwalk', price=400, mortgage_price=200, possible_structures=[Structure('house', 200, 200), Structure('house', 200, 600), Structure('house', 200, 1400), Structure('house', 200, 1700), Structure('hotel', 200, 2000)], base_rent=50)),
                      ]

class Card:
    def __init__(self, face, action, holdable, passes_go):
        self.face = face
        self.action = action
        self.holdable = holdable
        self.passes_go = passes_go
        self.parent_deck = None


@attr.s
class Deck:
    cards = attr.ib(factory=list)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    #Cards are read from the top of each deck, and re-inserted at the bottom their action is performed
    def deal_from_deck(self, active_player):
        card = self.cards[0]
        if card.holdable:
            active_player.hand.append(card)
            self.cards.remove(card)
        else:
            card.action(active_player)
            del self.cards[0]
            self.cards.append(card)

    def add_card(self, card):
        self.cards.append(card)
        card.parent_deck = self

    @staticmethod
    def build_chance_deck():
        chance_deck = Deck()
        cards = [Card(face='Advance to Go', action=advance_to_go, holdable=False, passes_go=False),
                 Card(face='Advance to Illinois Ave.', action=advance_to_illinois_ave, holdable=False, passes_go=True),
                 Card(face='Advance to St. Charles Place', action=advance_to_st_charles_place, holdable=False, passes_go=True),
                 Card(face='Advance toklen to nearest Utility', action=advance_to_nearest_utility, holdable=False, passes_go=False),
                 Card(face='Advance token to the nearest Railraod', action=advance_token_to_nearset_railroad, holdable=False, passes_go=False),
                 Card(face='Bank pays you dividend of $50', action=bank_pays_you_50_dividend, holdable=False, passes_go=False),
                 Card(face='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False),
                 Card(face='Go back 3 Spaces', action=go_back_3_spaces, holdable=False, passes_go=False),
                 Card(face='Go to Jail', action=go_to_jail, holdable=False, passes_go=False),
                 Card(face='Make general repairs on all your property', action=make_general_repairs_on_all_property, holdable=False, passes_go=False),
                 Card(face='Pay poor tax of $15', action=pay_poor_tax, holdable=False, passes_go=False),
                 Card(face='Take a trip to Reading Railroad', action=take_trip_to_reading_railroad, holdable=False, passes_go=True),
                 Card(face='Take a walk on the Boardwalk', action=take_a_walk_on_boardwalk, holdable=False, passes_go=False),
                 Card(face='You have been elected Chairman of the Board', action=chairman_of_the_board, holdable=False, passes_go=False),
                 Card(face='Your building loan matures', action=your_building_loan_matures, holdable=False, passes_go=False),
                 Card(face='You have won a crossword competition', action=you_have_won_a_crossword_competition, holdable=False, passes_go=False)]
        for card in cards: chance_deck.add_card(card)
        return chance_deck

    @staticmethod
    def build_communbity_deck():
        community_deck = Deck()
        cards = [Card(face='Advance to Go', action=advance_to_go, holdable=False, passes_go=False),
                  Card(face='Bank error in your favor', action=bank_error_in_your_favor, holdable=False, passes_go=False),
                  Card(face='Doctor\'s fees', action=doctors_fee, holdable=False, passes_go=False),
                  Card(face='From sale of stock you get $50', action=from_sale_of_stock_50, holdable=False, passes_go=False),
                  Card(face='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False),
                  Card(face='Go to Jail', action=go_to_jail, holdable=False, passes_go=False),
                  Card(face='Grand Opera Night', action=grand_opera_night, holdable=False, passes_go=False),
                  Card(face='Holiday', action=holiday_fund_matures, holdable=False, passes_go=False),
                  Card(face='Income tax refund', action=income_tax_refund, holdable=False, passes_go=False),
                  Card(face='Life insurance matures', action=life_insurace_matures, holdable=False, passes_go=False),
                  Card(face='Pay hospital fees', action=pay_hospital_fees, holdable=False, passes_go=False),
                  Card(face='Pay school fees', action=pay_school_fees, holdable=False, passes_go=False),
                  Card(face='Receive $25 consultancy fee', action=receive_25_consultancy_fee, holdable=False, passes_go=False),
                  Card(face='Your are assessed for street repairs', action=you_are_assessed_for_street_repairs, holdable=False, passes_go=False),
                  Card(face='You have won second prize in a beauty contest', action=you_have_won_second_prize_in_a_beauty_contest, holdable=False, passes_go=False),
                  Card(face='You inherit $100', action=you_inherit_100, holdable=False, passes_go=False)]
        for card in cards: community_deck.add_card(card)
        return community_deck


class Player:

    def __init__(self, name, game):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        #Contains a list of Tile objects the player currently owns properties on
        self.property_holdings = []
        self.debts = 0
        self.consecutive_turns = 0
        #Might axe this attribute after finishing the Tile subclasses, I don't think anything in the game is dependent upon knowing if the player is jailed or not jailed, aside from the dice roll method
        self.jailed = False
        self.hand = []
        self.game = game

    def find_gross_worth(self):
        gross_worth = self.liquid_holdings
        for property in self.property_holdings:
            if property.mortgaged:
                gross_worth += property.mortgage_price
            else:
                gross_worth += property.price
            if len(property.existing_structures) > 0:
                for structure in property.existing_structures:
                  gross_worth += structure[1]
        return gross_worth

    def advance_position(self, amount):
        if self.position + amount < 0:
            self.position += 40
        self.position = (self.position + amount) % 40

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

    def get_tile_at_player_position(self):
        return self.game.board[self.position]

    def consume_held_card(self, card_face, card_deck):
        cards = list(filter(lambda card: card.face == card_face.lower() and card.parent_deck == card_deck.lower(), self.game.active_player.hand))
        if len(cards) > 1:
            raise Exception(f'Duplicate cards in deck, there are {len(cards)} instances of {cards[0].face} belonging to the {cards[0].parent_deck} deck')
        elif len(cards) == 0:
            raise Exception(f'{card_face} beloning to the {card_deck} deck was not found in {self.game.active_player.name}\'s hand')
        else:
            card = cards[0]
            card.action(self.game.active_player)
            if card.parent_deck == 'community':
                self.community_deck.append(card)
            else:
                self.chance_deck.append(card)

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

#tile_action(self) --- Performs the relevant actions for a tile when called.

@attr.s
class Tile:
    position = attr.ib(type=int)

    #Performs all appropriate actions associated with the Tile object in play
        #Assumes active_player is on the Tile

    def tile_actions(self, active_player, players, dice_roll):
        pass


#Should be able to tell if the property on the Tile is on the market, how many like tiles the Owner of the landed on tile has, determine if the Tile can be sold (I think this may be unique to color tiles)
@attr.s
class OwnableTile(Tile):
    property: Property = attr.ib()

    #Find owner of the tile in question, if no owner, return None
    def find_owner(self, players):
        for player in players:
            for property in player.property_holdings:
                if property.position == self.position:
                    return player
        return None

    def if_owned(self, player, owner, dice_roll):
        pass

    def if_not_owned(self, player, buy_decision):
        if player.liquid_holdings >= self.property.price:
            # buy_decision = strtobool(input(f'{self.property.name} is available.  \nYou can buy it for {self.property.price} or mortage it for {self.property.mortgage_price}\n Enter \'Buy\' \'Mortgage\' or \'Pass\'').lower())
            if buy_decision == 'buy':
                player.property_holdings.append(self)
                player.liquid_holdings -= self.property.price
            elif buy_decision == 'mortgage':
                player.liquid_holdings -= self.property.mortgage_price
                self.property.mortgaged = True
                player.property_holdings.append(self)
            else:
                return None

    #Below method finds out how many similar properties an owner has
    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if isinstance(self, tile):
                num_tiles += 1
        return num_tiles


    def determine_if_sellable(self, player):
        if self in player.property_holdings:
            if len(self.property.existing_structures) > 0:
                return False
            else:
                return True
        else:
            return False

    def sell_property(self, player):
        if self in player.property_holdings:
            player.property_holdings.remove(self)
            player.liquid_holdings += self.property.price
        else:
            raise Exception(f'{self.property.name} is not owned by {player.name}')



@attr.s
class UnownableTile(Tile):
    pass


@attr.s
class RailRoadTile(OwnableTile):
    def tile_actions(self, active_player, players, dice_roll, dealt_card):
       owner = self.find_owner(players)
       if owner:
            if owner == active_player:
                return True
            elif dealt_card.action == advance_token_to_nearset_railroad:
                self.if_owned(active_player, owner, dice_roll, dealt_card)
       else:
           return False

    def if_owned(self, player, owner, dice_roll=None, dealt_card = None):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        #If the current tile has a trainstation on it
        multiplier = 1
        if dealt_card:
            multiplier = 2
        if self.property.existing_structures[0].type == 'trainstation':
            player.liquid_holdings -= multiplier * self.property.base_rent * 4**(num_owned_railroads - 1)
            owner.liquid_holdings += multiplier * self.property.base_rent * 4**(num_owned_railroads - 1)
        else:
            player.liquid_holdings -= multiplier * self.property.base_rent * 2**(num_owned_railroads - 1)
            owner.liquid_holdings += multiplier * self.property.base_rent * 2**(num_owned_railroads - 1)

    def build_train_station(self, player):
        if player.liquid_holdings >= self.property.possible_structures[0].price:
            player.liquid_holdings -= self.property.possible_structures[0].price
            self.property.existing_structures.append(self.property.possible_structures)


#This gets a bit weird...  So I need to know the size of the dice roll that caused the player to land on this tile
@attr.s
class UtilityTile(OwnableTile):

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
@attr.s
class IncomeTaxTile(UnownableTile):

    @staticmethod
    def deduct_taxes(player):
        gross_worth = player.find_gross_worth()
        if gross_worth <= 2000:
            player.liquid_holdings -= .1 * gross_worth
        else:
            player.liquid_holdings -= 200

@attr.s
class JailTile(UnownableTile):

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

@attr.s
class GoTile(UnownableTile):

    @staticmethod
    def give_funds(player):
        player.liquid_holdings += 200

@attr.s
class ColorTile(OwnableTile):
    color = attr.ib(type=str)
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
    #add_or_remove = boolean for if the method is being called to add or remove a structure
    #Turns out adding the ability to remove structures following the build even rule took more than two lines of code, but still a simple change
    def build_evenly(self, player, add_structure):
        if len(self.property.existing_structures) == 0:
            if add_structure:
                return self.property.possible_structures[0]
            else:
                return None
        else:
            struct_count = [len(x.property.existing_structrues) for x in filter(lambda x: x.color == self.color, player.property_holdings)]
            if max(struct_count) - min(struct_count) > 1:
                raise Exception(f'The difference between the minimum and maximum number of structures on the {self.color} tiles has exceeded 1.  Min: {min(struct_count)} Max: {max(struct_count)}')

            elif add_structure and len(self.property.existing_structures) == min(struct_count) and min(struct_count) != max(struct_count):
                return self.property.possible_structures[min(struct_count)]
            elif len(self.property.existing_structures) == max(struct_count):
                return self.property.existing_structures[-1]
            else:
                return None

    def build_structues(self, player):
        if self.color in player.determine_buildable_tiles():
            new_structure = self.build_evenly(player, False)
            if new_structure:
                if new_structure.price <= player.liquid_holdings:
                    self.property.existing_structures.append(new_structure)
                    player.liquid_holdings -= new_structure.price
                else:
                    return f'Insufficent funds.  Your liquid holdings total {player.liquid_holdings}, the structure\'s price is {new_structure.price}'

    #It might make sense to make this more defensive, but the determineation of whether or not a structure can be removed is handled by self.build_evenly()
    def remove_structures(self):
        self.property.existing_structures.remove(-1)

@attr.s
class CardTile(UnownableTile):

    @staticmethod
    def draw_card(player, deck):
        card = deck[-1]
        card.action(player)

@attr.s
class GoToJailTile(UnownableTile):

    @staticmethod
    def go_to_jail(player):
        player.jailed = True
        player.position = 10

@attr.s
class LuxuryTaxTile(UnownableTile):

    @staticmethod
    def pay_luxury_tax(player):
        player.liquid_holdings -= 75

#This Tile does nothing, however it is the only Tile which truly does nothing, therefore it gets its own class
@attr.s
class FreeParking(Tile):
    pass


class Structure():
    def __init__(self, type, price, rent):
        self.type = type
        self.price = price
        self.rent = rent






        