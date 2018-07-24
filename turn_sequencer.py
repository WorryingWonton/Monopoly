import monopoly
#1:  Determine active player
#2:  Determine if active_player.jailed
    #If active_player.jailed: run JailTile.jailed_dice_roll(active_player)
        #If player.jailed becomes False:  Perform Tile action at player.position
        #If player.jailed remains True:  GoTo step 3
    #Else: Perform Tile action at player.position
#3 Run game.eject_bankrupt_players
#3 Determine board state
    #Determine state of active_player.property_holdings:
        #Use Player.determine_buildable_tiles() to determine which color tiles, if any, can have structures built upon them
        #
def turn_sequencer(game):
    pass