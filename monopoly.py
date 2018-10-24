from community_chest_functions import *
from chance_deck_functions import *
import attr
import monopoly_cl_interface
import random

class Monopoly:

    def __init__(self):
        self.players = []
        self.board = Board().board
        self.chance_deck = ChanceDeck().cards
        self.community_deck = CommunityChest().cards
        self.turns = 0
        self.auction_timer = 10
        self.doubles = False
        self.bank = Bank(game=self)
        self.dice_roll = None
        #Test mode parameter for dice_roll
        self.index = 0


    def add_player(self, name):
        self.players.append(Player(name, game=self))

    def eject_bankrupt_players(self):
        for player in self.players:
            if player.liquid_holdings < 0:
                self.players.remove(player)

    def advance_turn(self):
        self.turns += 1

    @property
    def active_player(self):
        return self.players[self.turns % len(self.players)]

    def roll_dice(self, mode=None):
        """
        This function returns a 2 tuple containing 2 randomly generated integers bound between 1 and 6
        roll_dice does NOT update the dice_roll attribute in the Monopoly class
        :param basestring mode: A string representing one of several possible test modes
        :var dict test_modes: A dictionary containing different test modes, to remove RNG from the game.
        :return tuple dice_roll:
        """
        #First turn scenario starting from GO
        if self.turns < len(self.players):
            test_modes = {'railroads': [(2, 3), (6, 4), (6, 4), (6, 4)]}
        #All players have had their first turn
        else:
            test_modes = {'railroads': [(6, 4), (6, 4), (6, 4), (6, 4)]}
        if mode:
            if self.turns % len(self.players) == 0:
                self.index += 1
            return test_modes[mode][self.index % len(test_modes)]
        else:
            return (random.randint(1, 6), random.randint(1, 6))

    def run_turn(self):
        self.dice_roll = self.roll_dice(mode='railroads')
        self.check_for_doubles()
        if self.active_player.jailed:
            pass
        else:
            self.active_player.advance_position(amount=self.dice_roll[0] + self.dice_roll[1])
        print(f'\n{self.active_player.liquid_holdings}: --- {self.turns} --- {self.active_player.name} --- Pos: {self.active_player.position} ---{[x.property.name for x in self.active_player.property_holdings]}')
        option_list = []
        tile_options = self.board[self.active_player.position].tile_actions(game=self)
        if tile_options:
            for tile in self.active_player.property_holdings:
                if tile.position == self.active_player.position:
                    continue
                options = tile.tile_actions(game=self)
                if options:
                    for option in options:
                        tile_options.append(option)
            option_list += tile_options
        player_options = self.active_player.player_actions()
        if len(player_options) > 0:
            option_list += player_options
        if len(option_list) > 0:
            active_player_decision = monopoly_cl_interface.CLInterface(game=self).get_decision(option_list)
            self.execute_player_decision(active_player_decision)

    #active_player_decision
        #Need to implement common interface amongst executvie methods:
            #Executive methods return None
    def execute_player_decision(self, active_player_decision):
        if active_player_decision:
            active_player_decision.action(self)

    def run_game(self):
        while len(self.players) > 1:
            self.run_turn()
            if self.doubles:
                self.active_player.consecutive_turns += 1
                if self.active_player.consecutive_turns >= 3:
                    self.turns += self.active_player.consecutive_turns
                    self.active_player.consecutive_turns = 0
                    self.active_player.go_directly_to_jail()
                    self.advance_turn()
                    self.doubles = False
                continue
            else:
                self.advance_turn()
        return self.players[0]

    def run_bankruptcy_process(self, creditor, debtor):
        #Perhaps unnecessary check to make sure the creditor is not being passed on debt
        if debtor.liquid_holdings >= 0:
            creditor.liquid_holdings += debtor.liquid_holdings
        for tile in debtor.property_holdings:
            if tile.property.mortgaged:
                creditor.liquid_holdings -= 0.1 * tile.property.mortgage_price
            for structure in tile.property.existing_structures:
                creditor.liquid_holdings += 0.5 * structure.price
                #Remove all structures after sale to bank
            tile.property.existing_structures = []
            creditor.property_holdings.append(tile)
        self.players.remove(debtor)
        if creditor == self.bank:
            self.run_bank_auction()

    def run_bank_auction(self):
        for tile in self.bank.property_holdings:
            winning_bid = monopoly_cl_interface.CLInterface(game=self).run_auction(item=tile.property, seller=self.bank)
            if winning_bid:
                tile.complete_transaction(buyer=winning_bid[0], seller=self.bank, amount=winning_bid[1])
        for card in self.bank.hand:
            winning_bid = monopoly_cl_interface.CLInterface(game=self).run_auction(item=card, seller=self.bank)
            if winning_bid:
                card.complete_transaction(buyer=winning_bid[0], seller=self.bank, amoun=winning_bid[1])
        self.bank.property_holdings = []
        self.bank.hand = []

    def check_for_doubles(self):
        if self.dice_roll[0] == self.dice_roll[1]:
            self.doubles = True

