import json
from collections import OrderedDict
from .types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional,Static_variant,
    Map, Id, VoteId,
    ObjectId as GPHObjectId
)
from .baseobjects import GrapheneObject, isArgsThisClass
from .chains import known_chains, default_prefix
from .objecttypes import object_type
from .account import PublicKey
from .baseobjects import Operation as GPHOperation
from .operationids import operations
from PythonMiddleware.storage import configStorage as config
# default_prefix = config["default_prefix"]

class ExtensionsData(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('id', String(kwargs["id"])),
                ('data', kwargs["data"]),
            ]))


# class Chain_parameters(GrapheneObject):
#     def __init__(self, *args, **kwargs):
#         if isArgsThisClass(self, args):
#             self.data = args[0].data
#         else:
#             if len(args) == 1 and len(kwargs) == 0:
#                 kwargs = args[0]
#             super().__init__(OrderedDict([
#                 ('block_interval', Uint32(kwargs["block_interval"])),
#                 ('maintenance_interval', Uint32(kwargs["maintenance_interval"])),
#                 ('maintenance_skip_slots', Uint8(kwargs["maintenance_skip_slots"])),
#                 ('committee_proposal_review_period', Uint32(kwargs["committee_proposal_review_period"])),
#                 ('maximum_transaction_size', Uint32(kwargs["maximum_transaction_size"])),
#                 ('maximum_block_size', Uint32(kwargs["maximum_block_size"])),
#                 ('maximum_time_until_expiration', Uint32(kwargs["maximum_time_until_expiration"])),
#                 ('maximum_proposal_lifetime', Uint32(kwargs["maximum_proposal_lifetime"])),
#                 ('maximum_asset_whitelist_authorities', Uint8(kwargs["maximum_asset_whitelist_authorities"])),
#                 ('maximum_asset_feed_publishers', Uint8(kwargs["maximum_asset_feed_publishers"]))
#             ]))


class transaction_id_type(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('block_num', String(kwargs["block_num"])),
                ('trx_num', kwargs["trx_num"]),
            ]))
            
class ObjectId(GPHObjectId): 
    """ Encodes object/protocol ids
    """
    def __init__(self, object_str, type_verify=None):
        if len(object_str.split(".")) == 3:
            space, type, id = object_str.split(".")
            self.space = int(space)
            self.type = int(type)
            self.instance = Id(int(id))
            self.Id = object_str
            if type_verify:
                assert object_type[type_verify] == int(type),\
                    "Object id does not match object type! " +\
                    "Excpected %d, got %d" %\
                    (object_type[type_verify], int(type))
        else:
            raise Exception("Object id is invalid")


class Operation(GPHOperation):
    def __init__(self, *args, **kwargs):
        super(Operation, self).__init__(*args, **kwargs)

    def _getklass(self, name):
        module = __import__("PythonMiddlewarebase.operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_

    def operations(self):
        return operations

    def getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in operations:
            if int(operations[key]) is int(i):
                return key
        return "Unknown Operation ID %d" % i

    def json(self):
        return json.loads(str(self))


class Asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('amount', Int64(kwargs["amount"])),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset"))
            ]))


class Memo(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "message" in kwargs and kwargs["message"]:
                if "chain" not in kwargs:
                    chain = default_prefix
                else:
                    chain = kwargs["chain"]
                if isinstance(chain, str) and chain in known_chains:
                    chain_params = known_chains[chain]
                elif isinstance(chain, dict):
                    chain_params = chain
                else:
                    raise Exception("Memo() only takes a string or a dict as chain!")
                if "prefix" not in chain_params:
                    raise Exception("Memo() needs a 'prefix' in chain params!")
                prefix = chain_params["prefix"]
                super().__init__(OrderedDict([
                    ('from', PublicKey(kwargs["from"], prefix=prefix)),
                    ('to', PublicKey(kwargs["to"], prefix=prefix)),
                    ('nonce', Uint64(int(kwargs["nonce"]))),
                    ('message', Bytes(kwargs["message"]))
                ]))
            else:
                super().__init__(None)


class Price(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('base', Asset(kwargs["base"])),
                ('quote', Asset(kwargs["quote"]))
            ]))


class PriceFeed(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('settlement_price', Price(kwargs["settlement_price"])),
                ('maintenance_collateral_ratio', Uint16(kwargs["maintenance_collateral_ratio"])),
                ('maximum_short_squeeze_ratio', Uint16(kwargs["maximum_short_squeeze_ratio"])),
                ('core_exchange_rate', Price(kwargs["core_exchange_rate"])),
            ]))


