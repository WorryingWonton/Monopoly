import unittest
import monopoly
import tiles
import cards

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

class TestCardFunctions(unittest.TestCase):
    """
    Each card has a unique function associated with it.  In total, between the Chance and Community Chest decks, there
    are 32 cards.  All Card functions read state, modify state, and return None.  Cards that modify a Player's position
    need to be able to call game.board[game.active_player.position].perform_auto_actions(game=game), so that appropriate
    actions are taken in accordance with the rules for the Tile said Player has been moved to.  This defines the
    signature generically of each card function as:
        def card_func(Monopoly):
            return None
    """
    game_instance = monopoly.Monopoly()
    game_instance.add_player('Bill')
    game_instance.add_player('Sara')
    game_instance.add_player('Mike')
    game_instance.generate_in_game_players()
    game_instance.set_active_player()
    game_instance.active_player.liquid_holdings = 10000

    def card_finder(self, card_name, deck):
        return [card for card in deck.cards if card.name.lower() == card_name.lower()][0]

    def test_advance_to_go(self, game=game_instance):
        """
        This Card appears in both the Chance and Community Chest decks.
        :param Monopoly game:
        :return:
        """
        #Move the active player to an arbitrary position on the Board, the Card should move the Active Player back to
        #position 0.
        game.active_player.position = 23
        game.active_player.dealt_card = self.card_finder(card_name='Advance to Go', deck=game.chance_deck)
        game.active_player.dealt_card.consume_card(game=game)
        self.assertEqual(10200, game.active_player.liquid_holdings)
        self.assertEqual(0, game.active_player.position)

    def test_advance_to_illinois_ave(self, game=game_instance):
        game.active_player.dealt_card = self.card_finder(card_name='Advance to Illinois Ave.', deck=game.chance_deck)
        game.active_player.dealt_card.consume_card(game=game)
        #Case 1, advancing to Illinois Avenue if the Tile is not owned
        self.assertEqual(get_tile_positions(game=game, name='Illinois Avenue'), game.active_player.position)
        self.assertEqual(10000, game.active_player.liquid_holdings)
        #Case 2, another player owns the Tile
        game.active_player.position = 0
        game.players[1].property_holdings.append(game.board[get_tile_positions(game=game, name='Illinois Avenue')])
        game.active_player.dealt_card = self.card_finder(card_name='Advance to Illinois Ave.', deck=game.chance_deck)
        game.active_player.dealt_card.consume_card(game=game)
        self.assertEqual(9980, game.active_player.liquid_holdings)

    def test_cards_that_move_to_ownable_tiles(self, game=game_instance):
        card_names = []




class TestBankruptcyHandling(unittest.TestCase):
    def test_bankruptcy_from_rent_assessed(self):
        """
        Player to Player Bankruptcy

        """
        pass

    def test_bankruptcy_for_fees_assessed(self):
        """
        Player to Bank Bankruptcy
        :return:
        """
        pass

class TestColorTile(unittest.TestCase):


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

