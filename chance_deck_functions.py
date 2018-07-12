def advance_to_go(player):
    #What position is 'Go'?
    player.position = 0
    player.liquid_holdings += 200

def advance_to_illinois_ave(player):
    if player.position % 40 > 24:
        player.liquid_holdings += 200
    player.position = 24

def advance_to_st_charles_place(player):
    if player.position % 40 > 11:
        player.liquid_holdings += 200
    player.position = 11

#Utilities at 12 and 28
#Note if Card.face == 'Advance token to nearest Utility', do not call the if_owned() method on the utility tile in question
def advance_to_nearest_utility(player):
    if player.position % 40 > 28:
        player.position = 12
    if player.position % 40 > 12:
        player.position = 28
    player.liquid_holdings -= 10 * sum(HelperFunctions.roll_dice())


def advance_token_to_nearset_railroad(player, board):
    if player.position % 40 < 5:
        player.position = 5
    elif player.position % 40 < 15:
        player.position = 15
    elif player.position % 40 < 25:
        player.position = 25
    elif player.position % 40 < 35:
        player.position = 35
    working_tile = board[player.position]
    tile_owner = working_tile.find_owner()
    if tile_owner:
        working_tile.if_owned(player, tile_owner)
        working_tile.if_owned(player, tile_owner)
    else:
        working_tile.if_not_owned(player)

def bank_pays_you_50_dividend(player):
    player.liquid_holdings += 50

def get_out_jail_free(player):
    player.jailed = False
    player.position += HelperFunctions.roll_dice()

def go_back_3_spaces(player):
    player.position -= 3

def go_to_jail(player):
    player.jailed = True
    player.position = 10

def make_general_repairs_on_all_property(player):
    for tile in player.property_holdings:
        if len(tile.property.existing_structures) > 0:
            if tile.property.existing_structures[-1].type == 'hotel':
                player.liquid_holdings -= 100
            if tile.property.existing_structures[-1].type == 'house':
                player.liquid_holdings -= len(tile.property.existing_structures) * 25

def pay_poor_tax(player):
    player.liquid_holdings -= 15

def take_trip_to_reading_railroad(player):
    player.position = 5

def take_a_walk_on_boardwalk(player):
    player.position = 39

def chairman_of_the_board(player, player_list):
    for participant in player_list:
        participant.liquid_holdings += 50
        player.liquid_holdings -= 50

def your_building_loan_matures(player):
    player.liquid_holdings += 150

def you_have_won_a_crossword_competition(player):
    player.liquid_holdings += 100







