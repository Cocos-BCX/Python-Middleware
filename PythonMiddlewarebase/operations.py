from collections import OrderedDict
import json
from .types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId, Pair
)
from .objects import GrapheneObject, isArgsThisClass
from .account import PublicKey
from .chains import default_prefix
from .operationids import operations
from .objects import (
    Operation,
    Asset,
    Memo,
    Price,
    PriceFeed,
    Permission,
    AccountOptions,
    AssetOptions,
    BitassetOptions,
    ObjectId,
    Worker_initializer,
    Vesting_policy_initializer,
    Lua
)

from PythonMiddleware.storage import configStorage as config
# default_prefix = config["default_prefix"]


def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i


class Transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs and kwargs["memo"]:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            if "extensions" in kwargs and kwargs["extensions"]:
                super().__init__(OrderedDict([
                    
                    ('from', ObjectId(kwargs["from"], "account")),
                    ('to', ObjectId(kwargs["to"], "account")),
                    ('amount', Asset(kwargs["amount"])),
                    ('memo', memo),
                    ('extensions', Array([String(o) for o in kwargs["extensions"]])),
                ]))
            else:
                super().__init__(OrderedDict([
                    
                    ('from', ObjectId(kwargs["from"], "account")),
                    ('to', ObjectId(kwargs["to"], "account")),
                    ('amount', Asset(kwargs["amount"])),
                    ('memo', memo),
                    ('extensions', Set([])),
                ]))


class Limit_order_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('amount_to_sell', Asset(kwargs["amount_to_sell"])),
                ('min_to_receive', Asset(kwargs["min_to_receive"])),
                ('expiration', PointInTime(kwargs["expiration"])),
                ('fill_or_kill', Bool(kwargs["fill_or_kill"])),
                ('extensions', Set([])),
            ]))


class Limit_order_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('order', ObjectId(kwargs["order"], "limit_order")),
                ('extensions', Set([])),
            ]))


class Call_order_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('funding_account', ObjectId(kwargs["funding_account"], "account")),
                ('delta_collateral', Asset(kwargs["delta_collateral"])),
                ('delta_debt', Asset(kwargs["delta_debt"])),
                ('extensions', Set([])),
            ]))


class Account_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(OrderedDict([
                ('registrar', ObjectId(kwargs["registrar"], "account")),
                ('name', String(kwargs["name"])),
                ('owner', Permission(kwargs["owner"], prefix=prefix)),
                ('active', Permission(kwargs["active"], prefix=prefix)),
                ('options', AccountOptions(kwargs["options"], prefix=prefix)),
                ('extensions', Set([])),
            ]))


class Account_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            if "owner" in kwargs:
                owner = Optional(Permission(kwargs["owner"], prefix=prefix))
            else:
                owner = Optional(None)

            if "active" in kwargs:
                active = Optional(Permission(kwargs["active"], prefix=prefix))
            else:
                active = Optional(None)

            if "new_options" in kwargs:
                options = Optional(AccountOptions(kwargs["new_options"], prefix=prefix))
            else:
                options = Optional(None)

            if "lock_with_vote" in kwargs:
                lock_with_vote = Optional(Pair(Uint32(kwargs["lock_with_vote"][0]), Asset(kwargs["lock_with_vote"][1])))
            else:
                lock_with_vote = Optional(None)

            super().__init__(OrderedDict([
                # ('lock_with_vote',Asset(kwargs["lock_with_vote"])),
                ('lock_with_vote', lock_with_vote),
                ('account', ObjectId(kwargs["account"], "account")),
                ('owner', owner),
                ('active', active),
                ('new_options', options),
                ('extensions', Set([])),
            ]))


class Account_whitelist(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                
                ('authorizing_account', ObjectId(kwargs["authorizing_account"], "account")),
                ('account_to_list', ObjectId(kwargs["account_to_list"], "account")),
                ('new_listing', Uint8(kwargs["new_listing"])),
                ('extensions', Set([])),
            ]))


class Account_upgrade(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('account_to_upgrade', ObjectId(kwargs["account_to_upgrade"], "account")),
                ('upgrade_to_lifetime_member', Bool(kwargs["upgrade_to_lifetime_member"])),
                ('extensions', Set([])),
            ]))


