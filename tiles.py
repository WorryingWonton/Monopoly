import attr
import monopoly
import ownable_item
from math import floor
from auction import Auction


class Structure(ownable_item.OwnableItem):

    """
    My code will handle buying and selling Structures in the following ways:
        -Buying Structures:
            -The Option to buy a structure should only appear if the Player is able to place the structure on one of their tiles.
            -If two or more Players are able to build a structure, and the active player wishes (and is able) to buy a structure, AND the Bank only has one structure of that type left, then:
                -The structure shall be put up for auction.
                    -This is probably best handled in complete_transaction()
        -Selling Structures:
            -Structures can be sold to other eligible Players
                -Eligibility meaning the Players can both afford to buy the Structure AND have properties which can be developed.
        -Other Notes:
            -Players cannot buy structures unless they have a property on which to put them.
                -This is so players cannot hoard structures
            -When the game starts (in Monopoly.run_game() specifically), the Bank has a list attribute filled with the following:
                -32 Houses
                -12 Hotels
                -4 Railroads
            -Modifications:
                -RailRoadTile and ColorTile will need to have their remove_structure() and build_structure() equivalent methods
                modified to accommodate the new changes.
            -Structues could also be unlimited, though for the time being it might not make sense to not implement this feature.

    With the rules now set, the trick is to figure out how to go about buying a selling Structures.
    The problem is that Structures need to be removed from a specific Tile and also placed on a specific Tile:
        -Structures do not know what Tile they're on.
            -This could be solved by adding a current_tile attribute.
            -Structure.current_tile would initially be set to None, then set to whatever Tile it's placed on.
                -If the Structure is sold to the Bank, then the attribute will be set to None again.
        -There currently is no way to set the current_tile atribute
            -The changes to enable this need to occur in the following places:
                -ColorTile.build_structure() and ColorTile.remove_structure()

    """


    def __init__(self, type, price, rent, current_tile=None):
        self.type = type
        self.price = price
        self.rent = rent
        self.current_tile = current_tile

    def complete_transaction(self, buyer, seller, amount, game):
        """
        :param Player buyer:
        :param Player seller:
        :param amount:
        :param game:
        :return:
        """
        if self.price <= buyer.liquid_holdings:
            if seller == game.bank:
                pass

    def add_structure_to_tile(self, buyer):
        pass

    def remove_structure_from_tile(self, seller):
        pass



@attr.s
class Tile:
    position = attr.ib(type=int)

    def perform_auto_actions(self, game):
        pass

    def list_options(self, game):
        return []

    def find_properties_of_other_players(self, game):
        property_tuples = [(list(filter(lambda tile: tile.list_sell_options(owner=player), player.property_holdings)), player) for player in list(filter(lambda player: player != game.active_player, game.players))]
        option_list = []
        for n_tuple in property_tuples:
            for tile in n_tuple[0]:
                if tile.mortgaged:
                    option_list.append(monopoly.Option(option_name=f'''Request to buy {tile.name} from {n_tuple[1].name} --- (Property deed price is {tile.price}) --- WARNING: Property IS Mortgaged''', action=tile.start_direct_buy_process, item_name=f'{tile.name}', category='buymortgagedproperty'))
                else:
                    option_list.append(monopoly.Option(option_name=f'''Request to buy {tile.name} from {n_tuple[1].name} --- (Property deed price is {tile.price}) --- Property IS NOT Mortgaged''', action=tile.start_direct_buy_process, item_name=f'{tile.name}', category='buyownedproperty'))
        return option_list


