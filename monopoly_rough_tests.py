from community_chest_functions import *
from monopoly import *
player_1 = Player('Leslie')
card = Card('Pay Income Tax', receive_25_consultancy_fee)
card.action(player_1)
print(player_1.liquid_holdings)

my_game = Monopoly()
print(my_game.board)