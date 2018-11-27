from itertools import islice, dropwhile, cycle

class Auction:

    def __init__(self, game, item):
        self.game = game
        self.item = item
        self.current_bidder = None
        self.highest_bid = 0
        self.bidders = []
        self.highest_bidder = None

    def set_current_bidder(self):
        if not self.current_bidder:
            self.current_bidder = self.game.players[0]
        else:
            self.current_bidder = next(dropwhile(lambda bidder: bidder.find_gross_worth() >= self.highest_bid, islice(dropwhile(lambda bidder: not self.current_bidder, cycle(self.bidders)), 1, None)))
        self.bidders = [player for player in self.game.players if player.find_gross_worth() >= self.highest_bid]

    def auction_item(self):
        while len(self.bidders) > 1:
            self.set_current_bidder()
            bid = self.game.interface.get_bid(bidder=self.current_bidder, item=self.item, highest_bid=self.highest_bid)
            if bid and bid > self.highest_bid:
                self.highest_bid = bid
                self.highest_bidder = self.current_bidder
            else:
                self.bidders.remove(self.current_bidder)
        return (self.highest_bid, self.highest_bidder)