class Asset_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "bitasset_opts" in kwargs and kwargs["bitasset_opts"] != None:
                bitasset_opts = Optional(BitassetOptions(kwargs["bitasset_opts"]))
            else:
                bitasset_opts = Optional(None)
            super().__init__(OrderedDict([
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('symbol', String(kwargs["symbol"])),
                ('precision', Uint8(kwargs["precision"])),
                ('common_options', AssetOptions(kwargs["common_options"])),
                ('bitasset_opts', bitasset_opts),
                ('extensions', Set([]))
            ]))


class Asset_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if "new_issuer" in kwargs:
                new_issuer = Optional(ObjectId(kwargs["new_issuer"], "account"))
            else:
                new_issuer = Optional(None)
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_update', ObjectId(kwargs["asset_to_update"], "asset")),
                ('new_issuer', new_issuer),
                ('new_options', AssetOptions(kwargs["new_options"])),
                ('extensions', Set([])),
            ]))


class Update_collateral_for_gas(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('mortgager', ObjectId(kwargs["mortgager"], "account")),
                ('beneficiary', ObjectId(kwargs["beneficiary"], "account")),
                ('collateral', Int64(kwargs["collateral"])),
            ]))


class Asset_update_bitasset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_update', ObjectId(kwargs["asset_to_update"], "asset")),
                ('new_options', BitassetOptions(kwargs["new_options"])),
                ('extensions', Set([])),
            ]))


class Asset_update_feed_producers(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            kwargs["new_feed_producers"] = sorted(
                kwargs["new_feed_producers"],
                key=lambda x: float(x.split(".")[2]),
            )

            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_update', ObjectId(kwargs["asset_to_update"], "asset")),
                ('new_feed_producers',
                    Array([ObjectId(o, "account") for o in kwargs["new_feed_producers"]])),
                ('extensions', Set([])),
            ]))


class Asset_issue(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs and kwargs["memo"]:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_issue', Asset(kwargs["asset_to_issue"])),
                ('issue_to_account', ObjectId(kwargs["issue_to_account"], "account")),
                ('memo', memo),
                ('extensions', Set([]))
            ]))


class Asset_reserve(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                
                ('payer', ObjectId(kwargs["payer"], "account")),
                ('amount_to_reserve', Asset(kwargs["amount_to_reserve"])),
                ('extensions', Set([])),
            ]))


class Asset_fund_fee_pool(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('from_account', ObjectId(kwargs["from_account"], "account")),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset")),
                ('amount', Int64(kwargs["amount"])),
                ('extensions', Set([])),
            ]))


class Asset_settle(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('account', ObjectId(kwargs["account"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('extensions', Set([]))
            ]))


class Asset_settle_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('settlement', ObjectId(kwargs["settlement"], "force_settlement")),
                ('account', ObjectId(kwargs["account"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('extensions', Set([]))
            ]))


class Asset_global_settle(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_settle', ObjectId(kwargs["asset_to_settle"], "asset")),
                ('settle_price', Price(kwargs["settle_price"])),
                ('extensions', Set([]))
            ]))


class Asset_publish_feed(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('publisher', ObjectId(kwargs["publisher"], "account")),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset")),
                ('feed', PriceFeed(kwargs["feed"])),
                ('extensions', Set([])),
            ]))


class Asset_update_restricted(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('payer', ObjectId(kwargs["payer"], "account")),
                ('target_asset', ObjectId(kwargs["target_asset"], "asset")),
                ('isadd', Bool(kwargs['isadd'])),
                ('restricted_type', Uint8(kwargs["restricted_type"])),
                ('restricted_list', Array([ObjectId(o) for o in kwargs["restricted_list"]])),
                ('extensions', Set([])),
            ]))


class Witness_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # if "url" in kwargs and kwargs["url"]:
            #     url = Optional(String(kwargs["url"]))
            # else:
            #     url = Optional(String(""))
            if "prefix" not in kwargs:
                prefix = kwargs.get("prefix", default_prefix)
            else:
                prefix = kwargs["prefix"]
            
            if "block_signing_key" in kwargs and kwargs["block_signing_key"]:
                block_signing_key = PublicKey(kwargs["block_signing_key"],prefix=prefix)
            super().__init__(OrderedDict([
                ('witness_account', ObjectId(kwargs["witness_account"], "account")),
                ('url', String(kwargs["url"])),
                ('block_signing_key', block_signing_key),
            ]))


