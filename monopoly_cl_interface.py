from monopoly import *

class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        selection = input(f'Your options are: {self.ml_printer(option_list)}\nWhat would you like to do {self.game.active_player.name}?\nType a number from the list and press Enter:  ')
        return option_list[int(selection) - 1][1]

    def ml_printer(self, option_list):
        option_string = ''
        line_count = 1
        for option in option_list:
            option_string += f'\n{line_count}: {option[0]}'
            line_count += 1
        return option_string


        # return '\n'.join([x[0] for x in option_list])

if __name__ == '__main__':
    game_instance = Monopoly()
