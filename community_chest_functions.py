from tiles import *

def get_tile_positions(game, target=None, name=None):
    if target and name:
        raise Exception('Cannot search for both an instance of a Tile and the name of the Property on a Tile, pass one or the other.')
    if target:
        return [tile.position for tile in game.board if isinstance(tile, target)]
    if name:
        return [tile.position for tile in game.board if tile.property.name == name]

def advance_to_go(game):
    tile_position = get_tile_positions(target=GoTile, game=game)
    game.active_player.position = tile_position[0]
    game.board[game.active_player.position].tile_actions()

def go_to_jail(game):
    game.active_player.jailed = True
    game.active_player.position = get_tile_positions(game=game, target=JailTile)[0]
    game.board[game.active_player.position].tile_actions(game=game)

def get_out_jail_free(game):
    game.active_player.jailed = False
    game.dice_roll = game.roll_dice()
    game.active_player.advance_position(amount=sum(game.dice_roll))
    game.board[game.active_player.position].tile_actions(game=game)

def bank_error_in_your_favor(game):
    game.active_player.liquid_holdings += 250

def from_sale_of_stock_50(game):
    game.active_player.liquid_holdings += 50

def doctors_fee(game):
    if game.active_player.liquid_holdings >= 200:
        game.active_player.liquid_holdings -= 200
    else:
        game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)

def grand_opera_night(game):
    for player in [player for player in game.players if player != game.active_player]:
        if player.liquid_holdings >= 50:
            player.liquid_holdings -= 50
            game.active_player.liquid_holdings += 50
        else:
            game.run_bankruptcy_process(debtor=player, creditor=game.active_player)

def holiday_fund_matures(game):
    game.active_player.liquid_holdings += 100

def income_tax_refund(game):
    game.active_player.liquid_holdings += 20

def it_is_your_birthday(game):
    for player in [player for player in game.players if player != game.active_player]:
        if player.liquid_holdings >= 10:
            player.liquid_holdings -= 10
            game.active_player.liquid_holdings += 10
        else:
            game.run_bankruptcy_process(debtor=player, creditor=game.active_player)

def life_insurace_matures(game):
    game.active_player.liquid_holdings += 100

def pay_hospital_fees(game):
    if game.active_player.liquid_holdings >= 100:
        game.active_player.liquid_holdings -= 100
    else:
        game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)

def pay_school_fees(game):
    if game.active_player.liquid_holdings >= 150:
        game.active_player.liquid_holdings -= 150
    else:
        game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)

def receive_25_consultancy_fee(game):
    game.active_player.liquid_holdings += 25

def you_are_assessed_for_street_repairs(game):
    amount_assessed = 0
    color_tiles_with_structures = [tile for tile in game.active_player.property_holdings if len(tile.property.existing_structures) > 0 and isinstance(tile, ColorTile)]
    for tile in color_tiles_with_structures:
        for structure in tile.property.existing_structures:
            if structure.type == 'hotel':
                amount_assessed += 115
            if structure.type == 'house':
                amount_assessed += 30
    return amount_assessed

def you_have_won_second_prize_in_a_beauty_contest(game):
    game.active_player.liquid_holdings += 10

def you_inherit_100(game):
    game.active_player.liquid_holdings += 100

