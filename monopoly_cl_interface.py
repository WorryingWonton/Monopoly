from monopoly import *

def run_stuff():
    game = Monopoly()
    player_names = add_players()
    for player in player_names:
        game.add_player(player)
    print(game.players)


def turn_sequencer(game):
    active_player = game.advance_turn()
    if active_player.jailed:
        JailTile.jailed_dice_roll(active_player)



def if_jailed(player):
    pass




def add_players():
    player_names = []
    while True:
        if len(player_names) == 6:
            break
        else:
            new_player = input('Enter a name for your player, or enter \'stop\'')
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