from monopoly import *

def initialize_game():
    game = Monopoly()
    player_names = add_players()
    for player in player_names:
        game.add_player(player)
    turn_sequencer(game)


def turn_sequencer(game):
    while len(game.players) > 1:
        print_game_state(game)
        active_player = game.advance_turn()
        if active_player.jailed:
            JailTile.jailed_dice_roll(active_player)
        else:
            active_player.position += sum(HelperFunctions.roll_dice())
        if len(active_player.property_holdings) > 0:
            handle_builds(active_player)
        decision_list = []
        #If a player lands on a tile, if_owned, rent will be deducted according to the if_owned method of the tile object
        #if the tile is not owned, the if_not_owned method will be called on the Tile, and the output of that appended to the decision list
        action = input('This will do something')
        game.eject_bankrupt_players()
    return f'{game.players[0].name} has won the game.'

def if_jailed(player):
    pass

def print_game_state(game):
    #print state of players (liquidities, properties, and debts)
    for player in game.players:
        player_state = f'\nPlayer: {player.name} at Position: {player.position} on Tile: {type(game.board[player.position % 40])} \nLiquid Assets: {player.liquid_holdings} \nDebts: {player.debts} \nProperty Holdings: '
        if len(player.property_holdings) > 0:
            for tile in player.property_holdings:
                player_state += f'  Position:  {tile.position} - Property Name: {tile.property.name} - Structures: '
                if len(tile.property.existing_structures) > 0:
                    player_state += '- '
                    for structure in tile.property.existing_structures:
                        player_state += f'{structure.type} -'
                    player_state += '\n'
                else:
                    player_state += 'None\n'
        print(player_state + '\n')



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
            buildable_color_tiles[bct_index].build_structures()
            return
        bct_index += 1
    rr_index = 0
    while rr_index < len(railroads):
        buy_decision = strtobool(input(f'Do you want to buy {buildable_color_tiles[bct_index]}?  Enter yes or no:  ').lower())
        if buy_decision:
            railroads[rr_index].build_train_station()
            return
        rr_index += 1

def handle_buying(game, active_player):
    active_tile = game.board[active_player.position]

def handle_card_tiles(game,active_player):
    pass

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
    initialize_game()