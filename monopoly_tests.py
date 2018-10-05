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

class TestCards(unittest.TestCase):
    #If a card is holdable, and the active_player opts to hold the card, then the card will be removed from the deck, and added to the active_player's hand
    #Else: Perform the action associated with the card, and move it to the end of the card list for that particular deck.
    def test_deal_from_deck(self):
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

