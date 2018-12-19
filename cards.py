import random
from chance_deck_functions import *
from community_chest_functions import *
import attr
from ownable_item import OwnableItem

class Card:

    def __init__(self, name, action, parent_deck):
        self.name = name
        self.action = action
        self.parent_deck = parent_deck

    def consume_card(self, game):
        if self.parent_deck == 'Chance Deck':
            game.chance_deck.append(self)
        if self.parent_deck == 'Community Chest':
            game.community_chest.append(self)
        self.action(game=game)
        game.active_player.dealt_card = None

class HoldableCard(Card, OwnableItem):

    def complete_transaction(self, buyer, seller, amount, game):
        buyer.liquid_holdings -= amount
        if buyer.liquid_holdings < 0:
            buyer.liquid_holdings += amount
            game.run_bankruptcy_process(creditor=seller, debtor=buyer)
            return
        if self in seller.hand:
            seller.hand.remove(self)
        seller.liquid_holdings += amount
        buyer.hand.append(self)

@attr.s
class Deck:
    cards = attr.ib(factory=list)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    #Cards are read from the top of each deck, and re-inserted at the bottom once their action is performed
    def deal_from_deck(self, game):
        card = self.cards[0]
        if isinstance(card, HoldableCard):
            game.active_player.hand.append(card)
        else:
            game.active_player.dealt_card = card
        self.cards.remove(card)

@attr.s
class ChanceDeck(Deck):
    deck_name = attr.ib(default='Chance Deck')
    cards = attr.ib(default=[
        Card(name='Advance to Go', action=advance_to_go, parent_deck=deck_name),
        Card(name='Advance to Illinois Ave.', action=advance_to_illinois_ave, parent_deck=deck_name),
        Card(name='Advance to St. Charles Place', action=advance_to_st_charles_place, parent_deck=deck_name),
        Card(name='Advance token to nearest Utility', action=advance_to_nearest_utility, parent_deck=deck_name),
        Card(name='Advance token to the nearest Railroad', action=advance_token_to_nearset_railroad, parent_deck=deck_name),
        Card(name='Bank pays you dividend of $50', action=bank_pays_you_50_dividend, parent_deck=deck_name),
        HoldableCard(name='Get out of Jail Free', action=get_out_jail_free, parent_deck=deck_name),
        Card(name='Go back 3 Spaces', action=go_back_3_spaces, parent_deck=deck_name),
        Card(name='Go to Jail', action=go_to_jail, parent_deck=deck_name),
        Card(name='Make general repairs on all your property', action=make_general_repairs_on_all_property, parent_deck=deck_name),
        Card(name='Pay poor tax of $15', action=pay_poor_tax, parent_deck=deck_name),
        Card(name='Take a trip to Reading Railroad', action=take_trip_to_reading_railroad, parent_deck=deck_name),
        Card(name='Take a walk on the Boardwalk', action=take_a_walk_on_boardwalk, parent_deck=deck_name),
        Card(name='You have been elected Chairman of the Board', action=chairman_of_the_board, parent_deck=deck_name),
        Card(name='Your building loan matures', action=your_building_loan_matures, parent_deck=deck_name),
        Card(name='You have won a crossword competition', action=you_have_won_a_crossword_competition, parent_deck=deck_name)])

@attr.s
class CommunityChest(Deck):
    deck_name = attr.ib(default='Community Chest')
    cards = attr.ib(default=[
        Card(name='Advance to Go', action=advance_to_go, parent_deck=deck_name),
        Card(name='Bank error in your favor', action=bank_error_in_your_favor, parent_deck=deck_name),
        Card(name='Doctor\'s fees', action=doctors_fee, parent_deck=deck_name),
        Card(name='From sale of stock you get $50', action=from_sale_of_stock_50, parent_deck=deck_name),
        HoldableCard(name='Get out of Jail Free', action=get_out_jail_free, parent_deck=deck_name),
        Card(name='Go to Jail', action=go_to_jail, parent_deck=deck_name),
        Card(name='Grand Opera Night', action=grand_opera_night, parent_deck=deck_name),
        Card(name='Holiday', action=holiday_fund_matures, parent_deck=deck_name),
        Card(name='Income tax refund', action=income_tax_refund, parent_deck=deck_name),
        Card(name='Life insurance matures', action=life_insurace_matures, parent_deck=deck_name),
        Card(name='Pay hospital fees', action=pay_hospital_fees, parent_deck=deck_name),
        Card(name='Pay school fees', action=pay_school_fees, parent_deck=deck_name),
        Card(name='Receive $25 consultancy fee', action=receive_25_consultancy_fee, parent_deck=deck_name),
        Card(name='Your are assessed for street repairs', action=you_are_assessed_for_street_repairs, parent_deck=deck_name),
        Card(name='You have won second prize in a beauty contest', action=you_have_won_second_prize_in_a_beauty_contest, parent_deck=deck_name),
        Card(name='You inherit $100', action=you_inherit_100, parent_deck=deck_name)])