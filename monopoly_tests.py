import unittest
from monopoly import *
from monopoly_cl_interface import *

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

    def test_active_player_cycling(self):
        game = Monopoly()
        game.add_player('Sara')
        game.add_player('Bill')
        self.assertEqual('Sara', game.active_player.name)
        game.advance_turn()
        self.assertEqual('Bill', game.active_player.name)
        game.advance_turn()
        self.assertEqual('Sara', game.active_player.name)

class TestTurnHandling(unittest.TestCase):
    pass





class TestCards(unittest.TestCase):
    #If a card is holdable, and the active_player opts to hold the card, then the card will be removed from the deck, and added to the active_player's hand
    #Else: Perform the action associated with the card, and move it to the end of the card list for that particular deck.
    def test_deal_from_chance_deck(self):
        chance_deck = Deck.build_chance_deck()
        active_player = Player('David', game=None)
        chance_deck.deal_from_deck(active_player)
        self.assertEqual(1700, active_player.liquid_holdings)
        active_player.liquid_holdings -= 200
        self.assertEqual(16, len(chance_deck.cards))
        self.assertEqual('Advance to Go', chance_deck.cards[-1].face)

    #nonconsumable cards, verify that the cards advance to the back of the deck when used, and that their associated actions are performed on a given Player object
    def test_deal_from_community_deck(self):
        community_deck = Deck.build_communbity_deck()
        active_player = Player('Sara', game=None)
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
        game = Monopoly()
        game.add_player('David')
        for i in range(6):
            game.chance_deck.deal_from_deck(game.players[0])
            print(f'Position: {game.players[0].position}, Assets: {game.players[0].liquid_holdings}')

    def test_deal_multiple_consumable_cards(self):
        pass

    def test_use_consumable_card(self):
        pass

# class TestPlayerOptions(unittest.TestCase):
#     def test_railroad_tile_options(self):
#         game = Monopoly()
#         game.add_player('David')
#         game.players[0].position = 5
#         self.assertEqual(['Buy', 'Mortgage', 'Pass/Send to Auction'], game.board[5].tile_actions(active_player=game.players[0], players=game.players, dealt_card=None))


class TestAncillaryMethods(unittest.TestCase):

    def test_deal_from_deck(self):
        pass

    def verify_card_actions(self):
        pass

    def test_player_addition(self):
        pass

    def test_dice_roll(self):
        pass


class TestSingleTurn(unittest.TestCase):
    def test_railroad_tile_option_list(self):
        game_instance = Monopoly()
        game_instance.add_player('David')
        game_instance.add_player('Sara')
        game_instance.players[0].position = 5
        option_list = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        self.assertEqual('Buy Railroad', option_list[0][0])
        self.assertEqual('Mortgage RailRoad', option_list[1][0])

    def test_railroad_tile(self):
        game_instance = Monopoly()
        game_instance.add_player('David')
        game_instance.add_player('Sallie')
        #Move David to the RailRoad tile
        game_instance.players[0].position = 5
        #Monopoly.run_turn() will not be used for this test, as it moves the player forward by the outcome of the dice roll each time it's called.
        option_list = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # self.assertEqual('Buy Railroad', monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list))
        #Note that running this line requires user input.  Choose the option to buy the railroad.
        game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list))
        self.assertEqual(True, isinstance(game_instance.active_player.property_holdings[0], RailRoadTile))
        game_instance.advance_turn()
        self.assertEqual('Sallie', game_instance.active_player.name)
        game_instance.active_player.position = 5
        game_instance.advance_turn()
        option_list_turn_3 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_3))
        self.assertEqual('trainstation', game_instance.board[5].property.existing_structures.type)












if __name__ == '__main__':
    unittest.main()

#Helpful resource for constructing tests:  https://www.hasbro.com/common/instruct/monins.pdf

