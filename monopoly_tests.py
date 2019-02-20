import unittest
import monopoly
import tiles
import cards
import auction
import monopoly_cl_interface

from unittest.mock import patch

class HelperFunctions:

    @staticmethod
    def get_tile_positions(game, target=None, name=None):
        """
        Global helper function to find Tiles, either by Property.name or by Class reference.
        :param game:
        :param target:
        :param name:
        :return:
        """
        if target and name:
            raise Exception('Cannot search for both an instance of a Tile and the name of the Property on a Tile, pass one or the other.')
        if target:
            return [tile.position for tile in game.board if isinstance(tile, target)]
        if name:
            ownable_tiles = list(filter(lambda tile: isinstance(tile, tiles.OwnableTile), game.board))
            return [tile.position for tile in ownable_tiles if tile.property.name == name][0]


class TestMonopolyInitialization(unittest.TestCase):

    def test_game_initialization(self):
        game_instance = monopoly.Monopoly()
        self.assertEqual(40, len(game_instance.board))
        self.assertEqual(0, len(game_instance.players))
        print(game_instance.chance_deck)
        self.assertEqual(16, len(game_instance.chance_deck.cards))
        self.assertEqual(16, len(game_instance.community_deck.cards))
        self.assertEqual(0, game_instance.turns)

    def test_default_interface(self):
        game_instance = monopoly.Monopoly()
        self.assertEqual(True, isinstance(game_instance.interface, monopoly_cl_interface.CLInterface))

    def test_output_of_rungame(self):
        game_instance = monopoly.Monopoly()
        game_instance.add_player('David')
        output = game_instance.run_game()
        self.assertEqual('David', output.name)


