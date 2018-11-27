from itertools import islice, dropwhile, cycle

class Auction:

    def __init__(self, game):
        self.game = game
        self.current_bidder = None
        self.highest_bid = 0
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

    def auction_item(self, item, seller):
        self.bidders = self.game.players
        while len(self.bidders) > 1:
            self.set_current_bidder()
            bid = self.game.interface.get_bid(bidder=self.current_bidder, item=item, highest_bid=self.highest_bid, seller=seller)
            if bid and bid > self.highest_bid:
                self.highest_bid = bid
                self.highest_bidder = self.current_bidder
            else:
                self.remove_bidder(bidder=self.current_bidder)
        for player in self.game.players:
            player.in_auction = True
        return (self.highest_bidder, self.highest_bid)