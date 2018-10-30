import unittest
import monopoly
import tiles
import cards
class TestMonopolyInitialization(unittest.TestCase):
    def test_game_initialization(self):
        game_instance = monopoly.Monopoly()
        self.assertEqual(40, len(game_instance.board))
        self.assertEqual(0, len(game_instance.players))
        print(game_instance.chance_deck)
        self.assertEqual(16, len(game_instance.chance_deck.cards))
        self.assertEqual(16, len(game_instance.community_deck.cards))
        self.assertEqual(0, game_instance.turns)

class TestPlayerInitialization(unittest.TestCase):
    def test_add_player_method(self):
        game = monopoly.Monopoly()
        game.add_player('Dave')
        self.assertEqual('Dave', game.players[0].name)

    def test_active_player_cycling(self):
        game = monopoly.Monopoly()
        game.add_player('Sara')
        game.add_player('Bill')
        self.assertEqual('Sara', game.active_player.name)
        self.assertEqual('Bill', game.active_player.name)
        self.assertEqual('Sara', game.active_player.name)

class TestCards(unittest.TestCase):
    pass


class TestJailTile(unittest.TestCase):
    """
    This will verify the core aspects of the behavior for the JailTile, and the various other game functions which relate to it
    """
    pass


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

