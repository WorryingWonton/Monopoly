from monopoly import *
import monopoly_cl_interface
#1:  Determine active player
    #1.1 Pass interface current game state, if displaying it make sense
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
    while len(game.players) > 1:
        print(monopoly_cl_interface.print_game_state(game))
        active_player = game.advance_turn()
        if active_player.jailed:
            JailTile.jailed_dice_roll(active_player)
            if not active_player.jailed:
                game.board[2]




def check_for_get_out_of_jail_free(player):
    for card in player.hand:
        if card.face == 'Get out of Jail Free':
            return True




# def turn_sequencer(game):
#     while len(game.players) > 1:
#         print_game_state(game)
#         active_player = game.advance_turn()
#         if active_player.jailed:
#             JailTile.jailed_dice_roll(active_player)
#         else:
#             active_player.position += sum(HelperFunctions.roll_dice())
#         if len(active_player.property_holdings) > 0:
#             handle_builds(active_player)
#         decision_list = []
#         #If a player lands on a tile, if_owned, rent will be deducted according to the if_owned method of the tile object
#         #if the tile is not owned, the if_not_owned method will be called on the Tile, and the output of that appended to the decision list
#         action = input('This will do something')
#         game.eject_bankrupt_players()
#     return f'{game.players[0].name} has won the game.'