import attr
import monopoly
import monopoly_cl_interface
import ownable_item

class Property:

    def __init__(self, name, price, mortgage_price, possible_structures, base_rent):
        self.name = name
        self.price = price
        self.mortgage_price = mortgage_price
        #List of structure objects that can be built on the property
        self.possible_structures = possible_structures
        self.base_rent = base_rent
        self.existing_structures = []
        self.mortgaged = False

class Structure:
    def __init__(self, type, price, rent):
        self.type = type
        self.price = price
        self.rent = rent

#tile_action(self) --- Performs the relevant actions for a tile when called.

@attr.s
class Tile:
    position = attr.ib(type=int)

    def tile_actions(self, game):
        """Performs all appropriate actions associated with the Tile object in play
            Assumes active_player is on the Tile"""
        return []

    def find_properties_of_other_players(self, game):
        property_tuples = [(list(filter(lambda tile: tile.determine_if_sellable(owner=player), player.property_holdings)), player) for player in list(filter(lambda player: player != game.active_player, game.players))]
        option_list = []
        for n_tuple in property_tuples:
            for tile in n_tuple[0]:
                if tile.property.mortgaged:
                    option_list.append(monopoly.Option(option_name=f'''Request to buy {tile.property.name} from {n_tuple[1].name} --- (Property deed price is {tile.property.price}) --- WARNING: Property IS Mortgaged''', action=tile.start_direct_buy_process, item_name=f'{tile.property.name}'))
                else:
                    option_list.append(monopoly.Option(option_name=f'''Request to buy {tile.property.name} from {n_tuple[1].name} --- (Property deed price is {tile.property.price}) --- Property IS NOT Mortgaged''', action=tile.start_direct_buy_process, item_name=f'{tile.property.name}'))
        return option_list


