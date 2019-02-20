class Auction:

    def __init__(self, game, item, seller):
        self.game = game
        self.item = item
        self.seller = seller
        self.current_bidder = None
        self.highest_bid = None
        self.bidders = []
        self.highest_bidder = None

    def set_current_bidder(self):
        if not self.current_bidder:
            self.current_bidder = self.game.players[0]
        else:
            self.current_bidder = self.bidders[(self.bidders.index(self.current_bidder) + 1) % len(self.bidders)]
        self.bidders = [bidder for bidder in self.bidders if bidder.in_auction]

    def remove_bidder(self, bidder):
        bidder.in_auction = False

    def auction_item(self):
        self.bidders = self.game.players
        while len(self.bidders) > 1:
            self.set_current_bidder()
            if self.current_bidder == self.highest_bidder:
                continue
            else:
                bid = self.get_bid()
                if self.highest_bid is None or bid > self.highest_bid:
                    self.highest_bid = bid
                    self.highest_bidder = self.current_bidder
                else:
                    self.remove_bidder(bidder=self.current_bidder)
        for player in self.game.players:
            player.in_auction = True
        return (self.highest_bidder, self.highest_bid)

    def get_bid(self):
        bid = self.game.interface.get_bid(bidder=self.current_bidder, item=self.item, highest_bit=self.highest_bid, seller=self.seller)
        if bid > self.highest_bid and bid > self.current_bidder.liquid_holdings and bid < self.current_bidder.find_gross_worth():
            self.case_2(bid=bid)
        return bid

    def case_2(self, bid):
        """
        case_2() is called when a bidder submits a bid valued between their current liquid holdings and their guaranteed gross worth.
        This method, and its associated interface methods, provide the bidder with the options to:
            1.  Submit a different bid
            2.  Submit no bid and back out of the auction
            3.  Proceed with their bid as is, and hope another player bids a larger amount
            4-n. Sell or mortgage some of their assets to the Bank.
        :param int bid: An integer representing the bid
        :return None:  This method has the side effects of removing the bidder from auction, increasing the bidder's liquid_holdings, or doing nothing.
        """
        while self.current_bidder.liquid_holdings < self.highest_bid:
            options = self.current_bidder.list_options_in_categories(categories=['selltobank', 'mortgageownedproperty', 'removestructure'])
            selection = self.game.interface.auction_case_2(bidder=self.current_bidder, options=options, bid=self.highest_bid)
            if selection == 1:
                self.game.interface.re_bid(current_bid=bid, bidder=self.current_bidder)
            elif selection == 2:
                self.remove_bidder(bidder=self.current_bidder)
            elif selection == 3:
                return
            else:
                self.game.execute_player_decsion(options[selection - 4])