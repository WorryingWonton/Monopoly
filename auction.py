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
                bid = self.game.interface.get_bid(bidder=self.current_bidder, item=self.item, highest_bid=self.highest_bid, seller=self.seller)
                if self.highest_bid is None or bid > self.highest_bid:
                    self.highest_bid = bid
                    self.highest_bidder = self.current_bidder
                else:
                    self.remove_bidder(bidder=self.current_bidder)
        for player in self.game.players:
            player.in_auction = True
        return (self.highest_bidder, self.highest_bid)