import monopoly_cl_interface
import random
from functools import reduce
import cards
import board

class Monopoly:

    def __init__(self, interface=None):
        self.players = []
        self.board = board.Board().board
        self.chance_deck = cards.ChanceDeck()
        self.community_deck = cards.CommunityChest()
        self.active_player = None
        self.generator = self.next_player_generator()
        self.turns = 0
        self.bank = Bank(game=self)
        self.dice_roll = None
        if not interface:
            self.interface = monopoly_cl_interface.CLInterface(game=self)
        else:
            self.interface = interface

    def add_player(self, name):
        self.players.append(Player(name, game=self))

    def next_player_generator(self):
        while True:
            for i in range(len(self.players)):
                if i in range(len(self.players)):
                    player = self.players[i]
                else:
                    break
                yield player

    def roll_dice(self):
        return (random.randint(1, 6), random.randint(1, 6))

    def run_turn(self):
        self.dice_roll = self.roll_dice()
        if self.active_player.jailed:
            pass
        else:
            self.active_player.advance_position(amount=self.dice_roll[0] + self.dice_roll[1])
        print(f'\n{self.active_player.liquid_holdings}: --- {self.turns} --- {self.active_player.name} --- Pos: {self.active_player.position} ({self.board[self.active_player.position]}) --- {self.dice_roll} ---{[x.property.name for x in self.active_player.property_holdings]}')
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
        return self.check_for_doubles()

    def execute_player_decision(self, active_player_decision):
        if active_player_decision:
            active_player_decision.action(self)

    def run_game(self):
        doubles = False
        while len(self.players) > 1:
            if doubles:
                self.active_player.consecutive_turns += 1
                if self.active_player.consecutive_turns == 3:
                    self.active_player.consecutive_turns = 0
                    self.active_player.go_directly_to_jail()
                    self.active_player = next(self.generator)
                    doubles = False
                    continue
            else:
                self.active_player = next(self.generator)
                self.active_player.consecutive_turns = 0
            self.advance_turn()
            doubles = self.run_turn()
        return self.players[0]

    def advance_turn(self):
        self.turns += 1

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
        return self.dice_roll[0] == self.dice_roll[1]

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

    def generate_card_options(self):
        card_options = []
        for card in self.hand:
            card_options.append(Option(item_name=card.name, action=card.start_direct_sale_process, option_name=f'Sell {card.name}'))
        return card_options + self.list_cards_of_other_players()

    def list_cards_of_other_players(self):
        return [Option(option_name=f'Buy {card.name} from {card.find_owner(game=self.game).name}', item_name=card.name, action=card.start_direct_buy_process) for card in reduce(lambda card, next_card: card + next_card, [player.hand for player in list(filter(lambda player: player != self.game.active_player and len(player.hand) > 0, self.game.players))], [])]

    def pass_go(self):
        self.liquid_holdings += 200

if __name__ == '__main__':
    game_instance = Monopoly()
    game_instance.interface.add_players()
    game_instance.run_game()