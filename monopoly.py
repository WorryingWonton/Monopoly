import monopoly_cl_interface
from auction import Auction
import random
from functools import reduce
import cards
import board
from itertools import cycle, islice, dropwhile
from tiles import OwnableTile
from cards import HoldableCard
"""
TODO (To bring Monopoly fully inline with the rules as defined by https://www.hasbro.com/common/instruct/monins.pdf)
    -Reimplement the interface to support Option categories [On hold]
        -After completing this, remove the option_name attribute from all Option objects [In Progress]
    -Add support for limited structures, the rules state there should be a set number of houses and hotels. [In progress]
        -Doing this involves making Structures into OwnableItems, and implemting the complete_transaction() method for a Structure
            -See docstring over in tiles.py in the Structure class for more details
    -Fix issues with auction behavior: [In Progress]
        -An auction can be called where the seller of an item is a participant
        -In a 2 player game, an Auction should NOT be called if a Player fails to sell an item to their opposite.
        -Some executive methods called in an auction (sell_to_bank, remove_structure, and mortgage_owned_property) only work on the Active Player:
            -These should work on the owner of the item.
    -Add feature to charge double rent if a Player owns all tiles in a particular color group. [On hold]
    -Add support for non active Players to perform the following actions: [On hold, potential major refactor]
        -Selling OwnableItems to other Players and the Bank.
        -Removing Structures from their properties
        -Requesting to buy OwnableItems from other Players        
"""

class Monopoly:

    def __init__(self, interface=None):
        self.players = []
        self.all_players = []
        self.board = board.Board().board
        self.chance_deck = cards.ChanceDeck()
        self.community_deck = cards.CommunityChest()
        self.active_player = None
        self.turns = 0
        self.bank = Bank(game=self)
        self.dice_roll = None
        self.continue_current_turn = True
        if not interface:
            self.interface = monopoly_cl_interface.CLInterface(game=self)
        else:
            self.interface = interface


    def add_player(self, name):
        self.all_players.append(Player(name, game=self))

    def remove_player(self, player):
        player.in_game = False

    def generate_in_game_players(self):
        self.players = [player for player in self.all_players if player.in_game]

    def set_active_player(self):
        if not self.active_player:
            self.active_player = self.all_players[0]
        else:
            self.active_player = next(dropwhile(lambda p: not p.in_game, islice(dropwhile(lambda p: p != self.active_player, cycle(self.players)), 1, None)))
        self.generate_in_game_players()

    def roll_dice(self):
        return (random.randint(1, 6), random.randint(1, 6))

    def run_turn(self):
        self.dice_roll = self.roll_dice()
        if not self.active_player.jailed:
            self.active_player.advance_position(amount=sum(self.dice_roll))
        self.board[self.active_player.position].perform_auto_actions(game=self)
        if not self.continue_current_turn:
            self.continue_current_turn = True
            return self.check_for_doubles()
        while True:
            if not self.active_player.in_game:
                break
            option_list = self.active_player.list_options_in_categories()
            option_list += self.board[self.active_player.position].find_properties_of_other_players(game=self)
            option_list += self.active_player.player_actions()
            if option_list:
                active_player_decision = self.interface.get_decision(option_list)
                if not active_player_decision:
                    auction_options = [option for option in option_list if option.category == 'auctionproperty']
                    if auction_options:
                        self.execute_player_decision(active_player_decision=auction_options[0])
                    break
                self.execute_player_decision(active_player_decision)
                if not self.continue_current_turn:
                    self.continue_current_turn = True
                    break
            else:
                break
        return self.check_for_doubles()

    def execute_player_decision(self, active_player_decision):
        active_player_decision.action(self)

    def run_game(self):
        doubles = False
        self.generate_in_game_players()
        self.chance_deck.shuffle_deck()
        self.community_deck.shuffle_deck()
        self.bank.property_holdings += self.board
        while len(self.players) > 1:
            if self.turns % len(self.chance_deck.cards) == 0:
                self.chance_deck.shuffle_deck()
                self.community_deck.shuffle_deck()
            if doubles:
                self.active_player.consecutive_turns += 1
                if self.active_player.consecutive_turns == 3:
                    self.active_player.consecutive_turns = 0
                    self.active_player.go_directly_to_jail()
                    self.set_active_player()
            else:
                self.set_active_player()
                self.active_player.consecutive_turns = 0
            self.advance_turn()
            doubles = self.run_turn()
        return self.players[0]

    def advance_turn(self):
        self.turns += 1

    def run_bankruptcy_process(self, creditor, debtor):
        if debtor.liquid_holdings >= 0:
            creditor.liquid_holdings += debtor.liquid_holdings
        for tile in debtor.property_holdings:
            if tile.mortgaged:
                creditor.liquid_holdingsq -= 0.1 * tile.mortgage_price
            for structure in tile.existing_structures:
                creditor.liquid_holdings += 0.5 * structure.price
            if creditor == self.bank:
                self.bank.reserved_holdings.append(tile)
                self.bank.structure_repository += tile.existing_structures
            else:
                creditor.property_holdings.append(tile)
            tile.existing_structures = []
        creditor.hand = debtor.hand
        self.remove_player(debtor)
        self.generate_in_game_players()
        if len(self.players) == 1:
            return
        if creditor == self.bank:
            self.run_bank_auction()

    def run_bank_auction(self):
        for item in self.bank.reserved_holdings:
            winning_bid = Auction(game=self, item=item, seller=self.bank).auction_item()
            if winning_bid and winning_bid[0]:
                    item.complete_transaction(buyer=winning_bid[0], seller=self.bank, amount=winning_bid[1], game=self)
        for item in self.bank.reserved_holdings:
            if isinstance(item, OwnableTile):
                self.bank.property_holdings.append(item)
            if isinstance(item, HoldableCard):
                if item.parent_deck == 'Community Chest':
                    self.community_deck.append(item)
                else:
                    self.chance_deck.append(item)
        self.bank.reserved_holdings = []

    def check_for_doubles(self):
        return self.dice_roll[0] == self.dice_roll[1]

    def end_current_turn(self):
        self.continue_current_turn = False


