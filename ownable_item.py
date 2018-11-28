from auction import Auction
import cards

class OwnableItem:

    def find_owner(self, game):
        for player in game.players:
            if isinstance(self, cards.Card):
                for card in player.hand:
                    if card == self:
                        return player
            else:
                for tile in player.property_holdings:
                    if tile == self:
                        return player
        return game.bank

    def start_direct_sale_process(self, game):
        amount = game.interface.get_amount_to_sell(item=self)
        eligible_buyers = self.find_eligible_buyers(game=game, amount=amount)
        if eligible_buyers:
            buyer = game.interface.pick_eligible_buyer(eligible_buyers)
            if buyer:
                buyer_decision = game.interface.get_buy_decision(item=self, amount=amount, buyer=buyer)
                if buyer_decision:
                    self.complete_transaction(buyer=buyer, seller=game.active_player, amount=amount, game=game)
                else:
                    self.start_auction_process(game=game)
            else:
                self.start_auction_process(game=game)

    def start_direct_buy_process(self, game):
        owner = self.find_owner(game=game)
        amount = game.interface.get_amount_to_buy(item=self, owner=owner)
        seller_decision = game.interface.get_sell_decision(item=self, proposed_amount=amount, seller=owner)
        if seller_decision:
            self.complete_transaction(buyer=game.active_player, seller=owner, amount=amount, game=game)

    def complete_transaction(self, buyer, seller, amount, game):
        return

    def start_auction_process(self, game):
        seller = self.find_owner(game=game)
        winning_bid = Auction(game=game, item=self, seller=seller).auction_item()
        if winning_bid:
            if winning_bid[0].liquid_holdings < winning_bid[1]:
                game.run_bankruptcy_process(debtor=winning_bid[0], creditor=game.active_player)
            else:
                self.complete_transaction(buyer=winning_bid[0], seller=seller, amount=winning_bid[1], game=game)

    def find_eligible_buyers(self, game, amount):
        return list(filter(lambda player: player.liquid_holdings >= amount and player != game.active_player, game.players))