from monopoly import *
from distutils.util import strtobool

def run_stuff():
    game = Monopoly()
    player_names = add_players()
    for player in player_names:
        game.add_player(player)
    print(game.players)
    turn_sequencer(game)


def turn_sequencer(game):
    while len(game.players) > 1:
        active_player = game.advance_turn()
        if active_player.jailed:
            JailTile.jailed_dice_roll(active_player)
        else:
            active_player.position += sum(HelperFunctions.roll_dice())
        if len(active_player.property_holdings) > 0:
            handle_builds(active_player)

def if_jailed(player):
    pass

def handle_builds(player):
    buildable_colors = Player.determine_buildable_tiles(player)
    buildable_color_tiles = []
    for color in buildable_colors:
        for tile in player.property_holdings:
            if tile.color == color:
                buildable_color_tiles.append(tile)
    railroads = list(filter(lambda x: isinstance(x, RailRoadTile), player.property_holdings))
    bct_index = 0
    while bct_index < len(buildable_color_tiles):
        buy_decision = strtobool(input(f'Do you want to buy {buildable_color_tiles[bct_index]}?  Enter yes or no:  ').lower())
        if buy_decision:
            buildable_color_tiles[bct_index].build_evenly()
            return
        bct_index += 1
    rr_index = 0
    while rr_index < len(railroads):
        buy_decision = strtobool(input(f'Do you want to buy {buildable_color_tiles[bct_index]}?  Enter yes or no:  ').lower())
        if buy_decision:
            railroads[rr_index].build_train_station()
            return
        rr_index += 1

def add_players():
    player_names = []
    while True:
        if len(player_names) == 6:
            break
        else:
            new_player = input('Enter a name for your player, or enter \'stop\':  ')
            if new_player.lower() == 'stop':
                break
            else:
                player_names.append(new_player)
    if len(player_names) >= 2:
        return player_names
    else:
        raise Exception('Monopoly requires two more players.')

if __name__ == '__main__':
    run_stuff()