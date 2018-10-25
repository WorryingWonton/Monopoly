class OwnableItem:

    def find_owner(self, game):
        pass

    def start_direct_sale_process(self, game):
        """Takes an instance of the item and the active_player, makes a series of interface calls to handle the sale of a property.
            -This method returns None
                -This is done because the transaction function in both the Card and OwnableTile classes (sell_card() and sell_property() respectively) requires additional arguments that the execute_player_decision
                    method in the Monopoly class cannot provide.  Therefore, this method is bypassed.
            -If a direct sale cannot be made, then the item will go to auction (Note that the auction method(s) is in the cl_interface module.
            """
        pass

    def start_direct_buy_process(self, game):
        pass

    def find_eligible_buyers(self, game, amount):
        return list(filter(lambda player: player.liquid_holdings >= amount and player != game.active_player, game.players))

    def start_auction_process(self, game, seller):
        """This method is called under three conditions:
            1.  The active player calls it directly
            2.  The amount the active player asked to sell an item for was higher than any other player could afford (i.e. find_eligible_players returned an empty list)
            3.  The buyer chosen by the player did not want to buy the item
            When it's called, all players except the active player have the chance to bid on the item for a set period of time.
            Most of the work for handling an auction is done by the interface module, all this does is call CLInterface.run_auction(item) and parse the returned 2 tuple from
            said method (WinngingPlayer, winning_bid).
            If run_auction() returns None, this method passes.
            """
        pass

    def complete_transaction(self, buyer, seller, amount, game):
        pass