class TestActivePlayerCycling(unittest.TestCase):

    """
    These tests cover a variety of cases for removing Players from the game.
    Each test covers a specific removal case (like removing the active Player, or removing the Player immediately ahead of the Active Player)
    The goal of each test is to verify that if a Player is removed by whatever scenario the test covers, that the correct next Active Player will always be chosen.
    The methods looked at in these tests are:
        -Monopoly.remove_player()
        -Monopoly.set_active_player()
            -And by extension:  Monopoly.generate_in_game_players()
    """

    def test_next_player_removal(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.set_active_player()
        self.assertEqual('David', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Sara', my_game.active_player.name)
        my_game.remove_player(my_game.all_players[2])
        my_game.set_active_player()
        self.assertEqual(3, len(my_game.players))
        self.assertEqual('Mark', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('David', my_game.active_player.name)

    def test_active_player_removal(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.set_active_player()
        self.assertEqual('David', my_game.active_player.name)
        my_game.remove_player(my_game.all_players[0])
        self.assertEqual(4, len(my_game.players))
        my_game.set_active_player()
        self.assertEqual(3, len(my_game.players))
        self.assertEqual('Sara', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Alan', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Mark', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Sara', my_game.active_player.name)

    def test_player_removal_at_prior_index(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.set_active_player()
        my_game.set_active_player()
        my_game.remove_player(my_game.all_players[0])
        #The next active player should be Alan if David is removed, and the current active player is Sara
        my_game.set_active_player()
        self.assertEqual('Alan', my_game.active_player.name)

    def test_player_removal_at_arbitrary_forward_index(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.add_player('Bill')
        my_game.add_player('Bob')
        my_game.set_active_player()
        my_game.remove_player(my_game.players[3])
        self.assertEqual('David', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Sara', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Alan', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Bill', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Bob', my_game.active_player.name)
        my_game.set_active_player()

    def test_player_removal_at_arbitrary_prior_index(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.add_player('Bill')
        my_game.add_player('Bob')
        my_game.set_active_player()
        my_game.set_active_player()
        my_game.set_active_player()
        self.assertEqual('Alan', my_game.active_player.name)
        my_game.remove_player(my_game.all_players[0])
        my_game.set_active_player()
        self.assertEqual('Mark', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Bill', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Bob', my_game.active_player.name)
        my_game.set_active_player()
        self.assertEqual('Sara', my_game.active_player.name)

    def test_player_removal_at_last_index_in_players(self):
        my_game = monopoly.Monopoly()
        my_game.add_player('David')
        my_game.add_player('Sara')
        my_game.add_player('Alan')
        my_game.add_player('Mark')
        my_game.set_active_player()
        my_game.remove_player(my_game.all_players[-1])
        my_game.set_active_player()
        self.assertEqual('Sara', my_game.active_player.name)
        my_game.remove_player(my_game.all_players[2])
        my_game.set_active_player()
        self.assertEqual('David', my_game.active_player.name)

class TestAuction(unittest.TestCase):

    @patch('monopoly_cl_interface.CLInterface.get_bid', return_value=10)
    def test_get_bid_case_1(self, input):
        game_instance = monopoly.Monopoly()
        game_instance.add_player('David')
        game_instance.generate_in_game_players()
        item = cards.HoldableCard(name='Go to BEENUS', action=None, parent_deck='Beenus')
        auc_instance = auction.Auction(game=game_instance, seller=game_instance.players[0], item=item)
        auc_instance.current_bidder = game_instance.players[0]
        auc_instance.highest_bid = 5
        self.assertEqual(10, auc_instance.get_bid())

    def test_case_2(self, input):
        pass

class TestColorTile(unittest.TestCase):
    """
    These tests validate the various components that enable my ColorTile code to behave in a way consistent with the rules of Monopoly.
    These tests also look in detail at the methods associated with OwnableTile, and its parent class OwnableItem.
        -OwnableTile and OwnableItem are both abstract classes, and while they possess many concrete methods, there are no direct examples of either object in the game.
        -TestColorTile will be used to both define the spec for OwnableItem and OwnableTile, and verify their adherence to that spec.
        -Structure will have its own dedicated test suite to define its behavior in greater detail.
            -The only tests involving Structure objects in TestColorTile will be centered on validating the build even rule.
    """

    def test_is_color_group_filled(self):
        """
        This test will verify that ColorTile.is_color_group_filled() will only return True if a Player owns all
        tiles within a color-set.
        :return None:
        """
        game_instance = monopoly.Monopoly()
        game_instance.add_player('Bob')
        game_instance.generate_in_game_players()
        game_instance.active_player = game_instance.players[0]
        game_instance.players[0].property_holdings.append(game_instance.board[37])
        #Case 1:  Player does not have all tiles within a color-set
        self.assertEqual(False, game_instance.board[37].is_color_group_filled(game=game_instance))
        game_instance.players[0].property_holdings.append(game_instance.board[39])
        #Case 2:  Player owns all tiles within a color-set
        self.assertEqual(True, game_instance.board[39].is_color_group_filled(game=game_instance))

    def test_assess_rent(self):
        """
        Case 1: The Bank holds a ColorTile, verify that no rent is charged when a Player lands on it.
            -I should not have to test this here, but currently I don't have any tests for OwnableTile.perform_auto_actions()
        Case 2: A Player holds one or more ColorTiles in a color group, but does not hold all the tiles in a color group.
            -Verify that only ColorTile.base_rent is deducted from the Player's liquid holdings
        Case 3: A Player holds all ColorTiles in a color group.
            -Verfiy that double rent is charged
        Case 4:  A Player holds all ColorTiles in color group, but one of them is mortgaged.
            -Verify that if a Player lands on the mortgaged
        :return:
        """
        game_instance = monopoly.Monopoly()
        game_instance.add_player('Bill')
        game_instance.generate_in_game_players()
        game_instance.active_player = game_instance.players[0]
        game_instance.active_player.position = 37
        game_instance.board[37].perform_auto_actions(game=game_instance)
        #Verify Case 1, NOTE that ColorTile.assess_rent() was not called here, I instead had to call OwnableTile.perform_auto_actions()
        self.assertEqual(1500, game_instance.active_player.liquid_holdings)
        game_instance.add_player('Bob')
        game_instance.generate_in_game_players()
        game_instance.players[1].property_holdings.append(game_instance.board[37])
        game_instance.board[37].perform_auto_actions(game=game_instance)
        #Verify Case 2
        self.assertEqual(1465, game_instance.players[0].liquid_holdings)
        self.assertEqual(1535, game_instance.players[1].liquid_holdings)
        game_instance.players[1].property_holdings.append(game_instance.board[39])
        game_instance.board[37].perform_auto_actions(game=game_instance)
        #Verify Case 3
        self.assertEqual(1395, game_instance.players[0].liquid_holdings)
        self.assertEqual(1605, game_instance.players[1].liquid_holdings)
        game_instance.board[39].mortgaged = True
        game_instance.board[37].perform_auto_actions(game=game_instance)
        #Verify Case 4
        self.assertEqual(1325, game_instance.players[0].liquid_holdings)
        self.assertEqual(1675, game_instance.players[1].liquid_holdings)
        game_instance.players[0].position = 39
        self.assertEqual(1325, game_instance.players[0].liquid_holdings)
        self.assertEqual(1675, game_instance.players[1].liquid_holdings)


class TestIncomeTaxTile(unittest.TestCase):
    pass

class TestLuxuryTaxTile(unittest.TestCase):
    pass

class TestJailTile(unittest.TestCase):
    """
    This class will specify the behavior for the JailTile and GoToJailTile
    """
    pass

class TestCardTiles(unittest.TestCase):
    pass

class TestUtilityTiles(unittest.TestCase):
    pass

class TestGoTile(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()

#Helpful resource for constructing tests:  https://www.hasbro.com/common/instruct/monins.pdf

