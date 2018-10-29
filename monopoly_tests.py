import unittest
import monopoly
import tiles

# class TestMonopolyInitialization(unittest.TestCase):
#     def test_game_initialization(self):
#         game_instance = Monopoly()
#         self.assertEqual(40, len(game_instance.board))
#         self.assertEqual(0, len(game_instance.players))
#         print(game_instance.chance_deck)
#         self.assertEqual(16, len(game_instance.chance_deck))
#         self.assertEqual(16, len(game_instance.community_deck))
#         self.assertEqual(0, game_instance.turns)
#
# class TestPlayerInitialization(unittest.TestCase):
#     def test_add_player_method(self):
#         game = Monopoly()
#         game.add_player('Dave')
#         self.assertEqual('Dave', game.players[0].name)
#
#     def test_active_player_cycling(self):
#         game = Monopoly()
#         game.add_player('Sara')
#         game.add_player('Bill')
#         self.assertEqual('Sara', game.active_player.name)
#         game.advance_turn()
#         self.assertEqual('Bill', game.active_player.name)
#         game.advance_turn()
#         self.assertEqual('Sara', game.active_player.name)
#
# class TestTurnHandling(unittest.TestCase):
#     pass
#
# class TestCards(unittest.TestCase):
#
#     #If a card is holdable, and the active_player opts to hold the card, then the card will be removed from the deck, and added to the active_player's hand
#     #Else: Perform the action associated with the card, and move it to the end of the card list for that particular deck.
#     def test_deal_from_chance_deck(self):
#         chance_deck = ChanceDeck()
#         player = Player('David', game=None)
#         chance_deck.deal_from_deck(active_player=player)
#         self.assertEqual(advance_to_go, player.dealt_card.action)
#         self.assertEqual(15, len(chance_deck.cards))
#
#     #nonconsumable cards, verify that the cards advance to the back of the deck when used, and that their associated actions are performed on a given Player object
#     def test_deal_from_community_deck(self):
#         community_deck = CommunityChest()
#         active_player = Player('Sara', game=None)
#         community_deck.deal_from_deck(active_player=active_player)
#         self.assertEqual(advance_to_go, active_player.dealt_card.action)
#         self.assertEqual(15, len(community_deck.cards))
#
#     #Verify that a card can be dealt, then consumed and restored to its respective deck
#     def test_deal_single_consumable_card(self):
#         game = Monopoly()
#         game.add_player('David')
#         for i in range(6):
#             game.chance_deck.deal_from_deck(game.players[0])
#             print(f'Position: {game.players[0].position}, Assets: {game.players[0].liquid_holdings}')
#
#     def test_deal_multiple_consumable_cards(self):
#         pass
#
#     def test_use_consumable_card(self):
#         pass
#
# # class TestPlayerOptions(unittest.TestCase):
# #     def test_railroad_tile_options(self):
# #         game = Monopoly()
# #         game.add_player('David')
# #         game.players[0].position = 5
# #         self.assertEqual(['Buy', 'Mortgage', 'Pass/Send to Auction'], game.board[5].tile_actions(active_player=game.players[0], players=game.players, dealt_card=None))
#
#
# class TestAncillaryMethods(unittest.TestCase):
#
#     def test_deal_from_deck(self):
#         pass
#
#     def verify_card_actions(self):
#         pass
#
#     def test_player_addition(self):
#         pass
#
#     def test_dice_roll(self):
#         pass


class TestSingleTurn(unittest.TestCase):
    # def test_railroad_tile_option_list(self):
    #     game_instance = Monopoly()
    #     game_instance.add_player('David')
    #     game_instance.add_player('Sara')
    #     game_instance.players[0].position = 5
    #     option_list = game_instance.board[game_instance.active_player.position].tile_actions(game_instance.active_player, game_instance.players, None)
    #     self.assertEqual('Buy Railroad at position: 5', option_list[0][0])
    #     self.assertEqual('Mortgage RailRoad at position: 5', option_list[1][0])

    #Note that running this line requires user input.  Choose the option to buy the railroad
    #Monopoly.run_turn() will not be used for this test, as it moves the player forward by the outcome of the dice roll each time it's called
    #Sallie and David will complete laps around the board, David will buy railroads upon landing on them and attempt to bankrupt Sallie
        #This test should accomplish the following:
            #Correctly initialization of a monopoly game and the addition of two players to that game
            #Verification of the correct operation of the tile_actions function for a player that does, and a player that does not own the railroad tile.
            #Verification of the correct operation of the execute_player_decision method

    def test_railroad_tile(self):
        game_instance = monopoly.Monopoly()
        game_instance.add_player('David')
        game_instance.add_player('Sallie')
        game_instance.add_player('Michelle')
        # game_instance.players[0].hand.append(Card(name='Get out of Jail Free', action=get_out_jail_free, holdable=True, passes_go=False))
        result = game_instance.run_game()
        # self.assertEqual('David', result.name)



