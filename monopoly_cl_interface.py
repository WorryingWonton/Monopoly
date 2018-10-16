from monopoly import *

class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        #if statement is part of test code, comment out when running outside of unit tests
        if len(option_list) > 0:
            selection = input(f'\nYour options are: {self.ml_printer(option_list)}\nWhat would you like to do {self.game.active_player.name}?\nType a number from the list and press Enter:  ')
            return option_list[int(selection) - 1][1]

        #Other player is chosen automatically and agrees to buy the property at $100

    def list_property(self):
        pass

    def ml_printer(self, option_list):
        option_string = ''
        for n, option in enumerate(option_list, start=1):
            option_string += f'\n{n}: {option[0]}'
        # option_string.append(f'To do nothing, Enter {line_count + 1}')
        return option_string


        # return '\n'.join([x[0] for x in option_list])

if __name__ == '__main__':
    game_instance = Monopoly()
