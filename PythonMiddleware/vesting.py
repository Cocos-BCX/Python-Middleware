from .instance import shared_graphene_instance
from .account import Account
from .exceptions import VestingBalanceDoesNotExistsException
import logging
log = logging.getLogger(__name__)


class Vesting(dict):
    """ Read data about a Vesting Balance in the chain

        :param str id: Id of the vesting balance
        :param bitshares bitshares_instance: BitShares() instance to use when accesing a RPC

    """
    def __init__(
        self,
        id,
        graphene_instance=None,
    ):
        self.id = id

        self.graphene = graphene_instance or shared_graphene_instance()
        self.refresh()

    def refresh(self):
        a, b = self.id.split(".")[0], self.id.split(".")[1]
        assert int(a) == 1 and int(b) == 13, "Valid vesting balances are 1.13.x"
        obj = self.graphene.rpc.get_objects([self.id])[0]
        super(Vesting, self).__init__(obj)

    @property
    def account(self):
        return Account(self["owner"])

    @property
    def claimable(self):
        from .amount import Amount
        if self["policy"][0] == 1:
            p = self["policy"][1]
            ratio = (
                (float(p["coin_seconds_earned"]) /
                    float(self["balance"]["amount"])) /
                float(p["vesting_seconds"])
            ) if float(p["vesting_seconds"]) > 0.0 else 1
            return Amount(self["balance"]) * ratio
        else:
            log.warning("This policy isn't implemented yet")
            return 0

    def claim(self, amount=None):
        return self.graphene.vesting_balance_withdraw(
            self["id"],
            amount=amount,
            account=self["owner"]
        )