#Should be able to tell if the property on the Tile is on the market, how many like tiles the Owner of the landed on tile has, determine if the Tile can be sold (I think this may be unique to color tiles)
@attr.s
class OwnableTile(Tile, ownable_item.OwnableItem):
    property: Property = attr.ib()

    def tile_actions(self, game):
        owner = self.find_owner(players=game.players)
        if owner:
            return self.if_owned(owner=owner, game=game)
        else:
            return self.if_not_owned(active_player=game.active_player)

    #Find owner of tile occupied by the active_player, if no owner, return None
    def find_owner(self, players):
        for player in players:
            for property in player.property_holdings:
                if property == self:
                    return player
        return None

    def if_owned(self, owner, game):
        pass

    def if_not_owned(self, active_player):
        buy_mortgage_option_list = []
        if self.property.price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(monopoly.Option(option_name=f'Buy {self.property.name} at position: {self.position}', action=self.buy_property, item_name=self.property.name))
        if self.property.mortgage_price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(monopoly.Option(option_name=f'Mortgage {self.property.name} at position: {self.position}', action=self.mortgage_property, item_name=self.property.name))
        return buy_mortgage_option_list

    def buy_property(self, game):
        game.active_player.liquid_holdings -= self.property.price
        game.active_player.property_holdings.append(self)

    def mortgage_property(self, game):
        game.active_player.liquid_holdings -= self.property.mortgage_price
        game.active_player.property_holdings.append(self)
        self.property.mortgaged = True

    def mortgage_owned_property(self, game):
        game.active_player.liquid_holdings += self.property.mortgage_price
        self.property.mortgaged = True

    def lift_mortgage(self, game):
        game.active_player.liquid_holdings -= 0.1*self.property.mortgage_price
        self.property.mortgaged = False

    #Below method finds out how many similar properties an owner has
    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if type(self) == type(tile):
                num_tiles += 1
        return num_tiles

    def determine_if_sellable(self, owner):
        """
        :param Player owner:  Player object who owns the tile
        :return: Returns either an empty list or a list containing an Option object which will start the direct sale process if chosen by the player
        """
        if self in owner.property_holdings:
            if len(self.property.existing_structures) > 0:
                return []
            else:
                return [monopoly.Option(option_name=f'Sell {self.property.name}', action=self.start_direct_sale_process, item_name=self.property.name),
                        monopoly.Option(option_name=f'Sell {self.property.name} to the Bank for {0.5 * self.property.price}', action=self.sell_to_bank, item_name=self.property.name)]
        else:
            return []

    def sell_to_bank(self, game):
        game.active_player.liquid_holdings += self.property.price * 0.5
        game.active_player.property_holdings.remove(self)

    def start_direct_sale_process(self, game):
        amount = game.interface.get_amount_to_sell(item=self.property)
        eligible_buyers = self.find_eligible_buyers(game=game, amount=amount)
        buyer = game.interface.pick_eligible_buyer(eligible_buyers)
        if buyer:
            buyer_decision = game.interface.get_buy_decision(item=self.property, amount=amount, buyer=buyer)
            if buyer_decision:
                self.complete_transaction(buyer=buyer, seller=game.active_player, amount=amount, game=game)
            else:
                self.start_auction_process(game=game, seller=game.active_player)
        else:
            self.start_auction_process(game=game, seller=game.active_player)

    def start_direct_buy_process(self, game):
        owner = self.find_owner(game.players)
        amount = game.interface.get_amount_to_buy(owner=owner, item=self.property)
        seller_decision = game.interface.get_sell_decision(item=self.property, seller=owner, proposed_amount=amount)
        if seller_decision:
            self.complete_transaction(buyer=game.active_player, seller=owner, amount=amount, game=game)

    def start_auction_process(self, game, seller):
        winning_bid = game.interface.run_auction(item=self.property, seller=seller)
        if winning_bid:
            if winning_bid[0].liquid_holdings < winning_bid[1]:
                game.run_bankruptcy_process(debtor=winning_bid[0], creditor=game.active_player)
            self.complete_transaction(buyer=winning_bid[0], seller=game.active_player, amount=winning_bid[1], game=game)

    def complete_transaction(self, buyer, seller, amount, game):
        if self.property.mortgaged:
            """This seems to be a grey area in the rules.  Normally, amount is just the deed price of the property, however the rules do not specify what happens if
            a mortgaged property is auctioned.  Or if, for that matter, if a mortgaged property can be auctioned.  I'm designing to the spec that a mortgaged property
            can be auctioned and the extra 10% assessed is based off the mortgage price."""
            if amount + 1.1 * self.property.mortgage_price <= buyer.liquid_holdings:
                immediate_unmortgage_decision = game.interface.get_buy_and_lift_mortgage_decision(buyer=buyer, seller=seller, amount=amount, item=self.property)
                if immediate_unmortgage_decision:
                    self.property.mortgaged = False
                    buyer.liquid_holdings -= 1.1 * self.property.mortgage_price
            buyer.liquid_holdings -= amount + 0.1*self.property.mortgage_price
            if buyer.liquid_holdings < 0:
                game.run_bankruptcy_process(debtor=buyer, creditor=seller)
                return
        else:
            buyer.liquid_holdings -= amount
            if buyer.liquid_holdings < 0:
                game.run_bankruptcy_process(debtor=buyer, creditor=seller)
        seller.property_holdings.remove(self)
        buyer.property_holdings.append(self)
        seller.liquid_holdings += amount

    def remove_structure(self, game):
        pass

    def assess_rent(self, owner, game):
        pass

@attr.s
class UnownableTile(Tile):
    pass

#tile_actions() needs to determine the Tile's state, perform automatic actions on the active_player as a function of that state, and return a list of options the player can choose from
@attr.s
class RailRoadTile(OwnableTile):

    def if_owned(self, owner, game):
        """
        :param active_player:
        :param owner:
        :param Monopoly game:
        :param dice_roll:
        :return:
        """
        if game.active_player == owner:
            sellability = self.determine_if_sellable(owner=owner)
            if sellability:
                if self.property.mortgaged:
                    if game.active_player.liquid_holdings >= self.property.price * 0.1:
                        return sellability + [monopoly.Option(option_name=f'Lift Mortgage on {self.property.name}', action=self.lift_mortgage, item_name=self.property.name)]
                    else:
                        return sellability + [monopoly.Option(option_name=f'Mortgage {self.propert.name}', action=self.mortgage_owned_property, item_name=self.property.name)]
                elif game.active_player.liquid_holdings >= self.property.possible_structures[0].price:
                    return sellability + [monopoly.Option(option_name=f'Build Transtation at {self.property.name}', action=self.build_train_station, item_name=self.property.name)]
                else:
                    return sellability
            else:
                return [monopoly.Option(option_name=f'Sell Trainstation at {self.property.name} to the Bank for {0.5*self.property.existing_structures[0].price}', action=self.remove_structure, item_name=self.property.existing_structures[0].type)]
        elif self.property.mortgaged:
            return []
        else:
            self.assess_rent(owner=owner, game=game)
            return []

    def assess_rent(self, owner, game):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        multiplier = 1
        if game.active_player.dealt_card:
            multiplier = 2
        if len(self.property.existing_structures) == 1 and self.property.existing_structures[0].type == 'transtation':
            rent = multiplier * self.property.existing_structures[0].rent * 2**(num_owned_railroads - 1)
        else:
            rent = multiplier * self.property.base_rent * 2**(num_owned_railroads - 1)
        if rent > game.active_player.liquid_holdings:
            game.run_bankruptcy_process(debtor=game.active_player, creditor=owner)
        else:
            owner.liquid_holdings += rent
            game.active_player.liquid_holdings -= rent

    def build_train_station(self, game):
        if game.active_player.liquid_holdings >= self.property.possible_structures[0].price:
            game.active_player.liquid_holdings -= self.property.possible_structures[0].price
            self.property.existing_structures.append(self.property.possible_structures[0])

    def remove_structure(self, game):
        self.property.existing_structures = []
        game.active_player.liquid_holdings += self.property.possible_structures[0].price

