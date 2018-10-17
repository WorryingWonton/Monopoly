from monopoly import *

class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        #if statement is part of test code, comment out when running outside of unit tests
        if len(option_list) > 0:
            selection = input(f'\nYour options are: {self.ml_printer(option_list)}\nWhat would you like to do {self.game.active_player.name}?\nType a number from the list and press Enter, to do nothing, enter 0:  ')
            list_item_types = [SellPropertyOption, SellCardOption]
            if type(option_list[int(selection) - 1]) in list_item_types:
                return self.list_item(option_list[int(selection) - 1])
            return option_list[int(selection) - 1][1]

        #Other player is chosen automatically and agrees to buy the property at $100
    #Takes active player, requests input for the desired sell price of the property.
        #Generates two additonal parameters,
    def list_item(self, option):
        player_list = [x for x in list(filter(lambda x: x != self.game.active_player, self.game.players))]
        chosen_player = int(input(f'{self.game.active_player}, which player would you like to {option.option_name} to?\n{self.ml_printer(player_list)}\nEnter a number from the list above: '))
        #TODO add defensive coding to deal with a player entering a letter, float, or symbol.
        amount = int(f'You have chosen to sell {option.option_name} to {player_list[chosen_player - 1].name}.\nHow much would you like to sell this for?  Enter a whole dollar amount: ')
        chosen_player_decision = strtobool(input(f'{player_list[chosen_player - 1].name}, {self.game.active_player.name} would like to {option.option_name} for {amount}.\nDo you want to buy this at that amount?\nAnswering in the negative will put the item up for auction.\n').lower())
        if chosen_player_decision:
            return option.action(active_player=self.game.active_player, buyer=player_list[chosen_player - 1], amount=amount)




        # \nEnter the name of the player listed above:

    # def ml_printer(self, option_list):
    #     option_string = ''
    #     for n, option in enumerate(option_list, start=1):
    #         option_string += f'\n{n}: {option[0]}'
    #     return option_string

    def ml_printer(self, option_list):
        option_string = ''
        for n, option in enumerate(option_list, start=1):
            if type(option) == Player:
                option_string += f'\n{n}: {option.name}'
            else:
                option_string += f'\n{n}: {option.option_name}'
        return option_string


        # return '\n'.join([x[0] for x in option_list])

if __name__ == '__main__':
    game_instance = Monopoly()
