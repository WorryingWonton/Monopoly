from tiles import *

def get_tile_positions(game, target=None, name=None):
    if target and name:
        raise Exception('Cannot search for both an instance of a Tile and the name of the Property on a Tile, pass one or the other.')
    if target:
        return [tile.position for tile in game.board if isinstance(tile, target)]
    if name:
        return [tile.position for tile in game.board if tile.property.name == name][0]

def advance_to_go(game):
    tile_position = get_tile_positions(target=GoTile, game=game)
    game.active_player.position = tile_position[0]
    game.board[game.active_player.position].tile_actions(game=game)

def advance_to_illinois_ave(game):
    tile_position = get_tile_positions(name='Illinois Avenue', game=game)
    game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=tile_position))
    game.board[game.active_player.position].tile_actions(game=game)

def advance_to_st_charles_place(game):
    tile_position = get_tile_positions(name='Illinois Avenue', game=game)
    game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=tile_position))
    game.board[game.active_player.position].tile_actions(game=game)

def advance_to_nearest_utility(game):
    utility_tile_positions = get_tile_positions(game=game, target=UtilityTile)
    nearest_tile_positions = list(filter(lambda x: x > game.active_player.position % 40, utility_tile_positions))
    if not nearest_tile_positions:
        game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=utility_tile_positions[0]))
    else:
        game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=nearest_tile_positions[0]))
    game.dice_roll = game.roll_dice()
    game.board[game.active_player.position].tile_actions(game=game)

def advance_token_to_nearset_railroad(game):
    railroad_tile_positions = get_tile_positions(game=game, target=RailRoadTile)
    nearest_tile_positions = list(filter(lambda x: x > game.active_player.position % 40, railroad_tile_positions))
    if not nearest_tile_positions:
        game.active_player.position = railroad_tile_positions[0]
        game.active_player.pass_go()
    else:
        game.active_player.position = nearest_tile_positions[0]
    game.board[game.active_player.position].tile_actions(game=game)

def bank_pays_you_50_dividend(game):
    game.active_player.liquid_holdings += 50

def get_out_jail_free(game):
    game.active_player.jailed = False
    game.dice_roll = game.roll_dice()
    game.active_player.advance_position(amount=sum(game.dice_roll))
    game.board[game.active_player.position].tile_actions(game=game)

def go_back_3_spaces(game):
    game.active_player.advance_position(amount=-3)
    game.board[game.active_player.position].tile_actions(game=game)

def go_to_jail(game):
    game.active_player.jailed = True
    game.active_player.position = get_tile_positions(game=game, target=JailTile)[0]
    game.board[game.active_player.position].tile_actions(game=game)

def make_general_repairs_on_all_property(game):
    color_tiles = [tile for tile in game.active_player.property_holdings if isinstance(tile, ColorTile) and len(tile.property.existing_structures) > 0]
    repair_cost = 0
    for tile in color_tiles:
        for structure in tile.existing_structures:
            if structure.type == 'hotel':
                repair_cost += 100
            if structure.type == 'house':
                repair_cost += 25
    if game.active_player.liquid_holdings >= repair_cost:
        game.active_player.liquid_holdings -= repair_cost
    else:
        game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)

def pay_poor_tax(game):
    if game.active_player.liquid_holdings >= 15:
        game.active_player.liquid_holdings -= 15
    else:
        game.run_bankruptcy_process(creditor=game.bank, debtor=game.active_player)

def take_trip_to_reading_railroad(game):
    rrr_pos = get_tile_positions(name='Reading Railroad', game=game)
    game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=rrr_pos))
    game.board[game.active_player.position].tile_actions()

def take_a_walk_on_boardwalk(game):
    bw_pos = get_tile_positions(name='Boardwalk', game=game)
    game.active_player.advance_position(amount=game.active_player.compute_advancement_amount(target_position=bw_pos))
    game.board[game.active_player.position].tile_actions()

def chairman_of_the_board(game):
    non_active_players = [player for player in game.players if player != game.active_player]
    if len(non_active_players) * 50 <= game.active_player.liquid_holdings:
        for participant in game.players:
            participant.liquid_holdings += 50
            game.active_player.liquid_holdings -= 50
    else:
        amount_disbursed_to_player = game.active_player.liquid_holdings / len(non_active_players)
        for player in non_active_players:
            player.liquid_holdings += amount_disbursed_to_player
        game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)

def your_building_loan_matures(game):
    game.active_player.liquid_holdings += 150

def you_have_won_a_crossword_competition(game):
    game.active_player.liquid_holdings += 100