class TestColorTile(unittest.TestCase):

    def test_determine_if_buildable(self):
        """
        This test will verify that ColorTile.determine_if_buildable() will only return True if a Player owns all
        tiles within a color-set.
        :return None:
        """
        game_instance = monopoly.Monopoly()
        game_instance.add_player('Bob')
        game_instance.active_player = game_instance.players[0]
        game_instance.players[0].property_holdings.append(game_instance.board[37])
        #Case 1:  Player does not have all tiles within a color-set
        self.assertEqual(False, game_instance.board[37].determine_if_buildable(game=game_instance))
        game_instance.players[0].property_holdings.append(game_instance.board[39])
        #Case 2:  Player owns all tiles within a color-set
        self.assertEqual(True, game_instance.board[39].determine_if_buildable(game=game_instance))

    def test_list_buildable_structures(self):
        game_instance = monopoly.Monopoly()
        #Add a player, add both blue properties to the player's property goldings
        game_instance.add_player(name='Alan')
        game_instance.active_player = game_instance.players[0]
        game_instance.players[0].property_holdings.append(game_instance.board[37])
        game_instance.players[0].property_holdings.append(game_instance.board[39])
        #Verify that the list_buildable_structures() returns the option to build a house on each blue tile, given that no structures are currently present
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        #Build a house on Park Place, verify that a second house cannot be built on same, then verify that a house can still be build on Park Place
        game_instance.board[37].build_structure(game=game_instance)
        self.assertEqual([], game_instance.board[37].list_buildable_structures(game=game_instance))
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        #Build a house on Boardwalk, verify that houses can again be built on both Park Place and BoardWalk
        game_instance.board[39].build_structure(game=game_instance)
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        #The tests below this comment will verify that houses can be built via the Build Evenly rule until len(existing_structures) = len(possible_structures) on both Park Place and Boardwalk
        game_instance.board[39].build_structure(game=game_instance)
        self.assertEqual([], game_instance.board[39].list_buildable_structures(game=game_instance))
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[37].build_structure(game=game_instance)
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[37].build_structure(game=game_instance)
        self.assertEqual([], game_instance.board[37].list_buildable_structures(game=game_instance))
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[39].build_structure(game=game_instance)
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Build house on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[39].build_structure(game=game_instance)
        self.assertEqual([], game_instance.board[39].list_buildable_structures(game=game_instance))
        #Test to verify that the active player cannot afford to buy the next house
        self.assertEqual([], game_instance.board[37].list_buildable_structures(game=game_instance))
        game_instance.active_player.liquid_holdings += 10000
        self.assertEqual('Build house on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[37].build_structure(game=game_instance)
        self.assertEqual('Build hotel on Park Place', game_instance.board[37].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Build hotel on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        game_instance.board[37].build_structure(game=game_instance)
        self.assertEqual('Build hotel on Boardwalk', game_instance.board[39].list_buildable_structures(game=game_instance)[0].option_name)
        self.assertEqual([], game_instance.board[37].list_buildable_structures(game=game_instance))
        game_instance.board[39].build_structure(game=game_instance)
        self.assertEqual([], game_instance.board[39].list_buildable_structures(game=game_instance))
        self.assertEqual([], game_instance.board[37].list_buildable_structures(game=game_instance))

    def test_list_removable_structures(self):
        game_instance = monopoly.Monopoly()
        game_instance.add_player('Bill')
        game_instance.active_player = game_instance.players[0]
        game_instance.active_player.property_holdings = [tile for tile in game_instance.board if isinstance(tile, tiles.ColorTile) and tile.color == 'green']
        for tile in game_instance.active_player.property_holdings:
            tile.property.existing_structures += tile.property.possible_structures
        self.assertEqual('Remove hotel on Pacific Avenue', game_instance.board[31].list_removable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Remove hotel on North Carolina Avenue', game_instance.board[32].list_removable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Remove hotel on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
        game_instance.board[31].remove_structure(game=game_instance)
        self.assertEqual([], game_instance.board[31].list_removable_structures(game=game_instance))
        self.assertEqual('Remove hotel on North Carolina Avenue', game_instance.board[32].list_removable_structures(game=game_instance)[0].option_name)
        self.assertEqual('Remove hotel on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
        game_instance.board[32].remove_structure(game=game_instance)
        self.assertEqual([], game_instance.board[31].list_removable_structures(game=game_instance))
        self.assertEqual([], game_instance.board[32].list_removable_structures(game=game_instance))
        self.assertEqual('Remove hotel on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
        game_instance.board[34].remove_structure(game=game_instance)
        counter = 0
        while len(game_instance.board[31].property.existing_structures) > 0:
            self.assertEqual('Remove house on Pacific Avenue', game_instance.board[31].list_removable_structures(game=game_instance)[0].option_name)
            self.assertEqual('Remove house on North Carolina Avenue', game_instance.board[32].list_removable_structures(game=game_instance)[0].option_name)
            self.assertEqual('Remove house on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
            game_instance.board[31].remove_structure(game=game_instance)
            self.assertEqual([], game_instance.board[31].list_removable_structures(game=game_instance))
            self.assertEqual('Remove house on North Carolina Avenue', game_instance.board[32].list_removable_structures(game=game_instance)[0].option_name)
            self.assertEqual('Remove house on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
            game_instance.board[32].remove_structure(game=game_instance)
            self.assertEqual([], game_instance.board[31].list_removable_structures(game=game_instance))
            self.assertEqual([], game_instance.board[32].list_removable_structures(game=game_instance))
            self.assertEqual('Remove house on Pennsylvania Avenue', game_instance.board[34].list_removable_structures(game=game_instance)[0].option_name)
            game_instance.board[34].remove_structure(game=game_instance)
            counter += 1
        #Verify that the while loop ran for four iterations
        self.assertEqual(len(game_instance.board[31].property.possible_structures) - 1, counter)
        for tile in game_instance.active_player.property_holdings:
            self.assertEqual([], tile.property.existing_structures)


if __name__ == '__main__':
    unittest.main()

#Helpful resource for constructing tests:  https://www.hasbro.com/common/instruct/monins.pdf

