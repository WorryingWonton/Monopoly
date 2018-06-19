from monopoly import *
player_1 = Player('Leslie')
card = Card('Pay Income Tax', pay_income_tax)
card.action(player_1)
print(player_1.liquid_holdings)