@attr.s
class OwnableTile(Tile, ownable_item.OwnableItem):
    name = attr.ib(type=str)
    price = attr.ib(type=int)
    mortgage_price = attr.ib(type=int)
    base_rent = attr.ib(type=int)
    possible_structures = attr.ib(type=list)
    existing_structures = attr.ib(type=list, default=[])
    mortgaged = attr.ib(type=bool, default=False)

    def perform_auto_actions(self, game):
        if self.mortgaged:
            return
        owner = self.find_owner(game=game)
        if owner == game.active_player or owner == game.bank:
            return
        else:
            self.assess_rent(owner=owner, game=game)

    def if_not_owned(self, active_player):
        buy_mortgage_option_list = []
        if self.price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(monopoly.Option(option_name=f'Buy {self.name} at position: {self.position} for {self.price}', action=self.buy_property, item_name=self.name, category='buyunownedproperty'))
        if self.mortgage_price <= active_player.liquid_holdings:
            buy_mortgage_option_list.append(monopoly.Option(option_name=f'Mortgage {self.name} at position: {self.position} for {self.mortgage_price}', action=self.mortgage_property, item_name=self.name, category='mortgageunownedproperty'))
        buy_mortgage_option_list.append(monopoly.Option(option_name=f'Auction {self.name} at position: {self.position}', action=self.start_auction_process, item_name=self.name, category='auctionproperty'))
        return buy_mortgage_option_list

    def buy_property(self, game):
        game.active_player.liquid_holdings -= self.price
        game.active_player.property_holdings.append(self)
        game.bank.property_holdings.remove(self)

    def mortgage_property(self, game):
        game.active_player.liquid_holdings -= self.mortgage_price
        game.active_player.property_holdings.append(self)
        game.bank.property_holdings.remove(self)
        self.mortgaged = True

    def mortgage_owned_property(self, game):
        game.active_player.liquid_holdings += self.mortgage_price
        self.mortgaged = True

    def lift_mortgage(self, game):
        game.active_player.liquid_holdings -= 0.1*self.mortgage_price
        self.mortgaged = False

    def count_similar_owned_properties(self, owner):
        num_tiles = 0
        for tile in owner.property_holdings:
            if type(self) == type(tile):
                num_tiles += 1
        return num_tiles

    def list_sell_options(self, owner):
        """
        :param Player owner:  Player object who owns the tile
        :return list option_list: Returns either an empty list or a list containing an Option object which will start the direct sale process if chosen by the player
        """
        if self.existing_structures:
            return []
        option_list = []
        option_list.append(monopoly.Option(option_name=f'Sell {self.name}', action=self.start_direct_sale_process, item_name=self.name, category='selltoplayer'))
        if self.mortgaged:
            if owner.liquid_holdings >= 0.1 * self.price + self.mortgage_price:
                option_list.append(monopoly.Option(option_name=f'Lift Mortgage on {self.name}', action=self.lift_mortgage, item_name=self.name, category='liftmortgage'))
        else:
            option_list.append(monopoly.Option(option_name=f'Mortgage {self.name} (Note: This will not permit you to develop {self.name} or enable you to charge rent on it)', action=self.mortgage_owned_property, item_name=self.name, category='mortgageownedproperty'))
            option_list.append(monopoly.Option(option_name=f'Sell {self.name} to the bank for {self.price / 2}', action=self.sell_to_bank, item_name=self.name, category='selltobank'))
        return option_list

    def sell_to_bank(self, game):
        """Sell to Bank removes an OwnableTile from a Player's property holdings and returns it to the Bank"""
        owner = self.find_owner(game=game)
        owner.liquid_holdings += self.price * 0.5
        owner.property_holdings.remove(self)
        game.bank.property_holdings.append(self)

    def complete_transaction(self, buyer, seller, amount, game):
        if self.mortgaged:
            """This is a grey area in the rules.  Normally, amount is just the deed price of the property, however the rules do not specify what happens if
            a mortgaged property is auctioned.  Or if, for that matter, if a mortgaged property can be auctioned.  I'm designing to the spec that a mortgaged property
            can be auctioned and the extra 10% assessed is based off the mortgage price."""
            if amount + 1.1 * self.mortgage_price <= buyer.liquid_holdings:
                immediate_unmortgage_decision = game.interface.get_buy_and_lift_mortgage_decision(buyer=buyer, seller=seller, amount=amount, item=self)
                if immediate_unmortgage_decision:
                    self.mortgaged = False
                    amount = amount + 1.1 * self.mortgage_price
            else:
                amount = amount + 0.1*self.mortgage_price
        if buyer.liquid_holdings < amount:
            return game.run_bankruptcy_process(debtor=buyer, creditor=seller)
        seller.liquid_holdings += amount
        if self in seller.property_holdings:
            seller.property_holdings.remove(self)
            buyer.property_holdings.append(self)
            buyer.liquid_holdings -= amount

    def remove_structure(self, game):
        pass

    def assess_rent(self, owner, game):
        pass


