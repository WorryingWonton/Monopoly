import random

class HelperFunctions:

    @staticmethod
    def roll_dice():
        return (random.randint(1, 6), random.randint(1, 6))

    @staticmethod
    def afforadable(object, player):
        if player.liquid_holdings >= object.price:
            return True