#The board object is a list of Tile objects
class Board:

    def __init__(self):
        self.board = [GoTile(position=0),
                      ColorTile(position=1, color='brown', property=Property(name='Mediterranean Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 10), Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 160), Structure('hotel', 50, 250)], base_rent=2)),
                      CardTile(position=2),
                      ColorTile(position=3, color='brown', property=Property(name='Baltic Avenue', price=60, mortgage_price=30, possible_structures=[Structure('house', 50, 20), Structure('house', 50, 60), Structure('house', 50, 180), Structure('house', 50, 320), Structure('hotel', 50, 450)], base_rent=4)),
                      IncomeTaxTile(position=4),
                      RailRoadTile(position=5, property=Property(name='Reading Railroad', price=200, mortgage_price=100 , possible_structures=[Structure('trainstation', 100, 50)], base_rent=25)),
                      ColorTile(position=6, color='cyan', property=Property(name='Oriental Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      CardTile(position=7),
                      ColorTile(position=8, color='cyan', property=Property(name='Vermont Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 30), Structure('house', 50, 90), Structure('house', 50, 270), Structure('house', 50, 400), Structure('hotel', 50, 550)], base_rent=6)),
                      ColorTile(position=9, color='cyan', property=Property(name='Connecticut Avenue', price=100, mortgage_price=50, possible_structures=[Structure('house', 50, 40), Structure('house', 50, 100), Structure('house', 50, 300), Structure('house', 50, 450), Structure('hotel', 50, 600)], base_rent=8)),
                      JailTile(position=10),
                      ColorTile(position=11, color='pink', property=Property(name='St. Charles Place', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      UtilityTile(position=12, property=Property(name='Electric Company', price=150, mortgage_price=75, possible_structures=[], base_rent=None)),
                      ColorTile(position=13, color='pink', property=Property(name='States Avenue', price=140, mortgage_price=70, possible_structures=[Structure('house', 100, 50), Structure('house', 100, 150), Structure('house', 100, 450), Structure('house', 100, 625), Structure('hotel', 100, 750)], base_rent=10)),
                      ColorTile(position=14, color='pink', property=Property(name='Virginia Avenue', price=160, mortgage_price=80, possible_structures=[Structure('house', 100, 60), Structure('house', 100, 180), Structure('house', 100, 500), Structure('house', 100, 700), Structure('hotel', 100, 900)], base_rent=12)),
                      RailRoadTile(position=15, property=Property(name='Pennsylvania Railroad', price=200, mortgage_price=100 , possible_structures=[Structure('trainstation', 100, 50)], base_rent=25)),
                      ColorTile(position=16, color='orange', property=Property(name='St. James Place', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      CardTile(position=17),
                      ColorTile(position=18, color='orange', property=Property(name='Tennessee Avenue', price=180, mortgage_price=90, possible_structures=[Structure('house', 100, 70), Structure('house', 100, 200), Structure('house', 100, 550), Structure('house', 100, 750), Structure('hotel', 100, 950)], base_rent=14)),
                      ColorTile(position=19, color='orange', property=Property(name='New York Avenue', price=200, mortgage_price=100, possible_structures=[Structure('house', 100, 80), Structure('house', 100, 220), Structure('house', 100, 600), Structure('house', 100, 800), Structure('hotel', 100, 1000)], base_rent=16)),
                      FreeParking(position=20),
                      ColorTile(position=21, color='red', property=Property(name='Kentucky Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      CardTile(position=22),
                      ColorTile(position=23, color='red', property=Property(name='Indiana Avenue', price=220, mortgage_price=110, possible_structures=[Structure('house', 150, 90), Structure('house', 150, 250), Structure('house', 150, 700), Structure('house', 150, 875), Structure('hotel', 150, 1050)], base_rent=18)),
                      ColorTile(position=24, color='red', property=Property(name='Illinois Avenue', price=240, mortgage_price=120, possible_structures=[Structure('house', 150, 100), Structure('house', 150, 300), Structure('house', 150, 750), Structure('house', 150, 925), Structure('hotel', 150, 1100)], base_rent=20)),
                      RailRoadTile(position=25, property=Property(name='B. & O. Railroad', price=200, mortgage_price=100 , possible_structures=[Structure('trainstation', 100, 50)], base_rent=25)),
                      ColorTile(position=26, color='yellow', property=Property(name='Atlantic Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      ColorTile(position=27, color='yellow', property=Property(name='Ventnor Avenue', price=260, mortgage_price=130, possible_structures=[Structure('house', 150, 110), Structure('house', 150, 330), Structure('house', 150, 800), Structure('house', 150, 975), Structure('hotel', 150, 1150)], base_rent=22)),
                      UtilityTile(position=28, property=Property(name='Water Works', price=150, mortgage_price=75, possible_structures=[], base_rent=None)),
                      ColorTile(position=29, color='yellow', property=Property(name='Marvin Gardens', price=280, mortgage_price=140, possible_structures=[Structure('house', 150, 120), Structure('house', 150, 360), Structure('house', 150, 850), Structure('house', 150, 1025), Structure('hotel', 150, 1200)], base_rent=24)),
                      GoToJailTile(position=30),
                      ColorTile(position=31, color='green', property=Property(name='Pacific Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 200, 1275)], base_rent=26)),
                      ColorTile(position=32, color='green', property=Property(name='North Carolina Avenue', price=300, mortgage_price=150, possible_structures=[Structure('house', 200, 130), Structure('house', 200, 390), Structure('house', 200, 900), Structure('house', 200, 1100), Structure('hotel', 150, 1275)], base_rent=26)),
                      CardTile(position=33),
                      ColorTile(position=34, color='green', property=Property(name='Pennsylvania Avenue', price=320, mortgage_price=150, possible_structures=[Structure('house', 200, 150), Structure('house', 200, 450), Structure('house', 200, 1000), Structure('house', 200, 1200), Structure('hotel', 200, 1400)], base_rent=28)),
                      RailRoadTile(position=35, property=Property(name='Short Line', price=200, mortgage_price=100 , possible_structures=[Structure('trainstation', 100, 50)], base_rent=25)),
                      CardTile(position=36),
                      ColorTile(position=37, color='blue', property=Property(name='Park Place', price=350, mortgage_price=175, possible_structures=[Structure('house', 200, 175), Structure('house', 200, 500), Structure('house', 200, 1100), Structure('house', 200, 1300), Structure('hotel', 200, 1500)], base_rent=35)),
                      LuxuryTaxTile(position=38),
                      ColorTile(position=39, color='blue', property=Property(name='Boardwalk', price=400, mortgage_price=200, possible_structures=[Structure('house', 200, 200), Structure('house', 200, 600), Structure('house', 200, 1400), Structure('house', 200, 1700), Structure('hotel', 200, 2000)], base_rent=50)),
                      ]

class OwnableItem:

    def find_owner(self, game):
        pass

    def start_direct_sale_process(self, game):
        """Takes an instance of the item and the active_player, makes a series of interface calls to handle the sale of a property.
            -This method returns None
                -This is done because the transaction function in both the Card and OwnableTile classes (sell_card() and sell_property() respectively) requires additional arguments that the execute_player_decision
                    method in the Monopoly class cannot provide.  Therefore, this method is bypassed.
            -If a direct sale cannot be made, then the item will go to auction (Note that the auction method(s) is in the cl_interface module.
            """
        pass

    def start_direct_buy_process(self, game):
        pass

    def find_eligible_buyers(self, game, amount):
        return list(filter(lambda player: player.liquid_holdings >= amount and player != game.active_player, game.players))

    def start_auction_process(self, game, seller):
        """This method is called under three conditions:
            1.  The active player calls it directly
            2.  The amount the active player asked to sell an item for was higher than any other player could afford (i.e. find_eligible_players returned an empty list)
            3.  The buyer chosen by the player did not want to buy the item
            When it's called, all players except the active player have the chance to bid on the item for a set period of time.
            Most of the work for handling an auction is done by the interface module, all this does is call CLInterface.run_auction(item) and parse the returned 2 tuple from
            said method (WinngingPlayer, winning_bid).
            If run_auction() returns None, this method passes.
            """
        pass

    def complete_transaction(self, buyer, seller, amount, game):
        pass

class Option:
    def __init__(self, option_name, item_name, action):
        self.option_name = option_name
        self.item_name = item_name
        self.action = action
        self.item = None


class Card(OwnableItem):
    def __init__(self, name, action, holdable, passes_go, parent_deck=None):
        self.name = name
        self.action = action
        self.holdable = holdable
        self.passes_go = passes_go
        self.parent_deck = parent_deck

    def find_owner(self, game):
        for player in game.players:
            for card in player.hand:
                if card == self:
                    return player

    def start_direct_sale_process(self, game):
        amount = monopoly_cl_interface.CLInterface(game=game).get_amount_to_sell(self)
        eligible_buyers = self.find_eligible_buyers(game=game, amount=amount)
        buyer = monopoly_cl_interface.CLInterface(game=game).pick_eligible_buyer(eligible_buyers)
        if buyer:
            buyer_decision = monopoly_cl_interface.CLInterface(game=game).get_buy_decision(item=self, buyer=buyer, amount=amount)
            if buyer_decision:
                self.complete_transaction(seller=game.active_player, amount=amount, buyer=buyer, game=game)
            else:
                self.start_auction_process(game=game, seller=game.active_player)
        else:
            self.start_auction_process(game=game, seller=game.active_player)

    def start_direct_buy_process(self, game):
        owner = self.find_owner(game=game)
        amount = monopoly_cl_interface.CLInterface(game=game).get_amount_to_buy(item=self, owner=owner)
        seller_decision = monopoly_cl_interface.CLInterface(game=game).get_sell_decision(item=self, proposed_amount=amount, seller=owner)
        if seller_decision:
            self.complete_transaction(buyer=game.active_player, seller=owner, amount=amount, game=game)

    def complete_transaction(self, buyer, seller, amount, game):
        buyer.liquid_holdings -= amount
        if buyer.liquid_holdings < 0:
            buyer.liquid_holdings += amount
            game.run_bankruptcy_process(creditor=seller, debtor=buyer)
            return
        seller.hand.remove(self)
        seller.liquid_holdings += amount
        buyer.hand.append(self)

    def start_auction_process(self, game, seller):
        winning_bid = monopoly_cl_interface.CLInterface(game=game).run_auction(item=self, seller=seller)
        if winning_bid:
            if winning_bid[0].liquid_holdings < winning_bid[1]:
                game.run_bankruptcy_process(debtor=winning_bid[0], creditor=game.active_player)
            else:
                self.complete_transaction(buyer=winning_bid[0], seller=game.active_player, amount=winning_bid[1], game=game)

    def consume_card(self, game):
        self.action(game=game)
        if self.parent_deck == 'Chance Deck':
            game.chance_deck.append(self)
        elif self.parent_deck == 'Community Chest':
            game.community_chest.append(self)
        else:
            raise Exception(f'{self.name} does not have a recognized parent deck.')

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
        else:
            active_player.dealt_card = card
        self.cards.remove(card)

@attr.s
class ChanceDeck(Deck):
    name = attr.ib(default='Chance Deck')
    cards = attr.ib(default=[
            Card(name='Advance to Go', action=advance_to_go, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Advance to Illinois Ave.', action=advance_to_illinois_ave, holdable=False, passes_go=True, parent_deck=name),
            Card(name='Advance to St. Charles Place', action=advance_to_st_charles_place, holdable=False, passes_go=True, parent_deck=name),
            Card(name='Advance token to nearest Utility', action=advance_to_nearest_utility, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Advance token to the nearest Railroad', action=advance_token_to_nearset_railroad, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Bank pays you dividend of $50', action=bank_pays_you_50_dividend, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False, parent_deck=name),
            Card(name='Go back 3 Spaces', action=go_back_3_spaces, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Go to Jail', action=go_to_jail, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Make general repairs on all your property', action=make_general_repairs_on_all_property, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Pay poor tax of $15', action=pay_poor_tax, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Take a trip to Reading Railroad', action=take_trip_to_reading_railroad, holdable=False, passes_go=True, parent_deck=name),
            Card(name='Take a walk on the Boardwalk', action=take_a_walk_on_boardwalk, holdable=False, passes_go=False, parent_deck=name),
            Card(name='You have been elected Chairman of the Board', action=chairman_of_the_board, holdable=False, passes_go=False, parent_deck=name),
            Card(name='Your building loan matures', action=your_building_loan_matures, holdable=False, passes_go=False, parent_deck=name),
            Card(name='You have won a crossword competition', action=you_have_won_a_crossword_competition, holdable=False, passes_go=False, parent_deck=name)])

@attr.s
class CommunityChest(Deck):
    name = attr.ib(default='Community Chest')
    cards = attr.ib(default=[Card(name='Advance to Go', action=advance_to_go, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Bank error in your favor', action=bank_error_in_your_favor, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Doctor\'s fees', action=doctors_fee, holdable=False, passes_go=False, parent_deck=name),
              Card(name='From sale of stock you get $50', action=from_sale_of_stock_50, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False, parent_deck=name),
              Card(name='Go to Jail', action=go_to_jail, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Grand Opera Night', action=grand_opera_night, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Holiday', action=holiday_fund_matures, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Income tax refund', action=income_tax_refund, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Life insurance matures', action=life_insurace_matures, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Pay hospital fees', action=pay_hospital_fees, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Pay school fees', action=pay_school_fees, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Receive $25 consultancy fee', action=receive_25_consultancy_fee, holdable=False, passes_go=False, parent_deck=name),
              Card(name='Your are assessed for street repairs', action=you_are_assessed_for_street_repairs, holdable=False, passes_go=False, parent_deck=name),
              Card(name='You have won second prize in a beauty contest', action=you_have_won_second_prize_in_a_beauty_contest, holdable=False, passes_go=False, parent_deck=name),
              Card(name='You inherit $100', action=you_inherit_100, holdable=False, passes_go=False, parent_deck=name)])


class Bank:
    def __init__(self, game):
        self.name = 'the Bank'
        self.game = game
        self.property_holdings = []
        self.liquid_holdings = 0
        self.hand = []

class Player:

    def __init__(self, name, game):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        #Contains a list of Tile objects the player currently owns properties on
        self.consecutive_turns = 0
        self.property_holdings = []
        self.jailed_turns = 0
        self.jailed = False
        self.hand = []
        self.game = game
        self.dealt_card = None

    def player_actions(self):
        return self.generate_card_options()

    def find_gross_worth(self):
        gross_worth = self.liquid_holdings
        for tile in self.property_holdings:
            if tile.property.mortgaged:
                gross_worth += tile.property.mortgage_price
            else:
                gross_worth += tile.property.price
            if len(tile.property.existing_structures) > 0:
                for structure in tile.property.existing_structures:
                  gross_worth += structure.price/2
        return gross_worth

    def advance_position(self, amount):
        if self.position + amount < 0:
            self.position += 40
        self.position = (self.position + amount) % 40

    def go_directly_to_jail(self):
        self.position = 10
        self.jailed = True

    def pay_jail_fine(self):
        self.liquid_holdings -= 50
        if self.liquid_holdings < 0:
            self.game.run_bankruptcy_process(debtor=self, creditor=self.game.bank)
        else:
            self.jailed = False
            self.position += sum(self.game.roll_dice())

    #TODO Move this method to the ColorTile class.
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

    def generate_card_options(self):
        card_options = []
        for card in self.hand:
            card_options.append(Option(item_name=card.name, action=card.action, option_name=f'Use {card.name}'))
            card_options.append(Option(item_name=card.name, action=card.start_direct_sale_process, option_name=f'Sell {card.name}'))
        return card_options + self.list_cards_of_other_players()

    def list_cards_of_other_players(self):
        return [Option(option_name=f'Buy {card.name}', item_name=card.name, action=card.start_direct_buy_process(game=self.game)) for card in list(filter(lambda player: player != self.game.active_player and len(player.hand) > 0, self.game.players))]

    def pass_go(self):
        self.liquid_holdings += 200

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

class Structure:
    def __init__(self, type, price, rent):
        self.type = type
        self.price = price
        self.rent = rent

#tile_action(self) --- Performs the relevant actions for a tile when called.

@attr.s
class Tile:
    position = attr.ib(type=int)

    def tile_actions(self, game):
        """Performs all appropriate actions associated with the Tile object in play
            Assumes active_player is on the Tile"""
        pass


#Should be able to tell if the property on the Tile is on the market, how many like tiles the Owner of the landed on tile has, determine if the Tile can be sold (I think this may be unique to color tiles)
@attr.s
class OwnableTile(Tile, OwnableItem):
    property: Property = attr.ib()

    #Find owner of tile occupied by the active_player, if no owner, return None
    def find_owner(self, players):
        for player in players:
            for property in player.property_holdings:
                if property == self:
                    return player
        return None

    def if_owned(self, owner, game):
        pass

    def if_not_owned(self, active_player):
        buy_mortgage_option_list = []
        if self.property.price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(Option(option_name=f'Buy {self.property.name} at position: {self.position}', action=self.buy_property, item_name=self.property.name))
        if self.property.mortgage_price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(Option(option_name=f'Mortgage {self.property.name} at position: {self.position}', action=self.mortgage_property, item_name=self.property.name))
        return buy_mortgage_option_list

    def buy_property(self, game):
        game.active_player.liquid_holdings -= self.property.price
        game.active_player.property_holdings.append(self)

    def mortgage_property(self, game):
        game.active_player.liquid_holdings -= self.property.mortgage_price
        game.active_player.property_holdings.append(self)
        self.property.mortgaged = True

    def mortgage_owned_property(self, game):
        game.active_player.liquid_holdings += self.property.mortgage_price
        self.property.mortgaged = True

    def lift_mortgage(self, game):
        game.active_player.liquid_holdings -= 0.1*self.property.mortgage_price
        self.property.mortgaged = False

    #Below method finds out how many similar properties an owner has
    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if type(self) == type(tile):
                num_tiles += 1
        return num_tiles

    def determine_if_sellable(self, owner):
        """
        :param Player owner:  Player object who owns the tile
        :return: Returns either an empty list or a list containing an Option object which will start the direct sale process if chosen by the player
        """
        if self in owner.property_holdings:
            if len(self.property.existing_structures) > 0:
                return []
            else:
                return [Option(option_name=f'Sell {self.property.name}', action=self.start_direct_sale_process, item_name=self.property.name),
                        Option(option_name=f'Sell {self.property.name} to the Bank for {0.5 * self.property.price}', action=self.sell_to_bank, item_name=self.property.name)]
        else:
            return []

    def sell_to_bank(self, game):
        game.active_player.liquid_holdings += self.property.price * 0.5
        game.active_player.property_holdings.remove(self)

    def start_direct_sale_process(self, game):
        amount = monopoly_cl_interface.CLInterface(game=game).get_amount_to_sell(item=self.property)
        eligible_buyers = self.find_eligible_buyers(game=game, amount=amount)
        buyer = monopoly_cl_interface.CLInterface(game=game).pick_eligible_buyer(eligible_buyers)
        if buyer:
            buyer_decision = monopoly_cl_interface.CLInterface(game=game).get_buy_decision(item=self.property, amount=amount, buyer=buyer)
            if buyer_decision:
                self.complete_transaction(buyer=buyer, seller=game.active_player, amount=amount, game=game)
            else:
                self.start_auction_process(game=game, seller=game.active_player)
        else:
            self.start_auction_process(game=game, seller=game.active_player)

    def start_direct_buy_process(self, game):
        owner = self.find_owner(game.players)
        amount = monopoly_cl_interface.CLInterface(game=game).get_amount_to_buy(owner=owner, item=self.property)
        seller_decision = monopoly_cl_interface.CLInterface(game=game).get_sell_decision(item=self.property, seller=owner, proposed_amount=amount)
        if seller_decision:
            self.complete_transaction(buyer=game.active_player, seller=owner, amount=amount, game=game)

    def find_properties_of_other_players(self, game):
        property_tuples = [(list(filter(lambda tile: tile.determine_if_sellable(owner=player), player.property_holdings)), player) for player in list(filter(lambda player: player != game.active_player, game.players))]
        option_list = []
        for n_tuple in property_tuples:
            for tile in n_tuple[0]:
                if self.property.mortgaged:
                    option_list.append(Option(option_name=f'''Request to buy {tile.property.name} from {n_tuple[1].name} --- (Property deed price is {tile.property.price}) --- WARNING: Property IS Mortgaged''', action=self.start_direct_buy_process, item_name=f'{self.property.name}'))
                else:
                    option_list.append(Option(option_name=f'''Request to buy {tile.property.name} from {n_tuple[1].name} --- (Property deed price is {tile.property.price}) --- Property IS NOT Mortgaged''', action=self.start_direct_buy_process, item_name=f'{self.property.name}'))
        return option_list

    def start_auction_process(self, game, seller):
        winning_bid = monopoly_cl_interface.CLInterface(game=game).run_auction(item=self.property, seller=seller)
        if winning_bid:
            if winning_bid[0].liquid_holdings < winning_bid[1]:
                game.run_bankruptcy_process(debtor=winning_bid[0], creditor=game.active_player)
            self.complete_transaction(buyer=winning_bid[0], seller=game.active_player, amount=winning_bid[1], game=game)

    def complete_transaction(self, buyer, seller, amount, game):
        if self.property.mortgaged:
            """This seems to be a grey area in the rules.  Normally, amount is just the deed price of the property, however the rules do not specify what happens if
            a mortgaged property is auctioned.  Or if, for that matter, if a mortgaged property can be auctioned.  I'm designing to the spec that a mortgaged property
            can be auctioned and the extra 10% assessed is based off the mortgage price."""
            if amount + 1.1 * self.property.mortgage_price <= buyer.liquid_holdings:
                immediate_unmortgage_decision = monopoly_cl_interface.CLInterface(game=game).get_buy_and_lift_mortgage_decision(buyer=buyer, seller=seller, amount=amount, item=self.property)
                if immediate_unmortgage_decision:
                    self.property.mortgaged = False
                    buyer.liquid_holdings -= 1.1 * self.property.mortgage_price
            buyer.liquid_holdings -= amount + 0.1*self.property.mortgage_price
            if buyer.liquid_holdings < 0:
                game.run_bankruptcy_process(debtor=buyer, creditor=seller)
                return
        else:
            buyer.liquid_holdings -= amount
        seller.property_holdings.remove(self)
        buyer.property_holdings.append(self)
        seller.liquid_holdings += amount

    def remove_structure(self, game):
        pass

@attr.s
class UnownableTile(Tile):
    pass

#tile_actions() needs to determine the Tile's state, perform automatic actions on the active_player as a function of that state, and return a list of options the player can choose from
@attr.s
class RailRoadTile(OwnableTile):

    def tile_actions(self, game):
        owner = self.find_owner(game.players)
        other_owned_properties = self.find_properties_of_other_players(game=game)
        if owner:
            if owner == game.active_player:
                return self.if_owned(owner=owner, game=game)
            else:
                return self.if_owned(owner=owner, game=game) + other_owned_properties
        else:
            return self.if_not_owned(game.active_player) + other_owned_properties

    def if_owned(self, owner, game):
        """
        :param active_player:
        :param owner:
        :param Monopoly game:
        :param dice_roll:
        :return:
        """
        if game.active_player == owner:
            sellability = self.determine_if_sellable(owner=owner)
            if sellability:
                if self.property.mortgaged:
                    if game.active_player.liquid_holdings >= self.property.price * 0.1:
                        return sellability + [Option(option_name=f'Lift Mortgage on {self.property.name}', action=self.lift_mortgage, item_name=self.property.name)]
                    else:
                        return sellability + [Option(option_name=f'Mortgage {self.propert.name}', action=self.mortgage_owned_property, item_name=self.property.name)]
                elif game.active_player.liquid_holdings >= self.property.possible_structures[0].price:
                    return sellability + [Option(option_name=f'Build Transtation at {self.property.name}', action=self.build_train_station, item_name=self.property.name)]
                else:
                    return sellability
            else:
                return [Option(option_name=f'Sell Trainstation at {self.property.name} to the Bank for {0.5*self.property.existing_structures[0].price}', action=self.remove_structure, item_name=self.property.existing_structures[0].type)]
        elif self.property.mortgaged:
            return []
        else:
            self.assess_rent(owner=owner, game=game)
            return []

    def assess_rent(self, owner, game):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        multiplier = 1
        if game.active_player.dealt_card:
            multiplier = 2
        if len(self.property.existing_structures) == 1 and self.property.existing_structures[0].type == 'transtation':
            rent = multiplier * self.property.base_rent * 4**(num_owned_railroads - 1)
        else:
            rent = multiplier * self.property.base_rent * 2**(num_owned_railroads - 1)
        if rent > game.active_player.liquid_holdings:
            game.run_bankruptcy_process(debtor=game.active_player, creditor=owner)
        else:
            owner.liquid_holdings += rent
            game.active_player.liquid_holdings -= rent
            
    def build_train_station(self, game):
        if game.active_player.liquid_holdings >= self.property.possible_structures[0].price:
            game.active_player.liquid_holdings -= self.property.possible_structures[0].price
            self.property.existing_structures.append(self.property.possible_structures[0])

    def remove_structure(self, game):
        self.property.existing_structures = []
        game.active_player.liquid_holdings += self.property.possible_structures[0].price

@attr.s
class JailTile(UnownableTile):

    def tile_actions(self, game):
        """
        :param Monopoly game: Reference to the instance of Monopoly
        :return list option_list: List containing either zero or one Option objects
        JailTile is an interesting class, in that much of the behavior that relates to it is carried out in the Player class
        or Monopoly class.  The tile_actions method for JailTile performs a dice_roll on the player, if the player lands doubles,
        they are freed from jail.  If they do not, then it checks to see if their liquid_holdings are greater than $50.  It also checks
        to see if the active_player has a Get Out of Jail Free card.  It then returns a list containing the applicable Option objects.
        If the active_player has been in jail for three turns, tile_actions() calls active_player.pay_jail_fine() method and returns an empty list.
        """
        option_list = []
        dice_roll = game.roll_dice()
        if game.active_player.jailed_turns < 3:
            if dice_roll[0] == dice_roll[1]:
                game.active_player.advance_position(amount=sum(dice_roll))
                return game.board[game.active_player.position].tile_actions(game=game)
            if game.active_player.liquid_holdings >= 50:
                option_list.append(Option(option_name='Pay Jail Fine ($50)', item_name=None, action=game.active_player.pay_jail_fine))
            for card in game.active_player.hand:
                if card.name == 'Get out of Jail Free':
                    option_list.append(Option(option_name=f'Use {card.name} card from {card.parent_deck}', action=card.action, item_name=card.name))
        else:
            game.active_player.pay_jail_fine()
        return option_list

@attr.s
class CardTile(UnownableTile):

    def tile_actions(self, game):
        return []

    def consume_card(self, game, dealt_card):
        return None

@attr.s
class ChanceTile(CardTile):
    pass

@attr.s
class CommunityChestTile(CardTile):
    pass

    # def draw_card(player, deck):
    #     card = deck[-1]
    #     card.action(player)

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
class GoTile(UnownableTile):

    @staticmethod
    def give_funds(player):
        player.liquid_holdings += 200


























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














        