@attr.s
class JailTile(UnownableTile):

    def tile_actions(self, game):
        """
        :param Monopoly game: Reference to the instance of Monopoly
        :return list option_list: List containing either zero or one Option objects
        JailTile is an interesting class, in that much of the behavior that relates to it is carried out in the Player class
        or Monopoly class.  The tile_actions method for JailTile performs a dice_roll on the player, if the player lands doubles,
        they are freed from jail.  If they do not, then it checks to see if their liquid_holdings are greater than $50.  It also checks
        to see if the active_player has a Get Out of Jail Free card.  It then returns a list containing the applicable Option objects.
        If the active_player has been in jail for three turns, tile_actions() calls active_player.pay_jail_fine() method and returns an empty list.
        """
        option_list = []
        dice_roll = game.roll_dice()
        if game.active_player.jailed_turns < 3:
            if dice_roll[0] == dice_roll[1]:
                game.active_player.advance_position(amount=sum(dice_roll))
                game.dice_roll = dice_roll
                return game.board[game.active_player.position].tile_actions(game=game)
            if game.active_player.liquid_holdings >= 50:
                option_list.append(monopoly.Option(option_name='Pay Jail Fine ($50)', item_name=None, action=self.pay_jail_fine))
            for card in game.active_player.hand:
                if card.name == 'Get out of Jail Free':
                    option_list.append(monopoly.Option(option_name=f'Use {card.name} card from {card.parent_deck}', action=card.action, item_name=card.name))
        else:
            game.active_player.pay_jail_fine()
        return option_list

    def pay_jail_fine(self, game):
        game.active_player.liquid_holdings -= 50
        if game.active_player.liquid_holdings < 0:
            self.game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)
        else:
            game.active_player.jailed = False
            game.active_player.position = sum(game.roll_dice())

@attr.s
class CardTile(UnownableTile):
    pass

@attr.s
class ChanceTile(CardTile):

    def tile_actions(self, game):
        game.chance_deck.deal_from_deck(game=game)
        game.active_player.dealt_card.consume_card(game=game)
        return []

@attr.s
class CommunityChestTile(CardTile):

    def tile_actions(self, game):
        game.community_deck.deal_from_deck(game=game)
        game.active_player.dealt_card.consume_card(game=game)
        return []

@attr.s
class GoToJailTile(UnownableTile):

    def tile_actions(self, game):
        game.active_player.go_directly_to_jail()
        return []

@attr.s
class LuxuryTaxTile(UnownableTile):

    def tile_actions(self, game):
        if game.active_player.liquid_holdings >= 75:
            game.active_player.liquid_holdings -= 75
        else:
            game.run_bankruptcy_process(creditor=game.bank, debtor=game.active_player)
        return []

@attr.s
class FreeParking(UnownableTile):
    pass

@attr.s
class IncomeTaxTile(UnownableTile):

    def tile_actions(self, game):
        gross_worth = game.active_player.find_gross_worth()
        if gross_worth <= 2000:
            game.active_player.liquid_holdings -= .1 * gross_worth
        else:
            game.active_player.liquid_holdings -= 200
        return []
@attr.s
class GoTile(UnownableTile):

    def tile_actions(self, game):
        game.active_player.pass_go()
        return []

