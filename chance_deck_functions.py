from monopoly_helper_functions import HelperFunctions
# from monopoly import RailRoadTile


def advance_to_go(game):
    #What position is 'Go'?
    game.active_player.position = 0
    game.active_player.liquid_holdings += 200

def advance_to_illinois_ave(game):
    if game.active_player.position == 24:
        game.active_player.liquid_holdings += 200
    game.active_player.position = 24

def advance_to_st_charles_place(game):
    if game.active_player.position == 11:
        game.active_player.liquid_holdings += 200
    game.active_player.position = 11

#Utilities at 12 and 28
#Note if Card.face == 'Advance token to nearest Utility', do not call the if_owned() method on the utility tile in question
def advance_to_nearest_utility(game):
    if game.active_player.position > 28:
        game.active_player.position = 12
    if game.active_player.position > 12:
        game.active_player.position = 28
    game.active_player.liquid_holdings -= 10 * sum(HelperFunctions.roll_dice())


def advance_token_to_nearset_railroad(game):
    railroad_tile_positions = [x.position for x in game.board if isinstance(x, RailRoadTile)]
    nearest_tile_positions = list(filter(lambda x: x > game.active_player.position % 40, railroad_tile_positions))
    if not nearest_tile_positions:
        game.active_player.position = railroad_tile_positions[0]
        game.active_player.pass_go()
    else:
        game.active_player.position = nearest_tile_positions[0]
    owner = game.board[game.active_player.position].find_owner(players=game.players)
    if owner == game.active_player:
        return
    else:
        game.board[game.active_player.position].assess_rent(owner=owner, game=game)

def bank_pays_you_50_dividend(game):
    game.active_player.liquid_holdings += 50

def get_out_jail_free(game):
    game.active_player.jailed = False
    game.active_player.position += HelperFunctions.roll_dice()

def go_back_3_spaces(game):
    game.active_player.advance_position(-3)

def go_to_jail(game):
    game.active_player.jailed = True
    game.active_player.position = 10

def make_general_repairs_on_all_property(game):
    for tile in game.active_player.property_holdings:
        if len(tile.property.existing_structures) > 0:
            if tile.property.existing_structures[-1].type == 'hotel':
                game.active_player.liquid_holdings -= 100
            if tile.property.existing_structures[-1].type == 'house':
                game.active_player.liquid_holdings -= len(tile.property.existing_structures) * 25

def pay_poor_tax(game):
    game.active_player.liquid_holdings -= 15

def take_trip_to_reading_railroad(game):
    game.active_player.position = 5

def take_a_walk_on_boardwalk(game):
    game.active_player.position = 39

def chairman_of_the_board(game):
    for participant in game.players:
        participant.liquid_holdings += 50
        game.active_player.liquid_holdings -= 50

def your_building_loan_matures(game):
    game.active_player.liquid_holdings += 150

def you_have_won_a_crossword_competition(game):
    game.active_player.liquid_holdings += 100







