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
        self.assertEqual('Buy Railroad at position: 5', option_list[0][0])
        self.assertEqual('Mortgage RailRoad at position: 5', option_list[1][0])

    #Note that running this line requires user input.  Choose the option to buy the railroad
    #Monopoly.run_turn() will not be used for this test, as it moves the player forward by the outcome of the dice roll each time it's called
    #Sallie and David will complete laps around the board, David will buy railroads upon landing on them and attempt to bankrupt Sallie
        #This test should accomplish the following:
            #Correctly initialization of a monopoly game and the addition of two players to that game
            #Verification of the correct operation of the tile_actions function for a player that does, and a player that does not own the railroad tile.
            #Verification of the correct operation of the execute_player_decision method

    def test_railroad_tile(self):
        game_instance = Monopoly()
        game_instance.add_player('David')
        game_instance.add_player('Sallie')
        game_instance.players[0].hand.append(Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False))
        print(game_instance.players[0].hand)
        result = game_instance.run_game()
        self.assertEqual('David', result.name)




        # #Turn 1
        # self.assertEqual('David', game_instance.active_player.name)
        # game_instance.run_turn()
        # self.assertEqual(5, game_instance.active_player.position)
        # self.assertEqual(1300, game_instance.active_player.liquid_holdings)
        # self.assertEqual(RailRoadTile, type(game_instance.active_player.property_holdings[0]))
        #Turn 2

        # game_instance.active_player.position = 5
        # option_list_turn_1 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_1))
        # self.assertEqual(RailRoadTile, type(game_instance.active_player.property_holdings[0]))
        # self.assertEqual(1300, game_instance.active_player.liquid_holdings)
        # #Turn 2
        # game_instance.advance_turn()
        # game_instance.active_player.position += 5
        # option_list_turn_2 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_2))
        # self.assertEqual([], option_list_turn_2)
        # self.assertEqual(1475, game_instance.active_player.liquid_holdings)
        # #Turn 3
        # game_instance.advance_turn()
        # game_instance.active_player.position += 10
        # option_list_turn_2 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_2))
        # self.assertEqual([], option_list_turn_2)
        # self.assertEqual(1475, game_instance.active_player.liquid_holdings)



        # game_instance.players[0].position = 5
        # option_list_turn_1 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_1))
        # self.assertEqual(True, isinstance(game_instance.active_player.property_holdings[0], RailRoadTile))
        # game_instance.advance_turn()
        # self.assertEqual('Sallie', game_instance.active_player.name)
        # self.assertEqual(1500, game_instance.active_player.liquid_holdings)
        # game_instance.active_player.position = 5
        # option_list_turn_2 = game_instance.board[5].tile_actions(game_instance.active_player, game_instance.players, None)
        # self.assertEqual([], option_list_turn_2)
        # self.assertEqual(1475, game_instance.active_player.liquid_holdings)
        # game_instance.advance_turn()
        # option_list_turn_3 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_3))
        # self.assertEqual('trainstation', game_instance.board[5].property.existing_structures[0].type)
        # #Sallie is not the active player, so her holdings should not change during this run
        # self.assertEqual(1475, game_instance.players[1].liquid_holdings)
        # game_instance.advance_turn()
        # option_list_turn_4 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # self.assertEqual([], option_list_turn_4)
        # game_instance.advance_turn()
        # game_instance.active_player.position = 15
        # option_list_turn_5 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_5))
        # game_instance.advance_turn()
        # option_list_turn_6 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # self.assertEqual([], option_list_turn_6)
        # game_instance.advance_turn()
        # option_list_turn_7 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # game_instance.execute_player_decision(monopoly_cl_interface.CLInterface(game=game_instance).get_decision(option_list_turn_7))
        # game_instance.advance_turn()
        # option_list_turn_8 = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
        # self.assertEqual([], option_list_turn_8)
        # self.assertEqual(1350, game_instance.active_player.liquid_holdings)
















if __name__ == '__main__':
    unittest.main()

#Helpful resource for constructing tests:  https://www.hasbro.com/common/instruct/monins.pdf