@attr.s
class UtilityTile(OwnableTile):

    def if_owned(self, owner, game):
        if owner == game.active_player:
            return self.determine_if_sellable(owner=owner)
        elif self.property.mortgaged:
            return []
        else:
            self.assess_rent(owner=owner, game=game)
            return []

    def assess_rent(self, owner, game):
        num_owned_utilites = self.count_similar_owned_properties(owner)
        rent_assessed = 0
        if num_owned_utilites == 1:
            rent_assessed =  sum(game.dice_roll) * 4
        if num_owned_utilites == 2:
            rent_assessed -= sum(game.dice_roll) * 10
        if rent_assessed >= game.active_player.liquid_holdings:
            game.run_bankruptcy_process(debtor=game.active_player, creditor=owner)
        else:
            owner.liquid_holdings += rent_assessed
            game.active_player.liquid_holdings -= rent_assessed

@attr.s
class ColorTile(OwnableTile):
    color = attr.ib(type=str)

    def if_owned(self, owner, game):
        if owner == game.active_player:
            structure_options = self.list_buildable_structures(game=game)
            return structure_options + self.determine_if_sellable(owner=owner)
        else:
            self.assess_rent(owner=owner, game=game)
            return []

    def assess_rent(self, game, owner):
        if len(self.property.existing_structures) == 0:
            rent = self.property.base_rent
        else:
            rent = self.property.existing_structures[-1].rent
        if rent > game.active_player.liquid_holdings:
            game.run_bankruptcy_process(creditor=owner, debtor=game.active_player)
        else:
            owner.liquid_holdings += rent
            game.active_player.liquid_holdings -= rent

    def list_buildable_structures(self, game):
        if self.determine_if_buildable(game=game):
            struct_tuples = [(tile, len(tile.existing_structures)) for tile in list(filter(lambda x: isinstance(x, ColorTile) and self.color == x.color and len(x.property.existing_structures) != len(x.property.possible_structures), game.active_player.property_holdings))]
            if not struct_tuples:
                return []
            else:
                struct_counts = [x[1] for x in struct_tuples]
                option_list = []
                for struct_tuple in struct_tuples:
                    if struct_tuple[1] == min(struct_counts) and struct_tuple[0].property.possible_structures[struct_tuple[1]].price <= game.active_player.liquid_holdings:
                        option_list.append(monopoly.Option(option_name=f'Build {struct_tuple[0].property.possible_structures[struct_tuple[1]]} on {struct_tuple[0].property.name}', action=self.build_structure, item_name=struct_tuple[0].property.possible_structures[struct_tuple[1]]))
                return option_list
        else:
            return []

    def determine_if_buildable(self, game):
        #Number of each colored tile
        color_group_dict = {'brown': 2, 'cyan': 3, 'pink': 3, 'orange': 3, 'red': 3, 'yellow': 3, 'green': 3, 'blue': 2}
        counter = 0
        for tile in game.active_player.property_holdings:
            if isinstance(tile, ColorTile) and tile.color == self.color:
                counter += 1
        return color_group_dict[self.color] == counter

    def list_removable_structures(self, game):
        struct_tuples = [(tile, len(tile.existing_structures)) for tile in list(filter(lambda x: isinstance(x, ColorTile) and self.color == x.color and len(x.property.existing_structures) > 0,  game.active_player.property_holdings))]
        if not struct_tuples:
            return []
        else:
            struct_counts = [x[1] for x in struct_tuples]
            option_list = []
            for struct_tuple in struct_tuples:
                if struct_tuple[1] == max(struct_counts):
                    option_list.append(monopoly.Option(option_name=f'Remove {struct_tuple[0].property.possible_structures[len(struct_tuple[0].property.existing_structures)]} on {struct_tuple[0].property.name}', action=self.remove_structure, item_name=struct_tuple[0].property.possible_structures[len(struct_tuple[0].property.existing_structures)]))
            return option_list

    def build_structure(self, game):
        game.active_player.liquid_holdings -= self.property.possible_structures[len(self.property.existing_structures)].price
        self.property.existing_structures.append(self.property.possible_structures[len(self.property.existing_structures)])

    def remove_structure(self, game):
        game.active_player.liquid_holdings += self.property.possible_structures[len(self.property.existing_structures)].price / 2
        self.property.existing_structures.remove(self.property.existing_structures[-1])