class Permission(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.pop("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort keys (FIXME: ideally, the sorting is part of Public
            # Key and not located here)
            kwargs["key_auths"] = sorted(
                kwargs["key_auths"],
                key=lambda x: repr(PublicKey(x[0], prefix=prefix).address),
                reverse=False,
            )
            accountAuths = Map([
                [ObjectId(e[0], "account"), Uint16(e[1])]
                for e in kwargs["account_auths"]
            ])
            keyAuths = Map([
                [PublicKey(e[0], prefix=prefix), Uint16(e[1])]
                for e in kwargs["key_auths"]
            ])
            super().__init__(OrderedDict([
                ('weight_threshold', Uint32(int(kwargs["weight_threshold"]))),
                ('account_auths', accountAuths),
                ('key_auths', keyAuths),
                ('extensions', Set([])),
            ]))


class AccountOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        prefix = kwargs.pop("prefix", default_prefix)
        
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # remove dublicates
            kwargs["votes"] = list(set(kwargs["votes"]))
            # Sort votes
            kwargs["votes"] = sorted(
                kwargs["votes"],
                key=lambda x: float(x.split(":")[1]),
            )
            votes=Array([VoteId(o) for o in kwargs["votes"]])
            extensions=Array([String(o) for o in kwargs["extensions"]])
            super().__init__(OrderedDict([
                ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
                ('voting_account', ObjectId(kwargs["voting_account"], "account")),
                ('num_witness', Uint16(kwargs["num_witness"])),
                ('num_committee', Uint16(kwargs["num_committee"])),
                ('votes', votes),
                ('extensions', extensions),
                #('extensions', Set([])),
            ]))


class AssetOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sorting
            for key in [
                "whitelist_authorities",
                "blacklist_authorities",
                "whitelist_markets",
                "blacklist_markets"
            ]:
                kwargs[key] = sorted(
                    set(kwargs[key]),
                    key=lambda x: int(x.split(".")[2]),
                )

            super().__init__(OrderedDict([
                ('max_supply', Uint64(kwargs["max_supply"])),
                ('market_fee_percent', Uint16(kwargs["market_fee_percent"])),
                ('max_market_fee', Uint64(kwargs["max_market_fee"])),
                ('issuer_permissions', Uint16(kwargs["issuer_permissions"])),
                ('flags', Uint16(kwargs["flags"])),
                ('core_exchange_rate', Price(kwargs["core_exchange_rate"])),
                ('whitelist_authorities',
                    Array([ObjectId(o, "account") for o in kwargs["whitelist_authorities"]])),
                ('blacklist_authorities',
                    Array([ObjectId(o, "account") for o in kwargs["blacklist_authorities"]])),
                ('whitelist_markets',
                    Array([ObjectId(o, "asset") for o in kwargs["whitelist_markets"]])),
                ('blacklist_markets',
                    Array([ObjectId(o, "asset") for o in kwargs["blacklist_markets"]])),
                ('description', String(kwargs["description"])),
                ('extensions', Set([])),
            ]))


class BitassetOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
        super().__init__(OrderedDict([
            ("feed_lifetime_sec", Uint32(kwargs.get("feed_lifetime_sec", 60*60*24))),
            ("minimum_feeds", Uint8(kwargs.get("minimum_feeds", 1))),
            ("force_settlement_delay_sec", Uint32(kwargs.get("force_settlement_delay_sec", 60*60*24))),
            ("force_settlement_offset_percent", Uint16(kwargs.get("force_settlement_offset_percent", 0))),
            ("maximum_force_settlement_volume", Uint16(kwargs.get("maximum_force_settlement_volume", 2000))),
            ("short_backing_asset", ObjectId(kwargs.get("short_backing_asset", "1.3.0"), "asset")),
            ("extensions", Set([]))
        ]))


class Vesting_balance_worker_initializer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('pay_vesting_period_days', Uint16(kwargs["pay_vesting_period_days"])),
            ]))


class Burn_worker_initializer(GrapheneObject):
    def __init__(self, kwargs):
        super().__init__(OrderedDict([]))


class Refund_worker_initializer(GrapheneObject):
    def __init__(self, kwargs):
        super().__init__(OrderedDict([]))


class Worker_initializer(Static_variant):
    def __init__(self, o):
        id = o[0]
        if id == 0:
            data = Refund_worker_initializer(o[1])
        elif id == 1:
            data = Vesting_balance_worker_initializer(o[1])
        elif id == 2:
            data = Burn_worker_initializer(o[1])
        else:
            raise Exception("Unknown Worker_initializer")
        super().__init__(data, id)


class Linear_vesting_policy_initializer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('begin_timestamp', PointInTime(kwargs["begin_timestamp"])),
                ('vesting_cliff_seconds', Uint32(kwargs.get("vesting_cliff_seconds", 0))),
                ('vesting_duration_seconds', Uint32(kwargs.get("vesting_duration_seconds", 0))),
            ]))


class Cdd_vesting_policy_initializer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('start_claim', PointInTime(kwargs["start_claim"])),
                ('vesting_seconds', Uint32(kwargs.get("vesting_seconds", 0))),
            ]))


class Vesting_policy_initializer(Static_variant):
    def __init__(self, o):
        id = o[0]
        if id == 0:
            data = Linear_vesting_policy_initializer(o[1])
        elif id == 1:
            data = Cdd_vesting_policy_initializer(o[1])
        else:
            raise Exception("Unknown Vesting_policy_initializer")
        super().__init__(data, id)


class Int(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('baseValue', Uint16(kwargs["baseValue"]))
            ]))


class Number(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('baseValue', float(kwargs["baseValue"]))
            ]))


class Lua_String(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('baseValue', String(kwargs["baseValue"]))
            ]))


class Lua_Bool(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('baseValue', Bool(kwargs["baseValue"]))
            ]))


class Table(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('baseValue', Array([o for o in kwargs["baseValue"]]))
            ]))


class Function(GrapheneObject):
    def __init__(self, *args, **kwargs):
        super().__init__(OrderedDict([]))


class Lua(Static_variant):
    def __init__(self, o):
        id = o[0]
        print("id", id)
        print("o[1]", o[1])
        if id == 0:
            data = Int(o[1])
        elif id == 1:
            data = Number(o[1])
        elif id == 2:
            data = Lua_String(o[1])
        elif id == 3:
            data = Lua_Bool(o[1])
        elif id == 4:
            data = Table(o[1])
        elif id == 5:
            data = Function(o[1])
        else:
            raise ValueError("Unknown Lua_type")
        super().__init__(data, id)


