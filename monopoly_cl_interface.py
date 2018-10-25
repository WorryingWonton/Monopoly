from monopoly import *
from distutils.util import strtobool


class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        #if statement is part of test code, comment out when running outside of unit tests
        if len(option_list) > 0:
            while True:
                try:
                    selection = input(f'''
Your options are: {self.ml_printer(option_list)}
What would you like to do {self.game.active_player.name}?
Type a number from the list and press Enter, to do nothing, enter 0:  ''')
                    break
                except ValueError:
                    print('Please type a number corresponding to an item in the above list:  ')
            if int(selection) == 0:
                return None
            return option_list[int(selection) - 1]

    def get_amount_to_sell(self, item):
        """
        get_amount(): asks the active_player how much they'd like to sell a particular item for
            -Takes item as an input, and returns an int representing the sell price"""
        while True:
            try:
                amount = int(input(f'''
{self.game.active_player.name}, how much would you like to sell {item.name} for?'''))
                break
            except ValueError:
                print('Please enter a number:  ')
        return amount

    def get_amount_to_buy(self, item, owner):
        while True:
            try:
                amount = int(input(f'''
{self.game.active_player.name}, how much would you like to offer {owner.name} for {item.name}?  '''))
                break
            except ValueError:
                print('Please enter a number:  ')
        return amount

    def pick_eligible_buyer(self, eligible_buyers):
        """
        :param eligible_buyers: List of buyers who can afford the item at the amount specified in get_amount()
        :return: A Player object chosen by the active_player
        """
        while True:
            try:
                eligible_buyer = eligible_buyers[int(input(f'''
Below is a list of the players who can afford to buy your item
        {self.ml_player_printer(eligible_buyers)}
Pick a number from the list and press Enter:  ''')) - 1]
                break
            except ValueError:
                print('Please enter a number corresponding to a player from the list above:  ')
        return eligible_buyer

    def get_buy_decision(self, item, buyer, amount):
        """
        get_buy_decision(): Asks the chosen buyer if they want to purchase the item
            -Takes an OwnableItem object, Player object, and an int representing the amount as inputs, returns True or False"""
        while True:
            try:
                buy_decision = strtobool(input(f'''
{self.game.active_player.name} would like to sell you (--{buyer.name}--) {item.name} for ${amount}. 
Do you want to buy the item for ${amount}?  Enter Yes or No:  ''').lower())
                break
            except ValueError:
                print('Enter \'Yes\' or \'No\':  ')
        return buy_decision

    def get_buy_and_lift_mortgage_decision(self, item, buyer, seller, amount):
        while True:
            try:
                buy_decision = strtobool(input(f'''
{buyer.name}, you have chosen to buy {item.name} from {seller.name}.
This property is mortgaged.  You can lift the mortgage now for an additional {0.1*item.price} over {amount}
The total cost of doing so is {0.1*item.price + amount}.  
Unmortgaging a property at the time of purchase will save you an additional {0.1*item.price} later on as well as immediately let you charge rent and develop on {item.name}
Do you wish to buy and lift the mortgage?  Entering No will just buy the property:  ''').lower())
                break
            except ValueError:
                print('Enter \'Yes\' or \'No\':  ')
        return buy_decision

    def get_sell_decision(self, item, seller, proposed_amount):
        while True:
            try:
                sell_decision = strtobool(input(f'''
{seller.name}, {self.game.active_player.name} would like to buy {item.name} off you for ${proposed_amount}.
Would you like to sell for this price?  Enter Yes or No:  ''').lower())
                break
            except ValueError:
                print('Enter \'Yes\' or \'No\':  ')
        return sell_decision

    def run_auction(self, item, seller):
        participants = list(filter(lambda player: player != seller, self.game.players))
        winning_bid = ()
        highest_bid = 0
        while len(participants) > 1:
            for player in participants:
                current_bid = input(f'''
{player.name}, the highest bid for {item.name} is currently {highest_bid}.
If you quit after submitting a bid, you are required to buy the item up for auction, if your bid is the highest bid.
Enter an amount larger than {highest_bid}, enter an equal or smaller amount to quit the auction:  ''')
                try:
                    int(current_bid)
                except:
                    participants.remove(player)
                    break
                current_bid = int(current_bid)
                if current_bid <= highest_bid:
                    participants.remove(player)
                else:
                    highest_bid = current_bid
                    winning_bid = (player, highest_bid)
        return winning_bid

    def ml_printer(self, option_list):
        option_string = ''
        for n, option in enumerate(option_list, start=1):
            option_string += f'''
        {n}: {option.option_name}'''
        return option_string

    #What's a good way to consolidate this with ml_printer?
    def ml_player_printer(self, eligible_players):
        option_string = ''
        for n, player in enumerate(eligible_players, start=1):
            option_string += f'''
        {n}: {player.name}'''
        return option_string


    def display_current_game_state(self):
        """This method runs at the beginning of each turn, and shows the complete state of the game:
                -Players:
                    Player Position
                    Player Property Holdings
                        Status of each property in holding
                            Existing Structures
                            Mortgaged
                    Player Hand
                    Jailed Status
                -Game:
                    Dice Roll
                    Turn Iteration
                    Active Player Name
                    Elapsed Time since starting the game"""
        pass


if __name__ == '__main__':
    game_instance = Monopoly()



# next_active_player = players[(players.find(active_player) + 1) % len(players)]