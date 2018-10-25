import monopoly_cl_interface
import random
from functools import reduce
import cards
import board

class Monopoly:

    def __init__(self):
        self.players = []
        self.board = board.Board().board
        self.chance_deck = cards.ChanceDeck()
        self.community_deck = cards.CommunityChest()
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
        self.dice_roll = self.roll_dice()
        self.check_for_doubles()
        if self.active_player.jailed:
            pass
        else:
            self.active_player.advance_position(amount=self.dice_roll[0] + self.dice_roll[1])
        print(f'\n{self.active_player.liquid_holdings}: --- {self.turns} --- {self.active_player.name} --- Pos: {self.active_player.position} ---{[x.property.name for x in self.active_player.property_holdings]}')
        option_list = []
        tile_options = self.board[self.active_player.position].tile_actions(game=self)
        tile_options += self.board[self.active_player.position].find_properties_of_other_players(game=self)
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

    def compute_advancement_amount(self, target_position):
        if target_position < self.position:
            amount = 40 - self.position + target_position
        else:
            amount = target_position - self.position
        return amount

    def advance_position(self, amount):
        if self.position + amount < 0:
            self.position += 40
            if not self.jailed:
                self.pass_go()
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

    def generate_card_options(self):
        card_options = []
        for card in self.hand:
            card_options.append(Option(item_name=card.name, action=card.start_direct_sale_process, option_name=f'Sell {card.name}'))
        return card_options + self.list_cards_of_other_players()

    def list_cards_of_other_players(self):
        return [Option(option_name=f'Buy {card.name} from {card.find_owner(game=self.game).name}', item_name=card.name, action=card.start_direct_buy_process) for card in reduce(lambda card, next_card: card + next_card, [player.hand for player in list(filter(lambda player: player != self.game.active_player and len(player.hand) > 0, self.game.players))], [])]

    def pass_go(self):
        self.liquid_holdings += 200
















        