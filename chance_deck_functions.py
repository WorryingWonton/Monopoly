from monopoly import Tile, Board
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

def advance_token_to_nearset_railroad(player, player_list):
    if player.position % 40 < 5:
        player.position = 5
    elif player.position % 40 < 15:
        player.position = 15
    elif player.position % 40 < 25:
        player.position = 25
    elif player.position % 40 < 35:
        player.position = 35
    rent_multiplier = 0
    #Two loops, the first to determine who owns the tile the active Player is on, the second to determine how many other rail road properties that player owns
    tile_owner = None
    for participant in player_list:
        for tile in participant.property_holdings:
            if tile.position == player.position:
                tile_owner = participant
    if tile_owner:
        for tile in tile_owner.property_holdings:
            if tile.property.type == 'railroad':
                rent_multiplier += 1
        tile_owner.liquid_holdings += 25 * 2**(rent_multiplier - 1)
        player.liquid_holdings -= 25 * 2**(rent_multiplier - 1)
    else:
        purchase_decision = input('The railroad you are on is available for purchase, the price is $200. \n If you want to buy it, enter \'true\', otherwise enter \'false\'').lower()
        if purchase_decision in ['true', 'y', 'yes']:
            if player.liquid_holdings >= 200:
                player.property_holdings += Board().board[player.position]
                player.liquid_holdings -= 200
            else:
                return f'You do not have enough funds {player.name}, you need $200, you have {player.liquid_holdings}'