class Witness_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_url" in kwargs and kwargs["new_url"]:
                new_url = Optional(String(kwargs["new_url"]))
            else:
                new_url = Optional(None)

            if "new_signing_key" in kwargs and kwargs["new_signing_key"]:
                new_signing_key = Optional(PublicKey(kwargs["new_signing_key"]))
            else:
                new_signing_key = Optional(None)

            super().__init__(OrderedDict([
                
                ('witness', ObjectId(kwargs["witness"], "witness")),
                ('witness_account', ObjectId(kwargs["witness_account"], "account")),
                ('new_url', new_url),
                ('new_signing_key', new_signing_key),
                ('work_status', Bool(kwargs["work_status"]))
            ]))


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('op', Operation(kwargs["op"])),
            ]))


class Proposal_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "review_period_seconds" in kwargs and kwargs["review_period_seconds"]:
                review = Optional(Uint32(kwargs["review_period_seconds"]))
            else:
                review = Optional(None)
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('expiration_time', PointInTime(kwargs["expiration_time"])),
                ('proposed_ops', Array([Op_wrapper(o) for o in kwargs["proposed_ops"]])),
                ('review_period_seconds', review),
                ('extensions', Set([])),
            ]))


class Proposal_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            for o in ['active_approvals_to_add',
                      'active_approvals_to_remove',
                      'owner_approvals_to_add',
                      'owner_approvals_to_remove',
                      'key_approvals_to_add',
                      'key_approvals_to_remove']:
                if o not in kwargs:
                    kwargs[o] = []

            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('proposal', ObjectId(kwargs["proposal"], "proposal")),
                ('active_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_add"]])),
                ('active_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_remove"]])),
                ('owner_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_add"]])),
                ('owner_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_remove"]])),
                ('key_approvals_to_add',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_add"]])),
                ('key_approvals_to_remove',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_remove"]])),
                ('extensions', Set([])),
            ]))


class Proposal_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('using_owner_authority', Bool(kwargs.get("using_owner_authority", False))),
                ('proposal', ObjectId(kwargs["proposal"], "proposal")),
                ('extensions', Set([]))
            ]))


class Withdraw_permission_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('withdraw_from_account', ObjectId(kwargs["withdraw_from_account"], "account")),
                ('authorized_account', ObjectId(kwargs["authorized_account"], "account")),
                ('withdrawal_limit', Asset(kwargs["withdrawal_limit"])),
                ('withdrawal_period_sec', Uint32(kwargs.get("withdrawal_period_sec", 0))),
                ('periods_until_expiration', Uint32(kwargs.get("periods_until_expiration", 0))),
                ('period_start_time', PointInTime(kwargs["period_start_time"]))
            ]))


class Withdraw_permission_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('withdraw_from_account', ObjectId(kwargs["withdraw_from_account"], "account")),
                ('authorized_account', ObjectId(kwargs["authorized_account"], "account")),
                ('permission_to_update', ObjectId(kwargs["permission_to_update"], "withdraw_permission")),
                ('withdrawal_limit', Asset(kwargs["withdrawal_limit"])),
                ('withdrawal_period_sec', Uint32(kwargs.get("withdrawal_period_sec", 0))),
                ('period_start_time', PointInTime(kwargs["period_start_time"])),
                ('periods_until_expiration', Uint32(kwargs.get("periods_until_expiration", 0)))
            ]))


class Withdraw_permission_claim(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs and kwargs["memo"]:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                
                ('withdraw_permission', ObjectId(kwargs["withdraw_permission"], "withdraw_permission")),
                ('withdraw_from_account', ObjectId(kwargs["withdraw_from_account"], "account")),
                ('withdraw_to_account', ObjectId(kwargs["withdraw_to_account"], "account")),
                ('amount_to_withdraw', Asset(kwargs["amount_to_withdraw"])),
                ('memo', memo)
            ]))


class Withdraw_permission_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('withdraw_from_account', ObjectId(kwargs["withdraw_from_account"], "account")),
                ('authorized_account', ObjectId(kwargs["authorized_account"], "account")),
                ('withdrawal_permission', ObjectId(kwargs["withdrawal_permission"], "withdraw_permission")),
            ]))


class Committee_member_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # if "url" in kwargs and kwargs["url"]:
            #     url = Optional(String(kwargs["url"]))
            # else:
            #     url = Optional(String(""))
            super().__init__(OrderedDict([
                
                ('committee_member_account', ObjectId(kwargs["committee_member_account"], "account")),
                ('url', String(kwargs["url"]))
            ]))


