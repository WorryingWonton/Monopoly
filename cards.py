import attr
import random
import ownable_item
from chance_deck_functions import *
from community_chest_functions import *

class Card(ownable_item.OwnableItem):
    def __init__(self, name, action, holdable, passes_go, parent_deck):
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
        amount = game.interface.get_amount_to_sell(self)
        eligible_buyers = self.find_eligible_buyers(game=game, amount=amount)
        buyer = game.interface.pick_eligible_buyer(eligible_buyers)
        if buyer:
            buyer_decision = game.interface.get_buy_decision(item=self, buyer=buyer, amount=amount)
            if buyer_decision:
                self.complete_transaction(seller=game.active_player, amount=amount, buyer=buyer, game=game)
            else:
                self.start_auction_process(game=game, seller=game.active_player)
        else:
            self.start_auction_process(game=game, seller=game.active_player)

    def start_direct_buy_process(self, game):
        owner = self.find_owner(game=game)
        amount = game.interface.get_amount_to_buy(item=self, owner=owner)
        seller_decision = game.interface.get_sell_decision(item=self, proposed_amount=amount, seller=owner)
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
        winning_bid = game.interface.run_auction(item=self, seller=seller)
        if winning_bid:
            if winning_bid[0].liquid_holdings < winning_bid[1]:
                game.run_bankruptcy_process(debtor=winning_bid[0], creditor=game.active_player)
            else:
                self.complete_transaction(buyer=winning_bid[0], seller=game.active_player, amount=winning_bid[1], game=game)

    def consume_card(self, game):
        self.action(game=game)
        if self.parent_deck == 'Chance Deck':
            game.chance_deck.append(self)
        if self.parent_deck == 'Community Chest':
            game.community_chest.append(self)


@attr.s
class Deck:
    cards = attr.ib(factory=list)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    #Cards are read from the top of each deck, and re-inserted at the bottom their action is performed
    def deal_from_deck(self, game):
        card = self.cards[0]
        if card.holdable:
            game.active_player.hand.append(card)
        else:
            game.active_player.dealt_card = card
        self.cards.remove(card)

@attr.s
class ChanceDeck(Deck):
    deck_name = attr.ib(default='Chance Deck')
    cards = attr.ib(default=[
        Card(name='Advance to Go', action=advance_to_go, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Advance to Illinois Ave.', action=advance_to_illinois_ave, holdable=False, passes_go=True, parent_deck=deck_name),
        Card(name='Advance to St. Charles Place', action=advance_to_st_charles_place, holdable=False, passes_go=True, parent_deck=deck_name),
        Card(name='Advance token to nearest Utility', action=advance_to_nearest_utility, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Advance token to the nearest Railroad', action=advance_token_to_nearset_railroad, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Bank pays you dividend of $50', action=bank_pays_you_50_dividend, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False, parent_deck=deck_name),
        Card(name='Go back 3 Spaces', action=go_back_3_spaces, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Go to Jail', action=go_to_jail, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Make general repairs on all your property', action=make_general_repairs_on_all_property, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Pay poor tax of $15', action=pay_poor_tax, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Take a trip to Reading Railroad', action=take_trip_to_reading_railroad, holdable=False, passes_go=True, parent_deck=deck_name),
        Card(name='Take a walk on the Boardwalk', action=take_a_walk_on_boardwalk, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='You have been elected Chairman of the Board', action=chairman_of_the_board, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Your building loan matures', action=your_building_loan_matures, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='You have won a crossword competition', action=you_have_won_a_crossword_competition, holdable=False, passes_go=False, parent_deck=deck_name)])

@attr.s
class CommunityChest(Deck):
    deck_name = attr.ib(default='Community Chest')
    cards = attr.ib(default=[
        Card(name='Advance to Go', action=advance_to_go, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Bank error in your favor', action=bank_error_in_your_favor, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Doctor\'s fees', action=doctors_fee, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='From sale of stock you get $50', action=from_sale_of_stock_50, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False, parent_deck=deck_name),
        Card(name='Go to Jail', action=go_to_jail, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Grand Opera Night', action=grand_opera_night, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Holiday', action=holiday_fund_matures, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Income tax refund', action=income_tax_refund, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Life insurance matures', action=life_insurace_matures, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Pay hospital fees', action=pay_hospital_fees, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Pay school fees', action=pay_school_fees, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Receive $25 consultancy fee', action=receive_25_consultancy_fee, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='Your are assessed for street repairs', action=you_are_assessed_for_street_repairs, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='You have won second prize in a beauty contest', action=you_have_won_second_prize_in_a_beauty_contest, holdable=False, passes_go=False, parent_deck=deck_name),
        Card(name='You inherit $100', action=you_inherit_100, holdable=False, passes_go=False, parent_deck=deck_name)])