import unittest
from monopoly import *

class TestMonopolyInitialization(unittest.TestCase):
    def test_game_initialization(self):
        game_instance = Monopoly()
        self.assertEqual(40, len(game_instance.board))
        self.assertEqual(0, len(game_instance.players))
        self.assertEqual(16, len(game_instance.chance_deck.cards))
        self.assertEqual(16, len(game_instance.community_deck.cards))
        self.assertEqual(0, game_instance.turns)

class TestPlayerInitialization(unittest.TestCase):
    def test_add_player_method(self):
        game = Monopoly()
        game.add_player('Dave')
        self.assertEqual('Dave', game.players[0].name)


class TestCards(unittest.TestCase):
    #If a card is holdable, and the active_player opts to hold the card, then the card will be removed from the deck, and added to the active_player's hand
    #Else: Perform the action associated with the card, and move it to the end of the card list for that particular deck.
    def test_deal_from_chance_deck(self):
        chance_deck = Deck.build_chance_deck()
        active_player = Player('David')
        chance_deck.deal_from_deck(active_player)
        self.assertEqual(1700, active_player.liquid_holdings)
        active_player.liquid_holdings -= 200
        self.assertEqual(16, len(chance_deck.cards))
        self.assertEqual('Advance to Go', chance_deck.cards[-1].face)

    #nonconsumable cards, verify that the cards advance to the back of the deck when used, and that their associated actions are performed on a given Player object
    def test_deal_from_community_deck(self):
        community_deck = Deck.build_communbity_deck()
        active_player = Player('Sara')
        community_deck.deal_from_deck(active_player)
        self.assertEqual(1700, active_player.liquid_holdings)
        self.assertEqual('Advance to Go', community_deck.cards[-1].face)
        self.assertEqual(16, len(community_deck.cards))
        community_deck.deal_from_deck(active_player)
        self.assertEqual(1950, active_player.liquid_holdings)
        self.assertEqual('Bank error in your favor', community_deck.cards[-1].face)
        self.assertEqual('Doctor\'s fees', community_deck.cards[0].face)

    #Verify that a card can be dealt, then consumed and restored to its respective deck
    def test_deal_single_consumable_card(self):
        community_deck = Deck.build_communbity_deck()
        chance_deck = Deck.build_chance_deck()
        active_player = Player('David')
        for i in range(8):
            community_deck.deal_from_deck(active_player)
            chance_deck.deal_from_deck(active_player)
        self.assertEqual(2, len(active_player.hand))
        self.assertEqual('Get out of Jail Free', active_player.hand[0].face)
        self.assertEqual('Get out of Jail Free', active_player.hand[1].face)



    def test_use_consumable_card(self):
        pass

class TestKeyObjects(unittest.TestCase):

    def test_deal_from_deck(self):
        pass

    def verify_card_actions(self):
        pass

    def test_player_addition(self):
        pass

    def test_dice_roll(self):
        pass

if __name__ == '__main__':
    unittest.main()

#Helpful resource for constructing tests:  https://www.hasbro.com/common/instruct/monins.pdf

