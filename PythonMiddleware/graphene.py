import json
import logging
import random
import re
from datetime import datetime, timedelta
from PythonMiddlewareapi.graphenenoderpc import GrapheneNodeRPC
from PythonMiddlewarebase.account import PrivateKey, PublicKey, BrainKey
from PythonMiddlewarebase import transactions, operations
from .asset import Asset
from .account import Account
from .amount import Amount
from .price import Price
from .witness import Witness
from .committee import Committee
from .vesting import Vesting
from .worker import Worker
from .contract import Contract
from .storage import configStorage as config
from .extensions import extensions as Extensions, getExtensionObjectFromString
from .exceptions import (
    AccountExistsException,
    AccountDoesNotExistsException,
    InsufficientAuthorityError,
    MissingKeyError,
)
from .wallet import Wallet
from .transactionbuilder import TransactionBuilder
from .utils import getRegItem, formatTimeFromNow

log = logging.getLogger(__name__)


class Graphene(object):
    """ Connect to the graphene network.

        :param str node: Node to connect to *(optional)*
        :param str rpcuser: RPC user *(optional)*
        :param str rpcpassword: RPC password *(optional)*
        :param bool nobroadcast: Do **not** broadcast a transaction! *(optional)*
        :param bool debug: Enable Debugging *(optional)*
        :param array,dict,string keys: Predefine the wif keys to shortcut the wallet database *(optional)*
        :param bool offline: Boolean to prevent connecting to network (defaults to ``False``) *(optional)*
        :param str proposer: Propose a transaction using this proposer *(optional)*
        :param int proposal_expiration: Expiration time (in seconds) for the proposal *(optional)*
        :param int proposal_review: Review period (in seconds) for the proposal *(optional)*
        :param int expiration: Delay in seconds until transactions are supposed to expire *(optional)*
        :param str blocking: Wait for broadcasted transactions to be included in a block and return full transaction (can be "head" or "irrversible")
        :param bool bundle: Do not broadcast transactions right away, but allow to bundle operations *(optional)*

        Three wallet operation modes are possible:

        * **Wallet Database**: Here, the graphenelibs load the keys from the
          locally stored wallet SQLite database (see ``storage.py``).
          To use this mode, simply call ``graphene()`` without the
          ``keys`` parameter
        * **Providing Keys**: Here, you can provide the keys for
          your accounts manually. All you need to do is add the wif
          keys for the accounts you want to use as a simple array
          using the ``keys`` parameter to ``graphene()``.
        * **Force keys**: This more is for advanced users and
          requires that you know what you are doing. Here, the
          ``keys`` parameter is a dictionary that overwrite the
          ``active``, ``owner``, or ``memo`` keys for
          any account. This mode is only used for *foreign*
          signatures!

        If no node is provided, it will connect to the node of
        http://uptick.rocks. It is **highly** recommended that you pick your own
        node instead. Default settings can be changed with:

        .. code-block:: python

            uptick set node <host>

        where ``<host>`` starts with ``ws://`` or ``wss://``.

        The purpose of this class it to simplify interaction with
        graphene.

        The idea is to have a class that allows to do this:

        .. code-block:: python

            from graphene import graphene
            graphene = graphene()
            print(graphene.info())

        All that is requires is for the user to have added a key with uptick

        .. code-block:: bash

            uptick addkey

        and setting a default author:

        .. code-block:: bash

            uptick set default_account xeroc

        This class also deals with edits, votes and reading content.
    """

    def __init__(self,
                 node="",
                 rpcuser="",
                 rpcpassword="",
                 debug=False,
                 **kwargs):

        # More specific set of APIs to register to
        if "apis" not in kwargs:
            kwargs["apis"] = [
                "database",
                "network_broadcast",
            ]
        # print("gph_kwargs:", kwargs)
        self.rpc = None
        self.debug = debug

        self.offline = bool(kwargs.get("offline", False))
        self.nobroadcast = bool(kwargs.get("nobroadcast", False))
        self.unsigned = bool(kwargs.get("unsigned", False))
        self.expiration = int(kwargs.get("expiration", 3600))
        self.proposer = kwargs.get("proposer", None)
        self.crontaber = kwargs.get("crontaber", None)
        self.crontab_start_time = kwargs.get("crontab_start_time", None)
        self.crontab_execute_interval = kwargs.get(
            "crontab_execute_interval", None)
        self.crontab_scheduled_execute_times = kwargs.get(
            "crontab_scheduled_execute_times", None)
        self.proposal_expiration = int(kwargs.get("proposal_expiration", 3600))
        self.proposal_review = kwargs.get("proposal_review", None)
        self.bundle = bool(kwargs.get("bundle", False))
        self.blocking = kwargs.get("blocking", False)

        # Store config for access through other Classes
        self.config = config

        # print("self.proposer:", self.proposer)

        if not self.offline:
            self.connect(node=node,
                         rpcuser=rpcuser,
                         rpcpassword=rpcpassword,
                         **kwargs)

        self.wallet = Wallet(self.rpc, **kwargs)
        self.txbuffer = TransactionBuilder(graphene_instance=self)

    def connect(self,
                node="",
                rpcuser="",
                rpcpassword="",
                **kwargs):
        """ Connect to graphene network (internal use only)
        """
        if not node:
            if "node" in config:
                node = config["node"]
            else:
                raise ValueError("A graphene node needs to be provided!")

        if not rpcuser and "rpcuser" in config:
            rpcuser = config["rpcuser"]

        if not rpcpassword and "rpcpassword" in config:
            rpcpassword = config["rpcpassword"]

        self.rpc = GrapheneNodeRPC(node, rpcuser, rpcpassword, **kwargs)

    def newWallet(self, pwd):
        """ Create a new wallet. This method is basically only calls
            :func:`graphene.wallet.create`.

            :param str pwd: Password to use for the new wallet
            :raises graphene.exceptions.WalletExists: if there is already a wallet created
        """
        self.wallet.create(pwd)

    def finalizeOp(self, ops, account, permission):
        """ This method obtains the required private keys if present in
            the wallet, finalizes the transaction, signs it and
            broadacasts it

            :param operation ops: The operation (or list of operaions) to broadcast
            :param operation account: The account that authorizes the
                operation
            :param string permission: The required permission for
                signing (active, owner, posting)

            ... note::

                If ``ops`` is a list of operation, they all need to be
                signable by the same key! Thus, you cannot combine ops
                that require active permission with ops that require
                posting permission. Neither can you use different
                accounts for different operations!
        """
        # Append transaction
        self.txbuffer.appendOps(ops)

        if self.unsigned:
            # In case we don't want to sign anything
            self.txbuffer.addSigningInformation(account, permission)
            return self.txbuffer
        elif self.bundle:
            # In case we want to add more ops to the tx (bundle)

            self.txbuffer.appendSigner(account, permission)
            # print("txbuffer>>>:",self.txbuffer.json())
            return self.txbuffer.json()
        else:
            # default behavior: sign + broadcast
            self.txbuffer.appendSigner(account, permission)
            self.txbuffer.sign()
            # return self.txbuffer.json()
            # print("tx.buffer>>>:",self.txbuffer.json())
            return self.txbuffer.broadcast()

    def sign(self, tx=None, wifs=[]):
        """ Sign a provided transaction witht he provided key(s)

            :param dict tx: The transaction to be signed and returned
            :param string wifs: One or many wif keys to use for signing
                a transaction. If not present, the keys will be loaded
                from the wallet as defined in "missing_signatures" key
                of the transactions.
        """
        if tx:
            txbuffer = TransactionBuilder(tx, graphene_instance=self)
        else:
            txbuffer = self.txbuffer

        txbuffer.appendWif(wifs)
        txbuffer.appendMissingSignatures()
        txbuffer.sign()
        return txbuffer.json()

    def broadcast(self, tx=None):
        """ Broadcast a transaction to the graphene network

            :param tx tx: Signed transaction to broadcast
        """
        if tx:
            # If tx is provided, we broadcast the tx
            return TransactionBuilder(tx).broadcast()
        else:
            return self.txbuffer.broadcast()

    def info(self):
        """ Returns the global properties
        """
        return self.rpc.get_dynamic_global_properties()

    def transfer(self, to, amount, asset, memo=["", 0], account=None):
        """ Transfer an asset to another account.

            :param str to: Recipient
            :param float amount: Amount to transfer
            :param str asset: Asset to transfer
            :param str memo: (optional) Memo, may begin with `#` for encrypted messaging
            :param str account: (optional) the source account for the transfer if not ``default_account``
        """
        from .memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        to = Account(to, graphene_instance=self)
        memoObj=None
        if(len(memo[0]) != 0):
            if(memo[1] == 0):
                memoObj = [0, memo[0]]
            elif[memo[1] == 1]:
                memoObj = [1, Memo(
                    from_account=account,
                    to_account=to,
                    graphene_instance=self
                ).encrypt(memo[0])
                ]
        op = operations.Transfer(**{

            "from": account["id"],
            "to": to["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj,
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account, "active")

    def limit_order_create(self, amount, asset, min_amount, min_amount_asset, fill=False, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        # if not asset:
        #     raise ValueError("You need to provide asset")
        account = Account(account, full=False, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        min_amount = Amount(min_amount, min_amount_asset,
                            graphene_instance=self)
        op = operations.Limit_order_create(**{

            "seller": account["id"],
            "amount_to_sell": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "min_to_receive": {
                "amount": int(min_amount),
                "asset_id": min_amount.asset["id"]
            },
            "expiration": transactions.formatTimeFromNow(self.expiration),
            # "min_to_receive": {"amount": min_amount[0], "asset_id": min_amount[1]},
            "fill_or_kill": fill,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def limit_order_cancel(self, order_numbers, account=None):
        """ Cancels an order you have placed in a given market. Requires
            only the "orderNumbers". An order number takes the form
            ``1.7.xxx``.

            :param str orderNumbers: The Order Object ide of the form ``1.7.xxxx``
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, full=False, graphene_instance=self)

        if not isinstance(order_numbers, (list, set)):
            order_numbers = set(order_numbers)

        op = []
        for order in order_numbers:
            op.append(
                operations.Limit_order_cancel(**{

                    "fee_paying_account": account["id"],
                    "order": order,
                    "extensions": [],
                    "prefix": self.rpc.chain_params["prefix"]}))
        return self.finalizeOp(op, account["name"], "active")

    def call_order_update(self, amount, asset, _amount, _asset, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        # if not asset:
        #     raise ValueError("You need to provide asset")
        account = Account(account, full=False, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        _amount = Amount(_amount, _asset, graphene_instance=self)
        op = operations.Call_order_update(**{

            "funding_account": account["id"],
            "delta_collateral": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "delta_debt": {
                "amount": int(_amount),
                "asset_id": _amount.asset["id"]
            },
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def create_account(
        self,
        account_name,
        registrar=None,
        owner_key=None,
        active_key=None,
        memo_key=None,
        password=None,
        additional_owner_keys=[],
        additional_active_keys=[],
        additional_owner_accounts=[],
        additional_active_accounts=[],
        proxy_account="null-account",
        storekeys=True,
    ):
        """ Create new account on graphene

            The brainkey/password can be used to recover all generated keys (see
            `graphenebase.account` for more details.

            By default, this call will use ``default_account`` to
            register a new name ``account_name`` with all keys being
            derived from a new brain key that will be returned. The
            corresponding keys will automatically be installed in the
            wallet.

            .. warning:: Don't call this method unless you know what
                          you are doing! Be sure to understand what this
                          method does and where to find the private keys
                          for your account.

            .. note:: Please note that this imports private keys
                      (if password is present) into the wallet by
                      default. However, it **does not import the owner
                      key** for security reasons. Do NOT expect to be
                      able to recover it from the wallet if you lose
                      your password!

            :param str account_name: (**required**) new account name
            :param str registrar: which account should pay the registration fee
                                (defaults to ``default_account``)
            :param str owner_key: Main owner key
            :param str active_key: Main active key
            :param str memo_key: Main memo_key
            :param str password: Alternatively to providing keys, one
                                 can provide a password from which the
                                 keys will be derived
            :param array additional_owner_keys:  Additional owner public keys
            :param array additional_active_keys: Additional active public keys
            :param array additional_owner_accounts: Additional owner account names
            :param array additional_active_accounts: Additional acctive account names
            :param bool storekeys: Store new keys in the wallet (default: ``True``)
            :raises AccountExistsException: if the account already exists on the blockchain

        """
        if not registrar and config["default_account"]:
            registrar = config["default_account"]
        if not registrar:
            raise ValueError(
                "Not registrar account given. Define it with " +
                "registrar=x, or set the default_account using uptick")
        if password and (owner_key or active_key or memo_key):
            raise ValueError(
                "You cannot use 'password' AND provide keys!"
            )

        try:
            Account(account_name, graphene_instance=self)
            raise AccountExistsException
        except:
            pass

        registrar = Account(registrar, graphene_instance=self)
        # if not referrer:
        #     referrer = registrar
        # else:
        #     referrer = Account(referrer, graphene_instance=self)

        " Generate new keys from password"
        from PythonMiddlewarebase.account import PasswordKey, PublicKey
        if password:
            active_key = PasswordKey(account_name, password, role="active")
            owner_key = PasswordKey(account_name, password, role="owner")
            # memo_key = PasswordKey(account_name, password, role="memo")#nico chang: memo key 使用active角色，避免memo与active，公钥不一致
            active_pubkey = active_key.get_public_key()
            owner_pubkey = owner_key.get_public_key()
            #memo_pubkey = memo_key.get_public_key()
            memo_pubkey = active_key.get_public_key()
            active_privkey = active_key.get_private_key()
            owner_privkey = owner_key.get_private_key()
            #memo_privkey = memo_key.get_private_key()
            # memo_privkey = active_key.get_private_key()
            # store private keys
            if storekeys:
                self.wallet.addPrivateKey(owner_privkey)
                self.wallet.addPrivateKey(active_privkey)
                # self.wallet.addPrivateKey(memo_privkey)
        elif owner_key and active_key:
            active_pubkey = PublicKey(
                active_key, prefix=self.rpc.chain_params["prefix"])
            owner_pubkey = PublicKey(
                owner_key, prefix=self.rpc.chain_params["prefix"])
            # memo_pubkey = PublicKey(memo_key, prefix=self.rpc.chain_params["prefix"])
            memo_pubkey = active_pubkey
        else:
            raise ValueError(
                "Call incomplete! Provide either a password or public keys!"
            )
        owner = format(owner_pubkey, self.rpc.chain_params["prefix"])
        active = format(active_pubkey, self.rpc.chain_params["prefix"])
        memo = format(memo_pubkey, self.rpc.chain_params["prefix"])

        owner_key_authority = [[owner, 1]]
        active_key_authority = [[active, 1]]
        owner_accounts_authority = []
        active_accounts_authority = []

        # additional authorities
        for k in additional_owner_keys:
            owner_key_authority.append([k, 1])
        for k in additional_active_keys:
            active_key_authority.append([k, 1])

        for k in additional_owner_accounts:
            addaccount = Account(k, graphene_instance=self)
            owner_accounts_authority.append([addaccount["id"], 1])
        for k in additional_active_accounts:
            addaccount = Account(k, graphene_instance=self)
            active_accounts_authority.append([addaccount["id"], 1])

        # voting account
        # voting_account = Account(proxy_account or "proxy-to-self")

        op = {

            "registrar": registrar["id"],
            # "referrer": referrer["id"],
            # "referrer_percent": referrer_percent * 100,
            "name": account_name,
            'owner': {'account_auths': owner_accounts_authority,
                      'key_auths': owner_key_authority,
                      "address_auths": [],
                      'weight_threshold': 1},
            'active': {'account_auths': active_accounts_authority,
                       'key_auths': active_key_authority,
                       "address_auths": [],
                       'weight_threshold': 1},
            "options": {"memo_key": memo,
                        # "voting_account": voting_account["id"],
                        # "num_witness": 0,
                        # "num_committee": 0,
                        "votes": [],
                        "extensions": []
                        },
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        }
        op = operations.Account_create(**op)
        return self.finalizeOp(op, registrar["name"], "active")

    def asset_create(self, symbol, precision, common_options, bitasset_opts=None, account=None):
        account = Account(account, graphene_instance=self)
        # amount = Amount(amount, asset, graphene_instance=self)
        # _amount = Amount(_amount, _asset, graphene_instance=self)
        # base = {
        #     "amount": int(amount),
        #     "asset_id": amount.asset["id"]
        # }
        # quote = {
        #     "amount": int(_amount),
        #     "asset_id": _amount.asset["id"]
        # }
        # common_options["core_exchange_rate"] = {"base": base, "quote": quote}
        op = operations.Asset_create(**{

            "issuer": account["id"],
            "symbol": symbol,
            "precision": precision,
            "common_options": common_options,
            "bitasset_opts": bitasset_opts,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def asset_update(self, asset, new_options, issuer=None, account=None):
        if not asset:
            raise ValueError("You need to provide to an asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide to an account")
        asset = Asset(asset, graphene_instance=self)["id"]
        issuer = Account(account, graphene_instance=self)
        # print("issuer_id", issuer["id"])
        # new_issuer = Account(account)
        # print("n_issuer_id", new_issuer["id"])
        op = operations.Asset_update(**{

            "issuer": issuer["id"],
            "asset_to_update": asset,
            # "new_issuer": new_issuer["id"],
            "new_options": new_options,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_update_restricted(self, target_asset, restricted_type, restricted_list, isadd=True, account=None):
        if not target_asset:
            raise ValueError("You need to provide to a target asset")
        if not restricted_type:
            raise ValueError("You need to provide to a restricted type")
        if not restricted_list:
            raise ValueError("You need to provide to restricted account")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide to an account")
        from PythonMiddlewarebase.asset_permissions import restricted
        restricted_type = restricted[restricted_type]
        # print("restircted_type", restricted_type)
        target_asset = Asset(target_asset, graphene_instance=self)["id"]
        account = Account(account, full=False, graphene_instance=self)
        op = operations.Asset_update_restricted(**{
            "payer": account["id"],
            "target_asset": target_asset,
            "isadd": isadd,
            "restricted_type": restricted_type,
            # "restricted_list": [Account(x)["id"] for x in restricted_list]
            "restricted_list": restricted_list
        })
        return self.finalizeOp(op, account["name"], "active")

    def update_collateral_for_gas(self, beneficiary, collateral, account=None):
        # if not mortgager:
        #     raise ValueError("You need to provide to a mortgager")
        if not beneficiary:
            raise ValueError("You need to provide to a beneficiary")
        if not collateral:
            raise ValueError("You need to provide to collateral")
        if collateral < 0:
            raise ValueError(
                "The collateral need to greater than or equal to 0")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide to an mortgager")
        mortgager = Account(account, full=False, graphene_instance=self)
        beneficiary = Account(beneficiary, full=False, graphene_instance=self)

        op = operations.Update_collateral_for_gas(**{
            "mortgager": mortgager["id"],
            "beneficiary": beneficiary["id"],
            "collateral": collateral
        })
        return self.finalizeOp(op, mortgager["name"], "active")

    def asset_update_bitasset(self, asset, new_options, account=None):
        if not asset:
            raise ValueError("You need to provide to an asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide to an account")
        asset = Asset(asset, graphene_instance=self)["id"]
        # short_backing_asset = Asset(short_backing_asset, graphene_instance=self)["id"]
        issuer = Account(account, graphene_instance=self)
        # new_options = {
        #     "feed_lifetime_sec": 60*60*24,
        #     "minimum_feeds": 1,
        #     "force_settlement_delay_sec": 60*60*24,
        #     "force_settlement_offset_percent": 1,
        #     "maximum_force_settlement_volume": 2000,
        #     "short_backing_asset": short_backing_asset,
        #     "extensions": {}
        # }
        op = operations.Asset_update_bitasset(**{

            "issuer": issuer["id"],
            "asset_to_update": asset,
            "new_options": new_options,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_update_feed_producers(self, asset, feed_producers, account=None):
        if not asset:
            raise ValueError("You need to provide to an asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide to an account")
        assert Asset(
            asset).is_bitasset, "Asset needs to be a bitasset/market pegged asset"
        asset = Asset(asset, graphene_instance=self)["id"]
        issuer = Account(account, graphene_instance=self)
        op = operations.Asset_update_feed_producers(**{

            "issuer": issuer["id"],
            "asset_to_update": asset,
            "new_feed_producers": [Account(x)["id"] for x in feed_producers],
            "extensions": {}
        })
        return self.finalizeOp(op, issuer, "active")

    def asset_issue(self, amount, asset, issue_to_account, memo=["",0], account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        _account = Account(issue_to_account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        from .memo import Memo
        memoObj=None
        if(len(memo[0]) != 0):
            if(memo[1] == 0):
                memoObj = [0, memo[0]]
            elif[memo[1] == 1]:
                memoObj = [1, Memo(
                    from_account=account,
                    to_account=_account,
                    graphene_instance=self
                ).encrypt(memo[0])
                ]
        op = operations.Asset_issue(**{

            "issuer": account["id"],
            "asset_to_issue": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "issue_to_account": _account["id"],
            "memo": memoObj,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_fund_fee_pool(self, asset, amount, account=None):
        if not (asset or amount):
            raise ValueError("You need to provide asset or amount")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        # amount = Amount(amount, asset)
        op = operations.Asset_fund_fee_pool(**{

            "from_account": account["id"],
            "asset_id": asset,
            "amount": amount,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_settle(self, amount, asset, account=None):
        if not (asset or amount):
            raise ValueError("You need to provide asset or amount")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Asset_settle(**{

            "account": account["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_settle_cancel(self, settlement, amount, asset, account=None):
        if not settlement:
            raise ValueError("You need to provide settlement id")
        if not (asset or amount):
            raise ValueError("You need to provide asset or amount")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Asset_settle_cancel(**{
            "settlement": settlement,
            "account": account["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def asset_global_settle(self, asset_to_settle, settle_price, account=None):
        if not (asset_to_settle or settle_price):
            raise ValueError("You need to provide asset or price")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        asset_to_settle = Asset(asset_to_settle, graphene_instance=self)["id"]
        op = operations.Asset_global_settle(**{

            "issuer": account["id"],
            "asset_to_settle": asset_to_settle,
            "settle_price": settle_price,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def _test_weights_treshold(self, authority):
        """ This method raises an error if the threshold of an authority cannot
            be reached by the weights.

            :param dict authority: An authority of an account
            :raises ValueError: if the threshold is set too high
        """
        weights = 0
        for a in authority["account_auths"]:
            weights += a[1]
        for a in authority["key_auths"]:
            weights += a[1]
        if authority["weight_threshold"] > weights:
            raise ValueError("Threshold too restrictive!")

    def allow(self, foreign, weight=None, permission="active",
              account=None, threshold=None):
        """ Give additional access to an account by some other public
            key or account.

            :param str foreign: The foreign account that will obtain access
            :param int weight: (optional) The weight to use. If not
                define, the threshold will be used. If the weight is
                smaller than the threshold, additional signatures will
                be required. (defaults to threshold)
            :param str permission: (optional) The actual permission to
                modify (defaults to ``active``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
            :param int threshold: The threshold that needs to be reached
                by signatures to be able to interact
        """
        from copy import deepcopy
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if permission not in ["owner", "active"]:
            raise ValueError(
                "Permission needs to be either 'owner', or 'active"
            )
        account = Account(account, graphene_instance=self)

        if not weight:
            weight = account[permission]["weight_threshold"]

        authority = deepcopy(account[permission])
        try:
            pubkey = PublicKey(foreign, prefix=self.rpc.chain_params["prefix"])
            authority["key_auths"].append([
                str(pubkey),
                weight
            ])
        except:
            try:
                foreign_account = Account(foreign, graphene_instance=self)
                authority["account_auths"].append([
                    foreign_account["id"],
                    weight
                ])
            except:
                raise ValueError(
                    "Unknown foreign account or invalid public key"
                )
        if threshold:
            authority["weight_threshold"] = threshold
            self._test_weights_treshold(authority)

        op = operations.Account_update(**{

            "account": account["id"],
            permission: authority,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        if permission == "owner":
            return self.finalizeOp(op, account["name"], "owner")
        else:
            return self.finalizeOp(op, account["name"], "active")

    def disallow(self, foreign, permission="active",
                 account=None, threshold=None):
        """ Remove additional access to an account by some other public
            key or account.

            :param str foreign: The foreign account that will obtain access
            :param str permission: (optional) The actual permission to
                modify (defaults to ``active``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
            :param int threshold: The threshold that needs to be reached
                by signatures to be able to interact
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if permission not in ["owner", "active"]:
            raise ValueError(
                "Permission needs to be either 'owner', or 'active"
            )
        account = Account(account, graphene_instance=self)
        authority = account[permission]

        try:
            pubkey = PublicKey(foreign, prefix=self.rpc.chain_params["prefix"])
            affected_items = list(
                filter(lambda x: x[0] == str(pubkey),
                       authority["key_auths"]))
            authority["key_auths"] = list(filter(
                lambda x: x[0] != str(pubkey),
                authority["key_auths"]
            ))
        except:
            try:
                foreign_account = Account(foreign, graphene_instance=self)
                affected_items = list(
                    filter(lambda x: x[0] == foreign_account["id"],
                           authority["account_auths"]))
                authority["account_auths"] = list(filter(
                    lambda x: x[0] != foreign_account["id"],
                    authority["account_auths"]
                ))
            except:
                raise ValueError(
                    "Unknown foreign account or unvalid public key"
                )

        removed_weight = affected_items[0][1]

        # Define threshold
        if threshold:
            authority["weight_threshold"] = threshold

        # Correct threshold (at most by the amount removed from the
        # authority)
        try:
            self._test_weights_treshold(authority)
        except:
            log.critical(
                "The account's threshold will be reduced by %d"
                % (removed_weight)
            )
            authority["weight_threshold"] -= removed_weight
            self._test_weights_treshold(authority)

        op = operations.Account_update(**{

            "account": account["id"],
            permission: authority,
            "extensions": {}
        })
        if permission == "owner":
            return self.finalizeOp(op, account["name"], "owner")
        else:
            return self.finalizeOp(op, account["name"], "active")

    def update_memo_key(self, key, account=None):
        """ Update an account's memo public key

            This method does **not** add any private keys to your
            wallet but merely changes the memo public key.

            :param str key: New memo public key
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        PublicKey(key, prefix=self.rpc.chain_params["prefix"])

        account = Account(account, graphene_instance=self)
        account["options"]["memo_key"] = key
        op = operations.Account_update(**{

            "account": account["id"],
            "new_options": account["options"],
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def AccountAddExtension(self, assetID, itemVER, itemID, extensionData, account=None):
        """
            return -1 : This data has already existed
        """
        if (not assetID) or (not itemVER) or (not itemID):
            raise ValueError(
                "You need to provide an assetId and a itemVER and itemID ")
        if not extensionData:
            raise ValueError("You need to provide an extensionData")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        options = account["options"]
        extension = Extensions(assetID, itemVER, itemID, extensionData)
        # index=extension.findExtension(options["extensions"])
        # if (index>-1):#找到目标数据，不能直接添加，可执行修改
        #    return -1
        # else:
        #    options["extensions"]=[]
        #    options["extensions"].append("add:"+extension.string())
        # options["extensions"]=[]
        # print(extension.string())
        options["extensions"].append(extension.string())
        # print(options["extensions"])
        op = operations.Account_update(**{

            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def AccountDelExtension(self, itemID, account=None):
        """
            return -1 : This data has already existed 
        """
        flag = False  # 标记是否有用户想删除的itemID，默认为False
        if not itemID:
            raise ValueError("You need to provide itemID ")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        options = account["options"]
        # extension=Extensions("*",itemVER,itemID,"*")
        ext_list = options['extensions']
        patter = '(.*)@([0-9a-zA-Z]+);(.*)'
        for index, ext in enumerate(ext_list):
            target = getRegItem(ext, patter, 2)
            if itemID == target:
                ext_list.pop(index)
                flag = True         # 找到itemID
                break
        if not flag:
            raise ValueError("You need to provide a correct itemID")
        options['extensions'] = ext_list
        # options['extensions']=[]
        # options["extensions"].append("erase:"+extension.string())

        op = operations.Account_update(**{

            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def AccountChangeExtension(self, assetID, itemVER, itemID, extensionData, account=None):
        return self.AccountAddExtension(assetID, itemVER, itemID, extensionData, account)

    def AccountFindExtension(self, itemVER, itemID, account=None):
        """
            return -1 : This data has already existed 
        """
        if(not itemVER) and (not itemID):
            raise ValueError("You need to provide a itemVER or itemID ")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        options = account["options"]
        retExtensions = []
        if(itemVER == "*"):
            for extension in options["extensions"]:
                retExtensions.append(getExtensionObjectFromString(extension))
        elif (itemID == "*"):
            for extension in options["extensions"]:
                temp = getExtensionObjectFromString(extension)
                if temp:
                    if temp.compareWithVER(itemVER):
                        retExtensions.append(temp)
        else:
            # print("extensions:>>>>%s"%options["extensions"])
            for extension in options["extensions"]:
                temp = getExtensionObjectFromString(extension)
                if temp:
                    if temp.compareWithId(itemID):
                        retExtensions.append(temp)
        return retExtensions

    def approve_witness(self, witnesses, vote_type, vote_amount, vote_asset, account=None):
        """ Approve a witness

            :param list witnesses: list of Witness name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(witnesses, (list, set)):
            witnesses = set(witnesses)
        for wit in witnesses:
            wit = Witness(wit, graphene_instance=self)
            options["votes"].append(wit["vote_id"])
        options["votes"] = list(set(options["votes"]))
        options["num_witness"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 1,
            options["votes"]
        )))
        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def disapprove_witness(self, witnesses, vote_type, vote_amount, vote_asset, account=None):
        """ Disapprove a witness

            :param list witnesses: list of Witness name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(witnesses, (list, set)):
            witnesses = set(witnesses)

        for witness in witnesses:
            witness = Witness(witness, graphene_instance=self)
            if witness["vote_id"] in options["votes"]:
                options["votes"].remove(witness["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_witness"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 1,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def committee_member_create(self, url, account=None):
        if not url:
            raise ValueError("You need to provide a url")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Committee_member_create(**{

            "committee_member_account": account["id"],
            "url": url
        })
        return self.finalizeOp(op, account["name"], "active")

    def committee_member_update(self, work_status, new_url="", account=None):
        # if not committee_member:
        #     raise ValueError("You need to provide a committee_member")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        committee_member = Committee(account, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        op = operations.Committee_member_update(**{
            "work_status": work_status,
            "committee_member": committee_member["id"],
            "committee_member_account": committee_member["committee_member_account"],
            "new_url": new_url
        })
        return self.finalizeOp(op, account["name"], "active")

    def approve_committee(self, committees, vote_type, vote_amount, vote_asset, account=None):
        """ Approve a committee

            :param list committees: list of committee member name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(committees, (list, set)):
            committees = set(committees)

        for committee in committees:
            committee = Committee(committee, graphene_instance=self)
            options["votes"].append(committee["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_committee"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 0,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def disapprove_committee(self, committees, vote_type, vote_amount, vote_asset, account=None):
        """ Disapprove a committee

            :param list committees: list of committee name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(committees, (list, set)):
            committees = set(committees)

        for committee in committees:
            committee = Committee(committee, graphene_instance=self)
            if committee["vote_id"] in options["votes"]:
                options["votes"].remove(committee["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_committee"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 0,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def approve_worker(self, workers, vote_type, vote_amount, vote_asset, account=None):
        """ Approve a worker

            :param list workers: list of worker member name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(workers, (list, set)):
            workers = set(workers)

        for worker in workers:
            worker = Worker(worker, graphene_instance=self)
            options["votes"].append(worker["vote_for"])
        options["votes"] = list(set(options["votes"]))

        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def disapprove_worker(self, workers, vote_type, vote_amount, vote_asset, account=None):
        """ Disapprove a worker

            :param list workers: list of worker name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        amount = Amount(vote_amount, vote_asset, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        options = account["options"]

        if not isinstance(workers, (list, set)):
            workers = set(workers)

        for worker in workers:
            worker = Worker(worker, graphene_instance=self)
            if worker["vote_for"] in options["votes"]:
                options["votes"].remove(worker["vote_for"])
        options["votes"] = list(set(options["votes"]))

        op = operations.Account_update(**{
            "lock_with_vote": [vote_type, {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }],
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def account_whitelist(self, account_to_list, account_listing="no_listing", account=None):
        if account_listing == "white_listed":
            account_listing = 0x1
        elif account_listing == "black_listed":
            account_listing = 0x2
        elif account_listing == "white_and_black_listed":
            account_listing = (0x1 | 0x2)
        else:
            account_listing = 0x0
        _account = Account(account_to_list, full=False, graphene_instance=self)
        account = Account(account, full=False, graphene_instance=self)
        op = operations.Account_whitelist(**{

            "authorizing_account": account["id"],
            "account_to_list": _account["id"],
            "new_listing": account_listing,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def withdraw_permission_create(self, authorized_account, amount, asset, period_start_time, withdrawal_period_sec=0, periods_until_expiration=0, account=None):
        if not authorized_account:
            raise ValueError("You need to provide an authorized_account")
        if not (amount or asset):
            raise ValueError("You need to provide asset or amount")
        if not period_start_time:
            raise ValueError("You need to provide period start time")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError(
                    "You need to provide an withdraw from account")
        account = Account(account, graphene_instance=self)
        authorized_account = Account(
            authorized_account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Withdraw_permission_create(**{

            "withdraw_from_account": account["id"],
            "authorized_account": authorized_account["id"],
            "withdrawal_limit": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "withdrawal_period_sec": withdrawal_period_sec,
            "periods_until_expiration": periods_until_expiration,
            "period_start_time": period_start_time
        })
        return self.finalizeOp(op, account, "active")

    def withdraw_permission_update(self, authorized_account, permission_to_update, amount, asset, period_start_time, withdrawal_period_sec=0, periods_until_expiration=0, account=None):
        if not authorized_account:
            raise ValueError("You need to provide an authorized_account")
        if not permission_to_update:
            raise ValueError("You need to provide withdraw_permission")
        if not (amount or asset):
            raise ValueError("You need to provide asset or amount")
        if not period_start_time:
            raise ValueError("You need to provide period start time")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError(
                    "You need to provide an withdraw from account")
        account = Account(account, graphene_instance=self)
        authorized_account = Account(
            authorized_account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)

        op = operations.Withdraw_permission_update(**{

            "withdraw_from_account": account["id"],
            "authorized_account": authorized_account["id"],
            "permission_to_update": permission_to_update,
            "withdrawal_limit": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "withdrawal_period_sec": withdrawal_period_sec,
            "periods_until_expiration": periods_until_expiration,
            "period_start_time": period_start_time
        })
        return self.finalizeOp(op, account, "active")

    def withdraw_permission_claim(self, withdraw_permission, withdraw_from_account, amount, asset, memo="", account=None):
        if not withdraw_permission:
            raise ValueError("You need to provide a withdraw_permission")
        if not withdraw_from_account:
            raise ValueError("You need to provide withdraw_from_account")
        if not (amount or asset):
            raise ValueError("You need to provide asset or amount")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError(
                    "You need to provide an withdraw from account")
        account = Account(account, graphene_instance=self)
        withdraw_from_account = Account(
            withdraw_from_account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        from .memo import Memo
        memoObj = Memo(
            from_account=withdraw_from_account,
            to_account=account,
            graphene_instance=self
        )
        op = operations.Withdraw_permission_claim(**{

            "withdraw_permission": withdraw_permission,
            "withdraw_from_account": withdraw_from_account["id"],
            "withdraw_to_account": account["id"],
            "amount_to_withdraw": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj.encrypt(memo)
        })
        return self.finalizeOp(op, account, "active")

    def withdraw_permission_delete(self, authorized_account, withdrawal_permission, account=None):
        if not withdrawal_permission:
            raise ValueError("You need to provide a withdrawal_permission")
        if not authorized_account:
            raise ValueError("You need to provide authorized_account")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError(
                    "You need to provide an withdraw from account")
        account = Account(account, graphene_instance=self)
        authorized_account = Account(
            authorized_account, graphene_instance=self)
        op = operations.Withdraw_permission_delete(**{

            "withdraw_from_account": account["id"],
            "authorized_account": authorized_account["id"],
            "withdrawal_permission": withdrawal_permission
        })
        return self.finalizeOp(op, account, "active")

    def get_vesting_balances(self, account_id_or_name):
        account_id = Account(account_id_or_name, graphene_instance=self)["id"]
        vesting_objects = self.rpc.get_vesting_balances(account_id)
        return vesting_objects

    def vesting_balance_create(self, owner, amount, asset, start, _type="cdd", vesting_cliff_seconds=0, vesting_duration_seconds=0, vesting_seconds=0, account=None):
        if not start:
            start = datetime.utcnow()
        if not owner:
            raise ValueError("You need to provide owner")
        if not (amount or asset):
            raise ValueError("You need to provide asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        owner = Account(owner, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)

        if _type == "linear":
            initializer = [0, {
                "begin_timestamp": start,
                "vesting_cliff_seconds": vesting_cliff_seconds,
                "vesting_duration_seconds": vesting_duration_seconds
            }]
        elif _type == "cdd":
            initializer = [1, {
                "start_claim": start,
                "vesting_seconds": vesting_seconds
            }]
        else:
            raise ValueError('type not in ["linear", "cdd"]')

        op = operations.Vesting_balance_create(**{

            "creator": account["id"],
            "owner": owner["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "policy": initializer
        })
        return self.finalizeOp(op, account, "active")

    def vesting_balance_withdraw(self, vesting_id, amount=None, asset=None, account=None):
        """ Withdraw vesting balance

            :param str vesting_id: Id of the vesting object
            :param graphene.amount.Amount Amount: to withdraw ("all" if not provided")
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        # amount = Amount(amount, asset)

        if not (amount or asset):
            obj = Vesting(vesting_id, graphene_instance=self)
            amount = obj.claimable
            # print("obj:", obj)
            # print("amount", amount)
        else:
            amount = Amount(amount, asset, graphene_instance=self)

        op = operations.Vesting_balance_withdraw(**{

            "vesting_balance": vesting_id,
            "owner": account["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount["asset"]["id"]
            },
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def approveproposal(self, proposal_ids, account=None, approver=None):
        """ Approve Proposal

            :param list proposal_id: Ids of the proposals
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        from .proposal import Proposal
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        is_key = approver and approver[:3] == self.rpc.chain_params["prefix"]
        if not approver and not is_key:
            approver = account
        elif approver and not is_key:
            approver = Account(approver, graphene_instance=self)
        else:
            approver = PublicKey(approver)

        if not isinstance(proposal_ids, (list, set)):
            proposal_ids = set(proposal_ids)

        op = []
        for proposal_id in proposal_ids:
            proposal = Proposal(proposal_id, graphene_instance=self)
            update_dict = {

                'fee_paying_account': account["id"],
                'proposal': proposal["id"],
                "prefix": self.rpc.chain_params["prefix"]
            }
            if is_key:
                update_dict.update({
                    'key_approvals_to_add': [str(approver)],
                })
            else:
                update_dict.update({
                    'active_approvals_to_add': [approver["id"]],
                })
            op.append(operations.Proposal_update(**update_dict))
        if is_key:
            self.txbuffer.appendSigner(account["name"], "active")
            return self.finalizeOp(op, approver, "active")
        else:
            return self.finalizeOp(op, approver["name"], "active")

    def disapproveproposal(self, proposal_ids, account=None, approver=None):
        """ Disapprove Proposal

            :param list proposal_ids: Ids of the proposals
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        from .proposal import Proposal
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        if not approver:
            approver = account
        else:
            approver = Account(approver, graphene_instance=self)

        if not isinstance(proposal_ids, (list, set)):
            proposal_ids = set(proposal_ids)

        op = []
        for proposal_id in proposal_ids:
            proposal = Proposal(proposal_id, graphene_instance=self)
            op.append(operations.Proposal_update(**{

                'fee_paying_account': account["id"],
                'proposal': proposal["id"],
                'active_approvals_to_remove': [approver["id"]],
                "prefix": self.rpc.chain_params["prefix"]
            }))
        return self.finalizeOp(op, account["name"], "active")

    def proposal_delete(self, proposal, account=None):
        account = Account(account, graphene_instance=self)
        op = operations.Proposal_delete(**{

            "fee_paying_account": account["id"],
            # "using_owner_authority": using_owner_authority,
            "proposal": proposal,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def publish_price_feed(
        self,
        symbol,
        settlement_price,
        # cer=None,
        mssr=150,
        mcr=175,
        account=None
    ):
        """ Publish a price feed for a market-pegged asset

            :param str symbol: Symbol of the asset to publish feed for
            :param graphene.price.Price settlement_price: Price for settlement
            :param graphene.price.Price cer: Core exchange Rate (default ``settlement_price + 5%``)
            :param float mssr: Percentage for max short squeeze ratio (default: 110%)
            :param float mcr: Percentage for maintenance collateral ratio (default: 200%)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

            .. note:: The ``account`` needs to be allowed to produce a
                      price feed for ``symbol``. For witness produced
                      feeds this means ``account`` is a witness account!
        """
        # from PythonMiddlewarebase.objects import Price
        # settlement_price = Price(settlement_price)
        # assert isinstance(settlement_price, Price), "settlement_price needs to be instance of `graphene.price.Price`!"
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        asset = Asset(symbol, graphene_instance=self, full=True)
        # assert asset["id"] == settlement_price["base"]["asset"]["id"] or \
        #     asset["id"] == settlement_price["quote"]["asset"]["id"], \
        assert asset["id"] == settlement_price["base"]["asset_id"] or \
            asset["id"] == settlement_price["quote"]["asset_id"], \
            "Price needs to contain the asset of the symbol you'd like to produce a feed for!"
        assert asset.is_bitasset, "Symbol needs to be a bitasset!"
        # assert settlement_price["base"]["asset_id"] == asset["bitasset_data"]["options"]["short_backing_asset"] or \
        #     settlement_price["quote"]["asset"]["id"] == asset["bitasset_data"]["options"]["short_backing_asset"], \
        assert settlement_price["base"]["asset_id"] == self.rpc.get_object(asset["bitasset_data_id"])["options"]["short_backing_asset"] or \
            settlement_price["quote"]["asset_id"] == self.rpc.get_object(asset["bitasset_data_id"])["options"]["short_backing_asset"], \
            "The Price needs to be relative to the backing collateral!"

        # Base needs to be short backing asset
        if settlement_price["base"]["asset_id"] == self.rpc.get_object(asset["bitasset_data_id"])["options"]["short_backing_asset"]:
            settlement_price = Price(settlement_price, graphene_instance=self)
            settlement_price = settlement_price.invert()

        # if cer:
        #     if cer["base"]["asset_id"] == self.rpc.get_object(asset["bitasset_data_id"])["options"]["short_backing_asset"]:
        #         cer = Price(cer, graphene_instance=self)
        #         cer = cer.invert()
        # else:
        #     cer = settlement_price * 1.05

        op = operations.Asset_publish_feed(**{

            "publisher": account["id"],
            "asset_id": asset["id"],
            "feed": {
                # "settlement_price": settlement_price.json(),
                "settlement_price": settlement_price,
                # "core_exchange_rate": cer.json(),
                # "core_exchange_rate": cer,
                "maximum_short_squeeze_ratio": int(mssr * 10),
                "maintenance_collateral_ratio": int(mcr * 10),
            },
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def upgrade_account(self, account=None):
        """ Upgrade an account to Lifetime membership

            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Account_upgrade(**{

            "account_to_upgrade": account["id"],
            "upgrade_to_lifetime_member": True,
            "prefix": self.rpc.chain_params["prefix"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def update_witness(self, witness_identifier, work_status, url=None, key=None):
        """ Upgrade a witness account

            :param str witness_identifier: Identifier for the witness
            :param str url: New URL for the witness
            :param str key: Public Key for the signing
        """
        witness = Witness(witness_identifier, graphene_instance=self)
        account = witness.account
        op = operations.Witness_update(**{

            "prefix": self.rpc.chain_params["prefix"],
            "witness": witness["id"],
            "witness_account": account["id"],
            "new_url": url,
            "new_signing_key": key,
            "work_status": work_status
        })
        return self.finalizeOp(op, account["name"], "active")

    def create_witness(self, account_name, url, key):
        account = Account(account_name, graphene_instance=self)
        op = operations.Witness_create(**{

            "prefix": self.rpc.chain_params["prefix"],
            "witness_account": account["id"],
            "url": url,
            "block_signing_key": key,
        })
        return self.finalizeOp(op, account["name"], "active")

    def asset_reserve(self, amount, asset, account=None):
        """ Reserve/Burn an amount of this shares

            This removes the shares from the supply

            :param graphene.amount.Amount amount: The amount to be burned.
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        # assert isinstance(amount, Amount)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Asset_reserve(**{

            "payer": account["id"],
            "amount_to_reserve": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]},
            "extensions": []
        })
        return self.finalizeOp(op, account, "active")

    def create_worker(
        self,
        name,
        daily_pay,
        end,
        describe="",
        begin=None,
        payment_type="vesting",
        pay_vesting_period_days=0,
        account=None
    ):
        """ Reserve/Burn an amount of this shares

            This removes the shares from the supply

            **Required**

            :param str name: Name of the worke
            :param graphene.amount.Amount daily_pay: The amount to be paid daily
            :param datetime end: Date/time of end of the worker

            **Optional**

            :param str url: URL to read more about the worker
            :param datetime begin: Date/time of begin of the worker
            :param string payment_type: ["burn", "refund", "vesting"] (default: "vesting")
            :param int pay_vesting_period_days: Days of vesting (default: 0)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        from PythonMiddlewarebase.transactions import timeformat
        # assert isinstance(daily_pay, Amount)
        # assert daily_pay["symbol"] == "BTS"
        if not begin:
            begin = datetime.utcnow().strftime(timeformat)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)

        if payment_type == "destroy":
            initializer = [0, {}]
        elif payment_type == "vesting":
            initializer = [
                1, {"pay_vesting_period_days": pay_vesting_period_days}
            ]
        elif payment_type == "burn":
            initializer = [2, {}]
        elif payment_type == "ssuance":
            initializer = [3, {}]
        else:
            raise ValueError(
                'payment_type not in ["burn", "refund", "vesting"]')

        op = operations.Worker_create(**{
            "beneficiary": account["id"],
            # "owner": account["id"],
            # "work_begin_date": begin.strftime(timeformat),
            "work_begin_date": begin,
            # "work_end_date": end.strftime(timeformat),
            "work_end_date": end,
            "daily_pay": int(daily_pay),
            "name": name,
            "describe": describe,
            "initializer": initializer
        })
        return self.finalizeOp(op, account, "active")

    def balance_claim(self, balance_to_claim, balance_owner_key, amount, asset, account=None):
        if not balance_to_claim:
            raise ValueError("You need to provide balance to claim")
        if not balance_owner_key:
            raise ValueError("You need to provide balance owner key")
        if not (amount or asset):
            raise ValueError("You need to provide amount or asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Balance_claim(**{

            "deposit_to_account": account["id"],
            "balance_to_claim": balance_to_claim,
            "balance_owner_key": balance_owner_key,
            "total_claimed": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })
        return self.finalizeOp(op, account, "active")

    def asset_claim_fees(self, amount, asset, account=None):
        if not (amount or asset):
            raise ValueError("You need to provide amount or asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        op = operations.Asset_claim_fees(**{

            "issuer": account["id"],
            "amount_to_claim": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def bid_collateral(self, amount, asset, debt_amount, debt_asset, account=None):
        if not (amount or asset):
            raise ValueError("You need to provide amount or asset")
        if not (debt_amount or debt_asset):
            raise ValueError("You need to provide debt_amount or debt_asset")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        amount = Amount(amount, asset, graphene_instance=self)
        _amount = Amount(debt_amount, debt_asset, graphene_instance=self)
        op = operations.Bid_collateral(**{

            "bidder": account["id"],
            "additional_collateral": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "debt_covered": {
                "amount": int(_amount),
                "asset_id": _amount.asset["id"]
            },
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def create_contract(self, name, data, con_authority, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Contract_create(**{

            "owner": account["id"],
            "name": name,
            "data": data,
            "contract_authority": con_authority,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def call_contract_function(self, contract, function, value_list, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        contract = Contract(contract, graphene_instance=self)
        # import re
        # if re.match("^1\.16\.[0-9]*$", contract):
        #     account = self.graphene.rpc.get_objects([self.name])[0]
        # else:
        #     account = self.graphene.rpc.lookup_account_names([self.name])[0]
        op = operations.Call_contract_function(**{

            "caller": account["id"],
            "contract_id": contract["id"],
            "function_name": function,
            "value_list": value_list,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def register_nh_asset_creator(self, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Register_nh_asset_creator(**{

            "fee_paying_account": account["id"]
        })
        return self.finalizeOp(op, account["name"], "active")

    def create_world_view(self, world_view, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        if not world_view:
            raise ValueError("You need to provide a world_view")
        account = Account(account, graphene_instance=self)
        op = operations.Create_world_view(**{

            "fee_paying_account": account["id"],
            "world_view": world_view
        })
        return self.finalizeOp(op, account["name"], "active")

    def proposal_create(self, proposed_ops, account=None):
        account = Account(account, graphene_instance=self)
        op = operations.Proposal_create(**{

            "fee_paying_account": account["id"],
            "proposed_ops": proposed_ops,
            # "expiration_time": formatTimeFromNow(60*60),
            "expiration_time": transactions.formatTimeFromNow(self.proposal_expiration),
            "review_period_seconds": self.proposal_review,
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active")

    def relate_world_view(self, world_view, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        if not world_view:
            raise ValueError("You need to provide a world view")
        account = Account(account, graphene_instance=self)
        # view_owner = Account(view_owner)
        view_owner = self.rpc.get_object(self.lookup_world_view(world_view)[
                                         0]["world_view_creator"])["creator"]

        # op = operations.Proposal_create(**{
        #     "fee": {"amount": 0,
        #             "asset_id": "1.3.0"
        #             },
        #     "fee_paying_account": account["id"],
        #     "expiration_time": transactions.formatTimeFromNow(self.proposal_expiration),
        #     # "expiration_time": "2019-02-23T00:00:00",
        #     "proposed_ops": [{
        op = operations.Relate_world_view(**{
            "related_account": account["id"],
            "world_view": world_view,
            "view_owner": view_owner
        })
        # "extensions": []
        # })
        return self.finalizeOp(op, account["name"], "active")

    def create_nh_asset(self, owner, assetID, world_view, describe, account=None):
        if (not assetID) or (not world_view):
            raise ValueError("You need to provide an assetID and an itemVER")
        if not describe:
            raise ValueError("You need to provide an itemData")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")

        # if not isinstance(describe, dict):
        #     raise ValueError("The describe type need to be a dict")
        # describe = json.dumps(describe)
        account = Account(account, graphene_instance=self)
        # assetID = Asset(assetID)["id"]
        owner_account = (Account(owner, graphene_instance=self)
                         if owner else Account(account, graphene_instance=self))
        op = operations.Create_nh_asset(**{

            "owner": owner_account["id"],
            "fee_paying_account": account["id"],
            "asset_id": assetID,
            "world_view": world_view,
            "base_describe": describe
        })
        return self.finalizeOp(op, account, "active")

    def relate_nh_asset(self, parent=None, child=None, contract=None, relate=True, account=None):
        # if not nh_asset_creator:
        #     raise ValueError("You need to provide asset creater")
        # if not parent:
        #     parent = None
        # if not child:
        #     child = None
        # if not contract:
        #     contract = None
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide account")
        account = Account(account, graphene_instance=self)
        # nh_asset_creator = Account(nh_asset_creator)

        op = operations.Relate_nh_asset(**{

            "nh_asset_creator": account["id"],
            "parent": parent,
            "child": child,
            "contract": contract,
            "relate": relate
        })
        return self.finalizeOp(op, account, "active")

    def delete_nh_asset(self, asset_id, account=None):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Delete_nh_asset(**{

            "fee_paying_account": account["id"],
            "nh_asset": asset_id
        })
        return self.finalizeOp(op, account, "active")

    def transfer_nh_asset(self, to, nh_asset_id, account=None):
        if not to:
            raise ValueError("You need to provide a receive account")
        if not nh_asset_id:
            raise ValueError("You need to provide nh asset id")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        to_account = Account(to, graphene_instance=self)
        account = Account(account, graphene_instance=self)
        op = operations.Transfer_nh_asset(**{

            "from": account["id"],
            "to": to_account["id"],
            "nh_asset": nh_asset_id
        })
        return self.finalizeOp(op, account, "active")

    def create_nh_asset_order(self, otcaccount, pending_order_fee_amount, pending_order_fee_asset, nh_asset, memo, price_amount, price, account=None):
        if not otcaccount:
            raise ValueError("You need to providea otcAccount")
        if not nh_asset:
            raise ValueError("You need to provide a nh_asset")
        if not pending_order_fee_amount:
            raise ValueError("You need to provide pending_order_fee")
        if not price:
            raise ValueError("You need to provide price")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        otcaccount = Account(otcaccount, graphene_instance=self)
        pending_order_fee = Amount(
            pending_order_fee_amount, pending_order_fee_asset, graphene_instance=self)
        price = Amount(price_amount, price, graphene_instance=self)
        op = operations.Create_nh_asset_order(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "seller": account["id"],
            "otcaccount": otcaccount['id'],
            "pending_orders_fee": {
                "amount": int(pending_order_fee),
                "asset_id": pending_order_fee.asset["id"]
            },
            "nh_asset": nh_asset,
            "memo": memo,
            "price": {
                "amount": int(price),
                "asset_id": price.asset["id"]
            },
            "expiration": transactions.formatTimeFromNow(self.proposal_expiration)
        })
        return self.finalizeOp(op, account, "active")

    def cancel_nh_asset_order(self, order, account=None):
        if not order:
            raise ValueError("You need to provide a orderId")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Cancel_nh_asset_order(**{

            "fee_paying_account": account["id"],
            "order": order,
            "extensions": {}
        })

        return self.finalizeOp(op, account, "active")

    def fill_nh_asset_order(self, order, account=None):
        if not order:
            raise ValueError("You need to provide a order")
        # if not seller:
        #     raise ValueError("You need to provide a seller")
        # if not nh_asset:
        #     raise ValueError("You need to provide a nh_asset")
        # if not(price_amount) or not(price_asset_id) or not(price_asset_symbol):
        #     raise ValueError("You need to provide price_amount,price_asset_id amd price_asset_symbol")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        order_info = self.rpc.get_object(order)
        sell_account = order_info["seller"]
        nh_asset = order_info["nh_asset_id"]
        price_amount = order_info["price"]["amount"]
        price_asset_id = order_info["price"]["asset_id"]
        price_asset_symbol = order_info["asset_qualifier"]
        # sell_account = Account(seller)
        op = operations.Fill_nh_asset_order(**{

            "fee_paying_account": account["id"],
            "order": order,
            "seller": sell_account,
            "nh_asset": nh_asset,
            "price_amount": price_amount,
            "price_asset_id": price_asset_id,
            "price_asset_symbol": price_asset_symbol,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def create_file(self, filename, content, account=None):
        if not filename:
            raise ValueError("You need to provide a file's name")
        if not content:
            raise ValueError("You need to provide a file's content")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Create_file(**{

            "file_owner": account["id"],
            "file_name": filename,
            "file_content": content
        })
        return self.finalizeOp(op, account, "active")

    def add_file_relate_account(self, file, related_account, account=None):
        if not file:
            raise ValueError("You need to provide a file's id")
        if not related_account:
            raise ValueError("You need to provide a related account")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        relate = []
        # if not isinstance(related_account, (list, set)):
        #     relate.append(related_account)
        #     # related_account = set(related_account)
        # else:
        #     relate = related_account
        file_id = self.get_file(file)["id"]
        for rel in related_account:
            relate_id = Account(rel)["id"]
            relate.append(relate_id)
        account = Account(account, graphene_instance=self)
        op = operations.Add_file_relate_account(**{

            "file_owner": account["id"],
            "file_id": file_id,
            "related_account": relate
        })
        return self.finalizeOp(op, account, "active")

    def file_signature(self, file, signature, account=None):
        if not file:
            raise ValueError("You need to provide a file's id")
        if not signature:
            raise ValueError("You need to provide a file's signature content")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        file_id = self.get_file(file)["id"]
        op = operations.File_signature(**{

            "signature_account": account["id"],
            "file_id": file_id,
            "signature": signature
        })
        return self.finalizeOp(op, account, "active")

    def relate_parent_file(self, parent_file, sub_file):
        if not parent_file:
            raise ValueError("You need to provide a parent file")
        if not sub_file:
            raise ValueError("You need to provide a sub file")
        # if not account:
        #     if "default_account" in config:
        #         account = config["default_account"]
        #     else:
        #         raise ValueError("You need to provide an account")
        # account = Account(account)
        # parent_file_owner = Account(parent_file_owner)
        parent_file_owner, parent_file_id = self.get_file(
            parent_file)["file_owner"], self.get_file(parent_file)["id"]
        sub_file_owner, sub_file_id = self.get_file(
            sub_file)["file_owner"], self.get_file(sub_file)["id"]
        # op = operations.Proposal_create(**{
        #     "fee": {"amount": 0,
        #             "asset_id": "1.3.0"
        #             },
        #     "fee_paying_account": sub_file_owner,
        #     "expiration_time": formatTimeFromNow(60*60*24),
        #     "proposed_ops": [{
        op = operations.Relate_parent_file(**{
            "sub_file_owner": sub_file_owner,
            "parent_file": parent_file_id,
            "parent_file_owner": parent_file_owner,
            "sub_file": sub_file_id
        })
        #     "extensions": []
        # })
        # op = operations.Relate_parent_file(**{
        #
        #     "sub_file_owner": account["id"],
        #     "parent_file": parentfile,
        #     "parent_file_owner": parent_file_owner["id"],
        #     "sub_file": subfile
        # })
        return self.finalizeOp(op, sub_file_owner, "active")

    def revise_contract(self, contract, data, account=None):
        if not contract:
            raise ValueError("You need to provide contract")
        if not data:
            raise ValueError("You need to provide contract data")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        contract = Contract(contract, graphene_instance=self)
        op = operations.Revise_contract(**{

            "reviser": account["id"],
            "contract_id": contract["id"],
            "data": data,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def crontab_create(self, crontab_ops, start_time, interval, times, account=None):
        if not (crontab_ops or start_time or interval or times):
            raise ValueError("You need to provide some args")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Crontab_create(**{

            "crontab_creator": account["id"],
            "crontab_ops": crontab_ops,
            "start_time": start_time,
            "execute_interval": interval,
            "scheduled_execute_times": times,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def crontab_cancel(self, task, account=None):
        if not task:
            raise ValueError("You need to provide a task")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Crontab_cancel(**{

            "fee_paying_account": account["id"],
            "task": task,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def crontab_recover(self, crontab, restart_time, account=None):
        if not crontab:
            raise ValueError("You need to provide crontab id")
        if not restart_time:
            raise ValueError("You need to provide crontab restart time")
        if not account:
            if "default_account" in config:
                account = config["default_account"]
            else:
                raise ValueError("You need to provide an account")
        account = Account(account, graphene_instance=self)
        op = operations.Crontab_recover(**{

            "crontab_owner": account["id"],
            "crontab": crontab,
            "restart_time": restart_time,
            "extensions": {}
        })
        return self.finalizeOp(op, account, "active")

    def lookup_world_view(self, world_view):
        if not world_view:
            raise ValueError("You need to provide world_view")
        world_view_list = []
        world_view_list.append(world_view)
        world_view = self.rpc.lookup_world_view(world_view_list)
        return world_view

    def lookup_nh_asset(self, nh_asset):
        if not nh_asset:
            raise ValueError("You need to provide nh_asset")
        nh_asset_list = []
        nh_asset_list.append(nh_asset)
        nh_asset = self.rpc.lookup_nh_asset(nh_asset_list)
        return nh_asset

    def list_nh_asset_by_creator(self, nh_asset_creator, page_size, page):
        if not nh_asset_creator:
            raise ValueError("You need to provide nh_asset_creator")
        nh_asset_creator = Account(
            nh_asset_creator, graphene_instance=self)["id"]
        list_nh_asset = self.rpc.list_nh_asset_by_creator(
            nh_asset_creator, page_size, page)
        return list_nh_asset

    def list_account_nh_asset(self, nh_asset_owner, world_view, page_size, page, _type=3):
        if not (nh_asset_owner or world_view):
            raise ValueError(
                "You need to provide nh_asset_owner or world_view")
        owner = Account(nh_asset_owner, graphene_instance=self)["id"]
        world_view_list = []
        world_view_list.append(world_view)
        account_nh_asset = self.rpc.list_account_nh_asset(
            owner, world_view_list, page_size, page, _type)
        return account_nh_asset

    def get_nh_creator(self, nh_creator):
        if not nh_creator:
            raise ValueError("You need to provide nh_creator")
        nh_creator = Account(nh_creator, graphene_instance=self)["id"]
        nh_creator = self.rpc.get_nh_creator(nh_creator)
        return nh_creator

    def list_nh_asset_order(self, asset, world_view, base_describe="", page_size=10, page=1, is_ascending_order=True):
        if not asset:
            raise ValueError("You need to provide asset symbol or asset id")
        if not world_view:
            raise ValueError("You need to provide world_view")
        list_nh_asset_order = self.rpc.list_nh_asset_order(
            asset, world_view, base_describe, page_size, page, is_ascending_order)
        return list_nh_asset_order

    def list_account_nh_asset_order(self, nh_asset_order_owner, page_size, page):
        if not nh_asset_order_owner:
            raise ValueError("You need to provide order_owner")
        account = Account(nh_asset_order_owner, graphene_instance=self)["id"]
        list_account_nh_asset_order = self.rpc.list_account_nh_asset_order(
            account, page_size, page)
        return list_account_nh_asset_order

    def get_file(self, file):
        if not file:
            raise ValueError("You need to provide a file name")
        file_info = self.rpc.lookup_file(file)
        return file_info

    def suggest_key(self):
        brain = BrainKey()
        priv_key = str(brain.get_private_key())
        active_key = str(brain.get_public_key())
        owner_key = str(BrainKey().get_public_key())
        key = {"owner_key": owner_key,
               "active_key": active_key, "private_key": priv_key}
        return key
