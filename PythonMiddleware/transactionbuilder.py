from .account import Account
from .blockchain import Blockchain
from PythonMiddlewarebase.objects import Operation
from PythonMiddlewarebase.account import PrivateKey, PublicKey
from PythonMiddlewarebase.signedtransactions import Signed_Transaction
from PythonMiddlewarebase import transactions, operations
from .exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError
)
from PythonMiddleware.instance import shared_graphene_instance
import logging
from pprint import pprint
log = logging.getLogger(__name__)


class TransactionBuilder(dict):
    """ This class simplifies the creation of transactions by adding
        operations and signers.
    """

    def __init__(self, tx={}, graphene_instance=None):
        self.graphene = graphene_instance or shared_graphene_instance()
        self.clear()
        # print("tx>>", tx)
        if not isinstance(tx, dict):
            raise ValueError("Invalid TransactionBuilder Format")
        super(TransactionBuilder, self).__init__(tx)

    def appendOps(self, ops):
        """ Append op(s) to the transaction builder

            :param list ops: One or a list of operations
        """
        if isinstance(ops, list):
            self.ops.extend(ops)
        else:
            self.ops.append(ops)

    def appendSigner(self, account, permission):
        """ Try to obtain the wif key from the wallet by telling which account
            and permission is supposed to sign the transaction
        """
        def fetchkeys(account, perm, level=0):
            if level > 2:
                return []
            r = []
            # print("key_auths>>>:", account[perm]["key_auths"])
            for authority in account[perm]["key_auths"]:
                # print("authority>>>:" ,authority)
                wif = self.graphene.wallet.getPrivateKeyForPublicKey(authority[0])
                # print("wif>>>:", wif)
                if wif:
                    r.append([wif, authority[1]])

            if sum([x[1] for x in r]) < required_treshold:
                # go one level deeper
                # print("3")
                for authority in account[perm]["account_auths"]:
                    auth_account = Account(authority[0], graphene_instance=self.graphene)
                    r.extend(fetchkeys(auth_account, perm, level + 1))

            # print("r>>>:", r)
            return r

        assert permission in ["active", "owner"], "Invalid permission"

        # print("account>>>:", account)
        # print("available_signers>>>:", self.available_signers)
        # print("permission>>>:", permission)

        if account not in self.available_signers:
            # is the account an instance of public key?
            if isinstance(account, PublicKey):
                self.wifs.append(
                    self.graphene.wallet.getPrivateKeyForPublicKey(
                        str(account)
                    )
                )
                # print("1")
            else:
                account = Account(account, graphene_instance=self.graphene)
                required_treshold = account[permission]["weight_threshold"]
                keys = fetchkeys(account, permission)
                if permission != "owner":
                    keys.extend(fetchkeys(account, "owner"))
                self.wifs.extend([x[0] for x in keys])
                # print("wifs>>>:", self.wifs)
                # print("2")
                # print("keys:>>>", keys)

            self.available_signers.append(account)
        # print("available_signers>>>:", self.available_signers)

    def appendWif(self, wif):
        """ Add a wif that should be used for signing of the transaction.
        """
        if wif:
            try:
                PrivateKey(wif)
                self.wifs.append(wif)
            except:
                raise InvalidWifError

    def constructTx(self):
        """ Construct the actual transaction and store it in the class's dict
            store
        """
        if self.graphene.proposer:
            ops = [operations.Op_wrapper(op=o) for o in list(self.ops)]
            proposer = Account(
                self.graphene.proposer,
                graphene_instance=self.graphene
            )
            ops = operations.Proposal_create(**{
                "fee_paying_account": proposer["id"],
                "expiration_time": transactions.formatTimeFromNow(
                    self.graphene.proposal_expiration),
                "proposed_ops": [o.json() for o in ops],
                "review_period_seconds": self.graphene.proposal_review,
                "extensions": []
            })
            ops = [Operation(ops)]
            # print("hahahaha")
        elif self.graphene.crontaber:
            ops = [operations.Op_wrapper(op=o) for o in list(self.ops)]
            crontab_creator = Account(self.graphene.crontaber, graphene_instance=self.graphene)
            ops = operations.Crontab_create(**{
                "crontab_creator": crontab_creator["id"],
                "crontab_ops": [o.json() for o in ops],
                "start_time": self.graphene.crontab_start_time,
                "execute_interval": self.graphene.crontab_execute_interval,
                "scheduled_execute_times": self.graphene.crontab_scheduled_execute_times,
                "extensions": {}
            })
            ops = [Operation(ops)]
        else:
            ops = [Operation(o) for o in list(self.ops)]
            # for i in ops:
                # print("ops>>>:", i)
        # print("ws:", self.graphene.rpc.get_required_fees([i.json() for i in ops], "1.3.0"))
        # ops = transactions.addRequiredFees(self.graphene.rpc, ops)
        # print("ops>>>:", ops)
        expiration = transactions.formatTimeFromNow(self.graphene.expiration)
        ref_block_num, ref_block_prefix = transactions.getBlockParams(self.graphene.rpc)

        tx = Signed_Transaction(
            ref_block_num=ref_block_num,
            ref_block_prefix=ref_block_prefix,
            expiration=expiration,
            operations=ops
        )
        # pprint(tx)
        super(TransactionBuilder, self).__init__(tx.json())

    def sign(self):
        """ Sign a provided transaction witht he provided key(s)

            :param dict tx: The transaction to be signed and returned
            :param string wifs: One or many wif keys to use for signing
                a transaction. If not present, the keys will be loaded
                from the wallet as defined in "missing_signatures" key
                of the transactions.
        """
        self.constructTx()

        # If we are doing a proposal, obtain the account from the proposer_id
        if self.graphene.proposer:
            proposer = Account(
                self.graphene.proposer,
                graphene_instance=self.graphene)
            self.wifs = []
            self.appendSigner(proposer["id"], "active")

        # We need to set the default prefix, otherwise pubkeys are
        # presented wrongly!
        if self.graphene.rpc:
            operations.default_prefix = self.graphene.rpc.chain_params["prefix"]
        elif "blockchain" in self:
            operations.default_prefix = self["blockchain"]["prefix"]
        # print("prefix>>>:", operations.default_prefix)
        try:
            signedtx = Signed_Transaction(**self.json())
        except:
            raise ValueError("Invalid TransactionBuilder Format")
        # print("self.wifs>>>>:", self.wifs)
        # print("signedtx>>>:", signedtx)

        if not any(self.wifs):
            raise MissingKeyError
        signedtx.sign(self.wifs, chain=self.graphene.rpc.chain_params)
        self["signatures"].extend(signedtx.json().get("signatures"))
        # print("signatures>>>>:", self["signatures"])

    def verify_authority(self):
        """ Verify the authority of the signed transaction
        """
        # print("verify_authority>>>:", self.graphene.rpc.verify_authority(self.json()))
        try:
            if not self.graphene.rpc.verify_authority(self.json()):
                raise InsufficientAuthorityError
        except Exception as e:
            raise e

    def broadcast(self):
        """ Broadcast a transaction to the graphene network

            :param tx tx: Signed transaction to broadcast
        """
        if "signatures" not in self or not self["signatures"]:
            self.sign()

        if self.graphene.nobroadcast:
            log.warning("Not broadcasting anything!")
            return self

        tx = self.json()
        # self.verify_authority()
        pprint(tx)
        # Broadcast
        try:
            tx_id = self.graphene.rpc.broadcast_transaction(tx, api="network_broadcast")
            # return tx_id
        except Exception as e:
            raise e

        self.clear()

        if self.graphene.blocking:
            chain = Blockchain(
                mode=("head" if self.graphene.blocking == "head" else "irreversible"),
                graphene_instance=self.graphene
            )
            tx = chain.awaitTxConfirmation(tx_id)
            return tx

        return self

    def clear(self):
        """ Clear the transaction builder and start from scratch
        """
        self.ops = []
        self.wifs = []
        self.pop("signatures", None)
        self.available_signers = []
        super(TransactionBuilder, self).__init__({})

    def addSigningInformation(self, account, permission):
        """ This is a private method that adds side information to a
            unsigned/partial transaction in order to simplify later
            signing (e.g. for multisig or coldstorage)

            FIXME: Does not work with owner keys!
        """
        self.constructTx()
        self["blockchain"] = self.graphene.rpc.chain_params

        if isinstance(account, PublicKey):
            self["missing_signatures"] = [
                str(account)
            ]
        else:
            accountObj = Account(account)
            authority = accountObj[permission]
            # We add a required_authorities to be able to identify
            # how to sign later. This is an array, because we
            # may later want to allow multiple operations per tx
            self.update({"required_authorities": {
                accountObj["name"]: authority
            }})
            for account_auth in authority["account_auths"]:
                account_auth_account = Account(account_auth[0])
                self["required_authorities"].update({
                    account_auth[0]: account_auth_account.get(permission)
                })

            # Try to resolve required signatures for offline signing
            self["missing_signatures"] = [
                x[0] for x in authority["key_auths"]
            ]
            # Add one recursion of keys from account_auths:
            for account_auth in authority["account_auths"]:
                account_auth_account = Account(account_auth[0])
                self["missing_signatures"].extend(
                    [x[0] for x in account_auth_account[permission]["key_auths"]]
                )
        # print("self", self)

    def json(self):
        """ Show the transaction as plain json
        """
        return dict(self)

    def appendMissingSignatures(self):
        """ Store which accounts/keys are supposed to sign the transaction

            This method is used for an offline-signer!
        """
        missing_signatures = self.get("missing_signatures", [])
        for pub in missing_signatures:
            wif = self.graphene.wallet.getPrivateKeyForPublicKey(pub)
            if wif:
                self.appendWif(wif)