@attr.s
class RailRoadTile(OwnableTile):

    def list_options(self, game):
        option_list = []
        owner = self.find_owner(game=game)
        if owner == game.active_player:
            sell_options = self.list_sell_options(owner=owner)
            option_list += sell_options
            if sell_options and not self.mortgaged and owner.liquid_holdings >= self.possible_structures[0].price:
                option_list.append(monopoly.Option(option_name=f'Build Transtation at {self.name}', action=self.build_train_station, item_name=self.name, category='buildstructure'))
            if self.existing_structures:
                option_list.append(monopoly.Option(option_name=f'Sell Trainstation at {self.name} to the Bank for {0.5*self.existing_structures[0].price}', action=self.remove_structure, item_name=self.existing_structures[0].type, category='removestructure'))
        else:
            if owner == game.bank:
                option_list += self.if_not_owned(active_player=game.active_player)
        return option_list

    def assess_rent(self, owner, game):
        num_owned_railroads = self.count_similar_owned_properties(owner)
        multiplier = 1
        if game.active_player.dealt_card:
            multiplier = 2
        if self.existing_structures:
            rent = multiplier * self.existing_structures[0].rent * 2**(num_owned_railroads - 1)
        else:
            rent = multiplier * self.base_rent * 2**(num_owned_railroads - 1)
        if rent > game.active_player.liquid_holdings:
            game.run_bankruptcy_process(debtor=game.active_player, creditor=owner)
        else:
            owner.liquid_holdings += rent
            game.active_player.liquid_holdings -= rent

    def build_train_station(self, game):
        if game.active_player.liquid_holdings >= self.possible_structures[0].price:
            game.active_player.liquid_holdings -= self.possible_structures[0].price
            self.existing_structures.append(self.possible_structures[0])

    def remove_structure(self, game):
        self.existing_structures = []
        game.active_player.liquid_holdings += self.possible_structures[0].price


@attr.s
class UtilityTile(OwnableTile):

    def list_options(self, game):
        owner = self.find_owner(game=game)
        option_list = []
        if owner == game.active_player:
            option_list += self.list_sell_options(owner=owner)
        else:
            if owner == game.bank:
                option_list += self.if_not_owned(active_player=game.active_player)
        return option_list

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
    color = attr.ib(type=str, default=None)

    def list_options(self, game):
        owner = self.find_owner(game=game)
        option_list = []
        if owner == game.active_player:
            option_list += self.list_sell_options(owner=owner) + self.list_buildable_structures(game=game) + self.list_removable_structures(game=game)
        else:
            if owner == game.bank:
                option_list += self.if_not_owned(active_player=game.active_player)
        return option_list

    def assess_rent(self, game, owner):
        if not self.existing_structures:
            if self.is_color_group_filled(game=game):
                rent = 2 * self.base_rent
            else:
                rent = self.base_rent
        else:
            rent = self.existing_structures[-1].rent
        if rent > game.active_player.liquid_holdings:
            game.run_bankruptcy_process(creditor=owner, debtor=game.active_player)
        else:
            owner.liquid_holdings += rent
            game.active_player.liquid_holdings -= rent

    def list_buildable_structures(self, game):
        if self.is_color_group_filled(game=game):
            struct_tuples = [(tile, len(tile.existing_structures)) for tile in list(filter(lambda x: isinstance(x, ColorTile) and self.color == x.color and len(x.existing_structures) != len(x.possible_structures), game.active_player.property_holdings))]
            if not struct_tuples:
                return []
            else:
                struct_counts = [x[1] for x in struct_tuples]
                option_list = []
                for struct_tuple in struct_tuples:
                    if struct_tuple[1] == min(struct_counts) and struct_tuple[0].possible_structures[struct_tuple[1]].price <= game.active_player.liquid_holdings and struct_tuple[0] == self:
                        option_list.append(monopoly.Option(option_name=f'Build {struct_tuple[0].possible_structures[struct_tuple[1]].type} on {struct_tuple[0].name}', action=self.build_structure, item_name=struct_tuple[0].possible_structures[struct_tuple[1]], category='buildstructure'))
                return option_list
        else:
            return []

    def is_color_group_filled(self, game):
        #Number of each colored tile
        color_group_dict = {'brown': 2, 'cyan': 3, 'pink': 3, 'orange': 3, 'red': 3, 'yellow': 3, 'green': 3, 'blue': 2}
        counter = 0
        for tile in self.find_owner(game=game).property_holdings:
            if isinstance(tile, ColorTile) and tile.color == self.color:
                counter += 1
        return color_group_dict[self.color] == counter

    def list_removable_structures(self, game):
        struct_tuples = [(tile, len(tile.existing_structures)) for tile in list(filter(lambda x: isinstance(x, ColorTile) and self.color == x.color and len(x.existing_structures) > 0,  game.active_player.property_holdings))]
        if not struct_tuples:
            return []
        else:
            struct_counts = [x[1] for x in struct_tuples]
            option_list = []
            for struct_tuple in struct_tuples:
                if struct_tuple[1] == max(struct_counts) and struct_tuple[0] == self:
                    option_list.append(monopoly.Option(option_name=f'Remove {struct_tuple[0].possible_structures[len(struct_tuple[0].existing_structures) - 1].type} on {struct_tuple[0].name}', action=self.remove_structure, item_name=struct_tuple[0].possible_structures[len(struct_tuple[0].existing_structures) - 1], category='removestructure'))
            return option_list

    def build_structure(self, game):
        game.active_player.liquid_holdings -= self.possible_structures[len(self.existing_structures)].price
        self.existing_structures.append(self.possible_structures[len(self.existing_structures)])

    def remove_structure(self, game):
        game.active_player.liquid_holdings += self.possible_structures[len(self.existing_structures) - 1].price / 2
        self.existing_structures.remove(self.existing_structures[-1])


