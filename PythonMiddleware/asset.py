import json
from .account import Account
from .instance import shared_graphene_instance
from PythonMiddlewarebase import operations
from PythonMiddlewarebase.asset_permissions import whitelist, asset_permissions, force_flag, test_permissions, todict
from .exceptions import AssetDoesNotExistsException


class Asset(dict):
    """ Deals with Assets of the network.

        :param str Asset: Symbol name or object id of an asset
        :param bool lazy: Lazy loading
        :param bool full: Also obtain bitasset-data and dynamic asset dat
        :param graphene.graphene.graphene graphene_instance: graphene instance
        :returns: All data of an asset
        :rtype: dict

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Asset.refresh()``.
    """

    assets_cache = dict()

    def __init__(
        self,
        asset,
        lazy=False,
        full=False,
        graphene_instance=None
    ):
        self.cached = False
        self.full = full
        self.asset = None

        self.graphene = graphene_instance or shared_graphene_instance()

        if isinstance(asset, Asset):
            self.asset = asset.get("symbol")
            super(Asset, self).__init__(asset)
            self.cached = True
            self._cache(asset)
        elif isinstance(asset, str):
            self.asset = asset
            if self.asset in Asset.assets_cache:
                if (
                    not full or (
                        full and "dynamic_asset_data" in
                        Asset.assets_cache[self.asset])):
                    super(Asset, self).__init__(Asset.assets_cache[self.asset])
                else:
                    self.refresh()
                self.cached = True
            elif not lazy and not self.cached:
                self.refresh()
                self.cached = True
        else:
            raise ValueError("Asset() expects a symbol, id or an instance of Asset")

    def refresh(self):
        """ Refresh the data from the API server
        """
        asset = self.graphene.rpc.get_asset(self.asset)
        if not asset:
            raise AssetDoesNotExistsException
        super(Asset, self).__init__(asset)
        if self.full:
            if self.is_bitasset:
                self["bitasset_data"] = self.graphene.rpc.get_object(asset["bitasset_data_id"])
            self["dynamic_asset_data"] = self.graphene.rpc.get_object(asset["dynamic_asset_data_id"])

        # Permissions and flags
        self["permissions"] = todict(asset["options"].get("issuer_permissions"))
        self["flags"] = todict(asset["options"].get("flags"))
        try:
            self["description"] = json.loads(asset["options"]["description"])
        except:
            self["description"] = asset["options"]["description"]

        self.cached = True
        self._cache(asset)

    def _cache(self, asset):
        # store in cache
        Asset.assets_cache[asset["symbol"]] = asset

    @property
    def is_bitasset(self):
        """ Is the asset a :doc:`mpa`?
        """
        return ("bitasset_data_id" in self)

    @property
    def permissions(self):
        """ List the permissions for this asset that the issuer can obtain
        """
        return self["permissions"]

    @property
    def flags(self):
        """ List the permissions that are currently used (flags)
        """
        return self["flags"]

    def ensure_full(self):
        if not self.full:
            self.full = True
            self.refresh()

    @property
    def feeds(self):
        from .price import PriceFeed
        self.ensure_full()
        if not self.is_bitasset:
            return
        r = []
        for feed in self["bitasset_data"]["feeds"]:
            r.append(PriceFeed(feed))
        return r

    @property
    def feed(self):
        from .price import PriceFeed
        assert self.is_bitasset
        self.ensure_full()
        return PriceFeed(self["bitasset_data"]["current_feed"])

    @property
    def calls(self):
        return self.get_call_orders(10)

    def get_call_orders(self, limit=100):
        from .price import Price
        from .amount import Amount
        assert limit <= 100
        assert self.is_bitasset
        self.ensure_full()
        r = list()
        bitasset = self["bitasset_data"]
        settlement_price = Price(bitasset["current_feed"]["settlement_price"])
        ret = self.graphene.rpc.get_call_orders(self["id"], limit)
        for call in ret[:limit]:
            call_price = Price(call["call_price"])
            collateral_amount = Amount(
                {
                    "amount": call["collateral"],
                    "asset_id": call["call_price"]["base"]["asset_id"]
                },
                graphene_instance=self.graphene
            )
            debt_amount = Amount(
                {
                    "amount": call["debt"],
                    "asset_id": call["call_price"]["quote"]["asset_id"],
                },
                graphene_instance=self.graphene
            )
            r.append({
                "account": Account(
                    call["borrower"],
                    lazy=True,
                    graphene_instance=self.graphene
                ),
                "collateral": collateral_amount,
                "debt": debt_amount,
                "call_price": call_price,
                "settlement_price": settlement_price,
                "ratio": float(collateral_amount) / float(debt_amount) * float(settlement_price)
            })
        return r

    @property
    def settlements(self):
        return self.get_settle_orders(10)

    def get_settle_orders(self, limit=100):
        from .amount import Amount
        from .utils import formatTimeString
        assert limit <= 100
        assert self.is_bitasset
        r = list()
        ret = self.graphene.rpc.get_settle_orders(self["id"], limit)
        for settle in ret[:limit]:
            r.append({
                "account": Account(
                    settle["owner"],
                    lazy=True,
                    graphene_instance=self.graphene
                ),
                "amount": Amount(settle["balance"],
                    graphene_instance=self.graphene),
                "date": formatTimeString(settle["settlement_date"])
            })
        return r

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Asset, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Asset, self).items()

    def __repr__(self):
        return "<Asset %s>" % str(self.asset)

    def halt(self,lockMarket=True):
        """ Halt this asset from being moved or traded
        """
        nullaccount = Account("null-account")  # We set the null-account
        flags = {"white_list": True,
                 "transfer_restricted": True,
                 }
        options = self["options"]
        test_permissions(options["issuer_permissions"], flags)
        flags_int = force_flag(options["flags"], flags)
        if lockMarket:
            options.update({
                "flags": flags_int,
                "whitelist_authorities": [self["issuer"],"1.2.6","1.2.7"],
                "blacklist_authorities": [],
                "whitelist_markets": [self["id"]],
                "blacklist_markets": [],
            })
        else:
            options.update({
                "flags": flags_int,
                "whitelist_authorities": [self["issuer"],"1.2.6","1.2.7"],
                "blacklist_authorities": [],
                "whitelist_markets": [],
                "blacklist_markets": [],
            })

        op = operations.Asset_update(**{
            "fee": {"amount": 0,
                    "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def release(
        self,
        whitelist_authorities=[],
        blacklist_authorities=[],
        whitelist_markets=[],
        blacklist_markets=[],
    ):
        """ Release this asset and allow unrestricted transfer, trading,
            etc.

            :param list whitelist_authorities: List of accounts that serve as whitelist authorities
            :param list blacklist_authorities: List of accounts that serve as blacklist authorities
            :param list whitelist_markets: List of assets to allow trading with
            :param list blacklist_markets: List of assets to prevent trading with
        """
        flags = {"white_list": False,
                 "transfer_restricted": False,
                 }
        options = self["options"]
        test_permissions(options["issuer_permissions"], flags)
        flags_int = force_flag(options["flags"], flags)
        options.update({
            "flags": flags_int,
            "whitelist_authorities": [
                Account(a)["id"] for a in whitelist_authorities
            ],
            "blacklist_authorities": [
                Account(a)["id"] for a in blacklist_authorities
            ],
            "whitelist_markets": [
                Asset(a)["id"] for a in whitelist_markets
            ],
            "blacklist_markets": [
                Asset(a)["id"] for a in blacklist_markets
            ],
        })
        op = operations.Asset_update(**{
            "fee": {"amount": 0,
                    "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def setoptions(self, flags):
        """ Enable a certain flag.

            Flags:

             * charge_market_fee
             * white_list
             * override_authority
             * transfer_restricted
             * disable_force_settle
             * global_settle
             * disable_confidential
             * witness_fed_asset
             * committee_fed_asset

            :param dict flag: dictionary of flags and boolean
        """
        assert set(flags.keys()).issubset(asset_permissions.keys()), "unknown flag"

        options = self["options"]
        test_permissions(options["issuer_permissions"], flags)
        flags_int = force_flag(options["flags"], flags)
        options.update({"flags": flags_int})
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def enableflag(self, flag):
        """ Enable a certain flag.

            :param str flag: Flag name
        """
        return self.setoptions({flag: True})

    def disableflag(self, flag):
        """ Enable a certain flag.

            :param str flag: Flag name
        """
        return self.setoptions({flag: False})

    def seize(self, from_account, to_account, amount):
        """ Seize amount from an account and send to another

            ... note:: This requires the ``override_authority`` to be
                       set for this asset!

            :param graphene.account.Account from_account: From this account
            :param graphene.account.Account to_account: To this account
            :param graphene.amount.Amount amount: Amount to seize
        """

        options = self["options"]
        if not (options["flags"] & asset_permissions["override_authority"]):
            raise Exception("Insufficient Permissions/flags for seizure!")

        op = operations.Override_transfer(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "from": from_account["id"],
            "to": to_account["id"],
            "amount": amount.json(),
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def add_authorities(self, type, authorities=[]):
        """ Add authorities to an assets white/black list

            :param str type: ``blacklist`` or ``whitelist``
            :param list authorities: List of authorities (Accounts)
        """
        assert type in ["blacklist", "whitelist"]
        assert isinstance(authorities, (list, set))

        options = self["options"]
        if type == "whitelist":
            options["whitelist_authorities"].extend([
                Account(a)["id"] for a in authorities
            ])
        if type == "blacklist":
            options["blacklist_authorities"].extend([
                Account(a)["id"] for a in authorities
            ])
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def remove_authorities(self, type, authorities=[]):
        """ Remove authorities from an assets white/black list

            :param str type: ``blacklist`` or ``whitelist``
            :param list authorities: List of authorities (Accounts)
        """
        assert type in ["blacklist", "whitelist"]
        assert isinstance(authorities, (list, set))

        options = self["options"]
        if type == "whitelist":
            for a in authorities:
                options["whitelist_authorities"].remove(
                    Account(a)["id"]
                )
        if type == "blacklist":
            for a in authorities:
                options["blacklist_authorities"].remove(
                    Account(a)["id"]
                )
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def add_markets(self, type, authorities=[], force_enable=True):
        """ Add markets to an assets white/black list

            :param str type: ``blacklist`` or ``whitelist``
            :param list markets: List of markets (assets)
            :param bool force_enable: Force enable ``white_list`` flag
        """
        assert type in ["blacklist", "whitelist"]
        assert isinstance(authorities, (list, set))

        options = self["options"]
        if force_enable:
            test_permissions(
                options["issuer_permissions"],
                {"white_list": True}
            )
            flags_int = force_flag(
                options["flags"],
                {"white_list": True}
            )
            options.update({"flags": flags_int})
        else:
            assert test_permissions(
                options["flags"],
                ["white_list"]
            ), "whitelist feature not enabled"

        if type == "whitelist":
            options["whitelist_markets"].extend([
                Asset(a)["id"] for a in authorities
            ])
        if type == "blacklist":
            options["blacklist_markets"].extend([
                Asset(a)["id"] for a in authorities
            ])
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def remove_markets(self, type, authorities=[]):
        """ Remove markets from an assets white/black list

            :param str type: ``blacklist`` or ``whitelist``
            :param list markets: List of markets (assets)
        """
        assert type in ["blacklist", "whitelist"]
        assert isinstance(authorities, (list, set))

        options = self["options"]
        if type == "whitelist":
            for a in authorities:
                options["whitelist_markets"].remove(
                    Asset(a)["id"]
                )
        if type == "blacklist":
            for a in authorities:
                options["blacklist_markets"].remove(
                    Asset(a)["id"]
                )
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def set_market_fee(self, percentage_fee, max_market_fee):
        """ Set trading percentage fee

            :param float percentage_fee: Percentage of fee
            :param graphene.amount.Amount max_market_fee: Max Fee
        """
        assert percentage_fee <= 100 and percentage_fee > 0
        flags = {"charge_market_fee": percentage_fee > 0}
        options = self["options"]
        test_permissions(options["issuer_permissions"], flags)
        flags_int = force_flag(options["flags"], flags)
        options.update({
            "flags": flags_int,
            "market_fee_percent": percentage_fee * 100,
            "max_market_fee": int(max_market_fee),
        })
        op = operations.Asset_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_options": options,
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")

    def update_feed_producers(self, producers):
        """ Update bitasset feed producers

            :param list producers: List of accounts that are allowed to produce a feed
        """
        assert self.is_bitasset, "Asset needs to be a bitasset/market pegged asset"
        op = operations.Asset_update_feed_producers(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "asset_to_update": self["id"],
            "new_feed_producers": [
                Account(a)["id"] for a in producers
            ],
            "extensions": []
        })
        return self.graphene.finalizeOp(op, self["issuer"], "active")