class Committee_member_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_url" in kwargs and kwargs["new_url"]:
                new_url = Optional(String(kwargs["new_url"]))
            else:
                new_url = Optional(None)
            super().__init__(OrderedDict([
                
                ('committee_member', ObjectId(kwargs["committee_member"], "committee_member")),
                ('committee_member_account', ObjectId(kwargs["committee_member_account"], "account")),
                ('new_url', new_url),
                ('work_status', Bool(kwargs["work_status"]))
            ]))


class Committee_member_update_global_parameters(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                # ('new_parameters', )
            ]))


class Vesting_balance_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                
                ('creator', ObjectId(kwargs["creator"], "account")),
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('policy', Vesting_policy_initializer(kwargs["policy"]))
            ]))


class Vesting_balance_withdraw(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                
                ('vesting_balance', ObjectId(kwargs["vesting_balance"], "vesting_balance")),
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('amount', Asset(kwargs["amount"])),
            ]))


class Worker_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "beneficiary" in kwargs and kwargs["beneficiary"]:
                beneficiary = Optional(ObjectId(kwargs["beneficiary"], "account"))
            else:
                beneficiary = Optional(None)

            super().__init__(OrderedDict([
                ('beneficiary', beneficiary),
                ('work_begin_date', PointInTime(kwargs["work_begin_date"])),
                ('work_end_date', PointInTime(kwargs["work_end_date"])),
                ('daily_pay', Uint64(kwargs["daily_pay"])),
                ('name', String(kwargs["name"])),
                ('describe', String(kwargs["describe"])),
                ('initializer', Worker_initializer(kwargs["initializer"])),
            ]))


class Balance_claim(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            super().__init__(OrderedDict([
                
                ('deposit_to_account', ObjectId(kwargs["deposit_to_account"], "account")),
                ('balance_to_claim', ObjectId(kwargs["balance_to_claim"], "balance")),
                ('balance_owner_key', PublicKey(kwargs["balance_owner_key"], prefix=prefix)),
                ('total_claimed', Asset(kwargs["total_claimed"]))
            ]))


class Asset_claim_fees(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('amount_to_claim', Asset(kwargs["amount_to_claim"])),
                ('extensions', Set([]))
            ]))


class Bid_collateral(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('bidder', ObjectId(kwargs["bidder"], "account")),
                ('additional_collateral', Asset(kwargs["additional_collateral"])),
                ('debt_covered', Asset(kwargs["debt_covered"])),
                ('extensions', Set([]))
            ]))


class Contract_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "prefix" not in kwargs:
                prefix = kwargs.get("prefix", default_prefix)
            else:
                prefix = kwargs["prefix"]
            if "contract_authority" in kwargs and kwargs["contract_authority"]:
                contract_authority = PublicKey(kwargs["contract_authority"], prefix=prefix)
            super().__init__(OrderedDict([
                
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('name', String(kwargs["name"])),
                ('data', String(kwargs["data"])),
                ('contract_authority', contract_authority),
                ('extensions', Set([]))
            ]))


class Call_contract_function(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # print("value_list:>>>", Array([Lua(o) for o in kwargs["value_list"]]))
            super().__init__(OrderedDict([
                
                ('caller', ObjectId(kwargs["caller"], "account")),
                ('contract_id', ObjectId(kwargs["contract_id"], "contract")),
                ('function_name', String(kwargs["function_name"])),
                ('value_list', Array([Lua(o) for o in kwargs["value_list"]])),
                # ('value_list', kwargs["value_list"]),
                ('extensions', Set([]))
            ]))


class Temporary_authority_chang(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('describe', String(kwargs["describe"])),
                ('temporary_active',),
                ('expiration_time', PointInTime(kwargs["expiration_time"])),
                ('extensions', Set([]))
            ]))


class Register_nh_asset_creator(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account"))
            ]))


class Create_world_view(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('world_view', String(kwargs["world_view"]))
            ]))


class Relate_world_view(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('related_account', ObjectId(kwargs["related_account"], "account")),
                ('world_view', String(kwargs["world_view"])),
                ('view_owner', ObjectId(kwargs["view_owner"], "account"))
            ]))


class Create_nh_asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('asset_id', String(kwargs["asset_id"])),
                ('world_view', String(kwargs["world_view"])),
                ('base_describe', String(kwargs["base_describe"]))
            ]))