@attr.s
class UnownableTile(Tile):
    pass


@attr.s
class JailTile(UnownableTile):

    def list_options(self, game):
        option_list = []
        if game.active_player.jailed:
            for card in game.active_player.hand:
                if card.name == 'Get out of Jail Free':
                    option_list.append(monopoly.Option(option_name=f'Use {card.name} card from {card.parent_deck}', action=card.action, item_name=card.name, category='useheldcard'))
            if game.active_player.liquid_holdings >= 50:
                option_list.append(monopoly.Option(option_name='Pay Jail Fine ($50)', item_name=None, action=self.pay_jail_fine, category='payjailfine', ends_turn=True))
        if game.active_player.position != self.position:
            option_list += game.board[game.active_player.position].list_options(game=game)
        return option_list

    def perform_auto_actions(self, game):
        if game.active_player.jailed:
            if game.active_player.jailed_turns < 3:
                if game.check_for_doubles():
                    game.active_player.jailed_turns = 0
                    game.active_player.jailed = False
                    game.active_player.advance_position(amount=sum(game.dice_roll))
                    game.board[game.active_player.position].perform_auto_actions(game=game)
                    game.end_current_turn()
                else:
                    game.active_player.jailed_turns += 1
            else:
                self.pay_jail_fine(game=game)

    def pay_jail_fine(self, game):
        game.active_player.liquid_holdings -= 50
        if game.active_player.liquid_holdings < 0:
            self.game.run_bankruptcy_process(debtor=game.active_player, creditor=game.bank)
        else:
            game.active_player.jailed_turns = 0
            game.active_player.jailed = False
            game.active_player.position = sum(game.roll_dice())
            game.board[game.active_player.position].perform_auto_actions(game=game)
            game.end_current_turn()


@attr.s
class CardTile(UnownableTile):
    pass


@attr.s
class ChanceTile(CardTile):

    def perform_auto_actions(self, game):
        game.chance_deck.deal_from_deck(game=game)
        if game.active_player.dealt_card:
            game.active_player.dealt_card.consume_card(game=game)


@attr.s
class CommunityChestTile(CardTile):

    def perform_auto_actions(self, game):
        game.community_deck.deal_from_deck(game=game)
        if game.active_player.dealt_card:
            game.active_player.dealt_card.consume_card(game=game)


@attr.s
class GoToJailTile(UnownableTile):

    def perform_auto_actions(self, game):
        game.active_player.go_directly_to_jail()
        game.board[game.active_player.position].perform_auto_actions(game=game)


@attr.s
class LuxuryTaxTile(UnownableTile):

    def perform_auto_actions(self, game):
        if game.active_player.liquid_holdings >= 75:
            game.active_player.liquid_holdings -= 75
        else:
            game.run_bankruptcy_process(creditor=game.bank, debtor=game.active_player)


@attr.s
class FreeParking(UnownableTile):
    pass


@attr.s
class IncomeTaxTile(UnownableTile):

    def perform_auto_actions(self, game):
        gross_worth = game.active_player.calculate_taxable_assets()
        if gross_worth <= 2000:
            game.active_player.liquid_holdings -= floor(.1 * gross_worth)
        else:
            game.active_player.liquid_holdings -= 200


@attr.s
class GoTile(UnownableTile):

    def perform_auto_actions(self, game):
        game.active_player.pass_go()