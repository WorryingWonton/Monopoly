import unittest
from monopoly import *
class TestKeyObjects(unittest.TestCase):

    def test_property_initialization(self):
        ownable_property_test = OwnableTile(position=5, property='Noodles')
        self.assertEqual(5, ownable_property_test.position)
        self.assertEqual('Noodles', ownable_property_test.property)
        bad_ownable_property_test = OwnableTile(position='Hello', property='Noodles')
        self.assertEqual('Hello', bad_ownable_property_test.position)



    #Verify deck lengths and that all items in the community and chance decks are card objects, and that the lists contain cards with the correct atributes
    #Note that calling Deck.make_deck() automatically calls Deck.shuffle_deck()

    def test_deck_construction(self):
        pass

    def test_deal_from_deck(self):
        pass

    def test_player_addition(self):
        pass

    def test_dice_roll(self):
        pass

if __name__ == '__main__':
    unittest.main()

