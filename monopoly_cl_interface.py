from distutils.util import strtobool
from monopoly import *
class CLInterface():
    def __init__(self, game):
        self.game = game

    def get_decision(self, option_list):
        #if statement is part of test code, comment out when running outside of unit tests
        if len(option_list) > 0:
            while True:
                try:
                    selection = int(input(f'''
Your options are: {self.ml_printer(option_list)}
What would you like to do {self.game.active_player.name}?
Type a number from the list and press Enter, to do nothing, enter 0:  '''))
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

    def ml_printer(self, option_list, start=1):
        option_string = ''
        for n, option in enumerate(option_list, start=start):
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

    def auction_sell_assets_to_bank(self, bidder, options, bid):
        """
        This method presents a Player with options to sell their assets (where applicable) to the Bank.
        It takes a Player object and a list of Option objects as inputs and returns an Int represeting the bidder's choice
        :param Player bidder:  Player object
        :param List options: List of Option objects
        :return: None
        """
        selection = self.get_number(input_message=f"""
        Overbid Warning!
        {bidder.name}, your bid exceeds your liquid holdings (${bidder.liquid_holdings}) by ${bid - bidder.liquid_holdings}
        Your options are:
            1. Enter a different bid
            2. Quit the auction (your bid will not be counted)
            3. Submit bid anyways (This will cause you to go bankrupt)
            {self.ml_printer(option_list=options, start=4)}
            Pick a number from the list and press Enter: """)
        return selection

    def re_bid(self, bidder, current_bid):
        new_bid = self.get_number(input_message=f"""
        {bidder.name}, your current bid is ${current_bid}, you have chosen to enter a different bid.
        What is your new bid?  $""")
        return new_bid

    def get_bid(self, bidder, item, highest_bid, seller):
        print(f'Auction for {item.name} sold by {seller.name}!')
        if not highest_bid:
            bid = self.get_number(input_message=f"""
            {bidder.name}, your current liquid holdings are ${bidder.liquid_holdings}, and you have a gross worth of ${bidder.find_gross_worth()}
            You are the first bidder.
            To exit the auction, enter a value less than ${highest_bid}
            How much would you like to bid?  $""")
        else:
            bid = self.get_number(input_message=f"""
                {bidder.name}, your current liquid holdings are ${bidder.liquid_holdings}, and you have a gross worth of ${bidder.find_gross_worth()}
                The current highest bid for {item.name} is ${highest_bid}
                To exit the auction, enter a value less than ${highest_bid}
                How much would you like to bid?  $""")
        return bid

    def get_number(self, input_message):
        while True:
            number = input(input_message)
            try:
                int(number)
                return int(number)
            except:
                print('Please enter a number: ')

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

    def add_players(self):
        print("""
Welcome to Command Line Monopoly!
Once two or more players have been added, the game can start.
The game will run until all but one player has been bankrupted.
Command Line Monopoly attempts to follow the rules for Monopoly as specified in:
https://www.hasbro.com/common/instruct/monins.pdf
This game has one notable exceptions to the normal rules of Monopoly:
    1.  Not opting to buy an unowned property during a turn will NOT result in it being put up for auction.
To start, enter the names of the participants below.  The turn order for the game is based on the order
in which players are added to it.
""")
        while len(self.game.all_players) < 6:
            player_name = input(f'''
    To stop entering players, type \'stop\'.
    What is Player {len(self.game.all_players) + 1}\'s name?  ''')
            if player_name.lower() == 'stop':
                if len(self.game.all_players) < 2:
                    raise Exception('Not enough players in the game to start.')
                else:
                    break
            else:
                self.game.add_player(name=player_name)



"""
Option objects can contain 14 different categories in Monopoly.
The interface should entirely determine how an Option is displayed.


"""

