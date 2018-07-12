#I'm going to put all of the card action functions here.
#Community Chest Functions
def advance_to_go(player):
    #What position is 'Go'?
    player.position = 0
    player.liquid_holdings += 200

def go_to_jail(player):
    player.jailed = True
    player.position = 10

def get_out_jail_free(player):
    player.jailed = False
    player.position += HelperFunctions.roll_dice()

def bank_error_in_your_favor(player):
    player.liquid_holdings += 200

def doctors_fee(player):
    player.liquid_holdings -= 200

def grand_opera_night_opening(player, monopoly):
    for person in monopoly.players:
        player.liquid_holdings += 50
        person.liquid_holdings -= 50

def holiday_fund_matures(player):
    player.liquid_holdings += 100

def income_tax_refund(player):
    player.liquid_holdings += 20

def it_is_your_birthday(player, monopoly):
    for person in monopoly.players:
        player.liquid_holdings += 10
        person.liquid_holdings -= 10

def life_insurace_matures(player):
    player.liquid_holdings += 100

def pay_hospital_fees(player):
    player.liquid_holdings -= 100

def pay_school_fees(player):
    player.liquid_holdings -= 150

def receive_25_consultancy_fee(player):
    player.liquid_holdings += 25

def you_are_assessed_for_street_repairs(player):
    for property in player.property_holdings:
        if property.lower() == 'hotel':
            player.liquid_holdings -= 115
        #I'm not sure if there are other kinds of properties
        if property.lower() == 'house':
            player.liquid_holdings -= 40

def you_have_won_second_prize_in_a_beauty_contest(player):
    player.liquid_holdings += 10

def you_inherit_100(player):
    player.liquid_holdings += 100