class Relate_nh_asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('nh_asset_creator', ObjectId(kwargs["nh_asset_creator"], "account")),
                ('parent', ObjectId(kwargs["parent"], "nh_asset")),
                ('child', ObjectId(kwargs["child"], "nh_asset")),
                ('contract', ObjectId(kwargs["contract"], "contract")),
                ('relate', Bool(kwargs["relate"]))
            ]))


class Delete_nh_asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('nh_asset', ObjectId(kwargs["nh_asset"], "nh_asset"))
            ]))


class Transfer_nh_asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('from', ObjectId(kwargs["from"], "account")),
                ('to', ObjectId(kwargs["to"], "account")),
                ('nh_asset', ObjectId(kwargs["nh_asset"], "nh_asset"))
            ]))


class Create_nh_asset_order(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('otcaccount', ObjectId(kwargs["otcaccount"], "account")),
                ('pending_orders_fee', Asset(kwargs["pending_orders_fee"])),
                ('nh_asset', ObjectId(kwargs["nh_asset"], "nh_asset")),
                ('memo', String(kwargs["memo"])),
                ('price', Asset(kwargs["price"])),
                ('expiration', PointInTime(kwargs["expiration"]))
            ]))


class Cancel_nh_asset_order(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('order', ObjectId(kwargs["order"], "nh_asset_order")),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('extensions', Set([]))
            ]))


class Fill_nh_asset_order(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ('order', ObjectId(kwargs["order"], "nh_asset_order")),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('nh_asset', ObjectId(kwargs["nh_asset"], "nh_asset")),
                ('price_amount', String(kwargs["price_amount"])),
                ('price_asset_id', ObjectId(kwargs["price_asset_id"], "asset")),
                ('price_asset_symbol', String(kwargs["price_asset_symbol"])),
                ('extensions', Set([]))
            ]))


class Create_file(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("file_owner", ObjectId(kwargs["file_owner"], "account")),
                ("file_name", String(kwargs["file_name"])),
                ("file_content", String(kwargs["file_content"]))
            ]))


class Add_file_relate_account(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("file_owner", ObjectId(kwargs["file_owner"], "account")),
                ("file_id", ObjectId(kwargs["file_id"], "file")),
                ("related_account", Array([ObjectId(o, "account") for o in kwargs["related_account"]]))
            ]))


class File_signature(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("signature_account", ObjectId(kwargs["signature_account"], "account")),
                ("file_id", ObjectId(kwargs["file_id"], "file")),
                ("signature", String(kwargs["signature"]))
            ]))


class Relate_parent_file(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                # 
                ("sub_file_owner", ObjectId(kwargs["sub_file_owner"], "account")),
                ("parent_file", ObjectId(kwargs["parent_file"], "file")),
                # ("parent_file_related_account", Array([ObjectId(o, "account") for o in kwargs["parent_file_related_account"]])),
                ("parent_file_owner", ObjectId(kwargs["parent_file_owner"], "account")),
                ("sub_file", ObjectId(kwargs["sub_file"], "file"))
            ]))


class Revise_contract(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                # 
                ("reviser", ObjectId(kwargs["reviser"], "account")),
                ("contract_id", ObjectId(kwargs["contract_id"], "contract")),
                ("data", String(kwargs["data"])),
                ("extensions", Set([]))
            ]))


class Crontab_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("crontab_creator", ObjectId(kwargs["crontab_creator"], "account")),
                ("crontab_ops", Array([Op_wrapper(o) for o in kwargs["crontab_ops"]])),
                ("start_time", PointInTime(kwargs["start_time"])),
                ("execute_interval", Uint64(kwargs["execute_interval"])),
                ("scheduled_execute_times", Uint64(kwargs["scheduled_execute_times"])),
                ("extensions", Set([]))
            ]))


class Crontab_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("task", ObjectId(kwargs["task"], "crontab")),
                ("extensions", Set([]))
            ]))


class Crontab_recover(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                
                ("crontab_owner", ObjectId(kwargs["crontab_owner"], "account")),
                ("crontab", ObjectId(kwargs["crontab"], "crontab")),
                ("restart_time", PointInTime(kwargs["restart_time"])),
                ("extensions", Set([]))
            ]))


class Override_transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('from', ObjectId(kwargs["from"], "account")),
                ('to', ObjectId(kwargs["to"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('memo', memo),
                ('extensions', Set([])),
            ]))
