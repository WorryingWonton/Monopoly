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
def advance_to_nearest_utility(player):
    if player.position % 40 > 28:
        player.position = 12
        player.liquid_holdings -= 150
    if player.position % 40 > 12:
        player.position = 28
        player.liquid_holdings -= 150

def advance_token_to_nearset_railroad(player, player_list, board):
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





