from monopoly import *

class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        #if statement is part of test code, comment out when running outside of unit tests
        if len(option_list) > 0:
            selection = input(f'\nYour options are: {self.ml_printer(option_list)}\nWhat would you like to do {self.game.active_player.name}?\nType a number from the list and press Enter, to do nothing, enter 0:  ')
            if int(selection) == 0:
                return None
            return option_list[int(selection) - 1].action

    """Direct sale methods are:
        -get_amount(): asks the active_player how much they'd like to sell a particular item for
            -Takes item as an input, and returns an int representing the sell price
        -pick_eligible_buyer(): asks the active_player to pick from a list of eligible buyers (eligible = can afford to buy the item at the amount specified in the previous method)
            -Takes a list of players as an input, returns a Player object
        -get_buy_decision(): Asks the chosen buyer if they want to purchase the item
            -Takes an OwnableItem object, Player object, and an int representing the amount as inputs, returns True or False 
    """

    def get_amount(self, item):
        amount = int(input(f'{self.game.active_player.name}, how much would you like to sell {item.name}'))
        return amount

    def pick_eligible_buyer(self, eligible_buyers):
        eligible_buyer = input()
        return eligible_buyer

    def get_buy_decision(self, item, buyer, amount):
        buy_decision = input()
        return buy_decision



    def ml_printer(self, option_list):
        option_string = ''
        for n, option in enumerate(option_list, start=1):
            option_string += f'\n{n}: {option.option_name}'
        return option_string



if __name__ == '__main__':
    game_instance = Monopoly()