class Option:
    def __init__(self, option_name, item_name, action, category, ends_turn=False):
        self.option_name = option_name
        self.item_name = item_name
        self.action = action
        """
        Categories are:
            'payjailfine'
                -Needs to know amount is $50
                -i18n.en_US.pay_jail_fine = "pay DOLLAR to get out of jail"
                -Message = i18n[language][category].replace("DOLLAR", amount)
            'mortgageunownedproperty'
            'mortgageownedproperty'
            'buyownedproperty'
            'buymortgagedproperty'
            'buyunownedproperty'
            'auctionproperty'
            'selltobank'
            'selltoplayer'
            'buycardfromplayer'
            'buildstructure'
            'removestructure'
			'liftmortgage'
			'buyandliftmortgage'
			'useheldcard'
        """
        self.category = category
        self.ends_turn = ends_turn


class Bank:
    def __init__(self, game):
        self.name = 'the Bank'
        self.game = game
        self.property_holdings = []
        self.liquid_holdings = 0
        self.hand = []
        #Can be populated with OwnableTile and HoldableCard objects
        self.reserved_holdings = []
        self.structure_repository = []

class Player:

    def __init__(self, name, game):
        self.name = name
        self.position = 0
        self.liquid_holdings = 1500
        self.consecutive_turns = 0
        self.property_holdings = []
        self.jailed_turns = 0
        self.jailed = False
        self.hand = []
        self.game = game
        self.dealt_card = None
        self.in_game = True
        self.in_auction = True

    def player_actions(self):
        return self.generate_card_options()

    def calculate_taxable_assets(self):
        assets = self.liquid_holdings
        for tile in self.property_holdings:
            if tile.mortgaged:
                assets += tile.mortgage_price
            else:
                assets += tile.price
            if len(tile.existing_structures) > 0:
                for structure in tile.existing_structures:
                  assets += structure.price/2
        return assets

    def find_gross_worth(self):
        gross_worth = self.liquid_holdings
        for tile in self.property_holdings:
            options = tile.list_options(game=self.game)
            for option in options:
                if option.category in ['selltobank', 'mortgageownedproperty']:
                    gross_worth += tile.price/2
                    break
                elif option.category == 'removestructure':
                    gross_worth += tile.existing_structures[-1].price
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
            return
        if self.position + amount > 40 and not self.jailed:
            self.pass_go()
        self.position = (self.position + amount) % 40

    def go_directly_to_jail(self):
        self.position = 10
        self.jailed = True

    def generate_card_options(self):
        card_options = []
        for card in self.hand:
            card_options.append(Option(item_name=card.name, action=card.start_direct_sale_process, option_name=f'Sell {card.name}', category='selltoplayer'))
        return card_options + self.list_cards_of_other_players()

    def list_cards_of_other_players(self):
        return [Option(option_name=f'Buy {card.name} from {card.find_owner(game=self.game).name}', item_name=card.name, action=card.start_direct_buy_process, category='buycardfromplayer') for card in reduce(lambda card, next_card: card + next_card, [player.hand for player in list(filter(lambda player: player != self.game.active_player and len(player.hand) > 0, self.game.players))], [])]

    def pass_go(self):
        self.liquid_holdings += 200

    def list_options_in_categories(self, categories=None):
        option_list = []
        if categories:
            option_list += [option for option in self.game.board[self.position].list_options(game=self.game) if option.category in categories]
            for tile in [tile for tile in self.property_holdings if tile.position != self.position]:
                option_list += [option for option in tile.list_options(game=self.game) if option.category in categories]
        else:
            option_list += self.game.board[self.position].list_options(game=self.game)
            for tile in [tile for tile in self.property_holdings if tile.position != self.position]:
                option_list += tile.list_options(game=self.game)
        return option_list

if __name__ == '__main__':
    game_instance = Monopoly()
    game_instance.interface.add_players()
    game_instance.run_game()
