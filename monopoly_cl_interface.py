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
            return option_list[int(selection) - 1]


    def get_amount(self, item):
        """
        get_amount(): asks the active_player how much they'd like to sell a particular item for
            -Takes item as an input, and returns an int representing the sell price"""
        amount = int(input(f'\n{self.game.active_player.name}, how much would you like to sell {item.name} for?'))
        return amount

    def pick_eligible_buyer(self, eligible_buyers):
        """
        :param eligible_buyers: List of buyers who can afford the item at the amount specified in get_amount()
        :return: A Player object chosen by the active_player
        """
        eligible_buyer = eligible_buyers[int(input(f'\nBelow is a list of the players who can afford to buy your item\n{self.ml_player_printer(eligible_buyers)}\nPick a number from the list and press Enter:  ')) - 1]
        return eligible_buyer

    def get_buy_decision(self, item, buyer, amount):
        """
        get_buy_decision(): Asks the chosen buyer if they want to purchase the item
            -Takes an OwnableItem object, Player object, and an int representing the amount as inputs, returns True or False"""
        buy_decision = strtobool(input(f'\n{self.game.active_player} would like to sell you (--{buyer.name}--) {item.name} for ${amount}.\nDo you want to buy the item for ${amount}?  Enter Yes or No:  ').lower())
        return buy_decision

    def ml_printer(self, option_list):
        option_string = ''
        for n, option in enumerate(option_list, start=1):
            option_string += f'\n{n}: {option.option_name}'
        return option_string
    #What's a good way to consolidate this with ml_printer?
    def ml_player_printer(self, eligible_players):
        option_string = ''
        for n, player in enumerate(eligible_players, start=1):
            option_string += f'\n{n}: {player.name}'
        return option_string



if __name__ == '__main__':
    game_instance = Monopoly()



