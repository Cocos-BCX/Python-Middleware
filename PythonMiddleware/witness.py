from PythonMiddleware.instance import shared_graphene_instance
from .account import Account
from .exceptions import WitnessDoesNotExistsException


class Witness(dict):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC

    """

    witness_cache = dict()

    def __init__(
        self,
        witness,
        lazy=False,
        graphene_instance=None,
    ):
        self.graphene = graphene_instance or shared_graphene_instance()
        self.cached = False

        if isinstance(witness, Witness):
            self.witness = witness["name"]
            super(Witness, self).__init__(witness)
            self.cached = True
            self._cache(witness)
        else:
            self.witness = witness
            if witness in Witness.witness_cache:
                super(Witness, self).__init__(Witness.witness_cache[witness])
                self.cached = True
            elif not lazy and not self.cached:
                self.refresh()

    def _cache(self, witness):
        # store in cache
        Witness.witness_cache[witness["id"]] = witness

    def refresh(self):
        parts = self.witness.split(".")
        if len(parts) == 3:
            a, b, _ = self.witness.split(".")
            assert int(a) == 1 and (int(b) == 6 or int(b) == 2), "Witness id's need to be 1.6.x or 1.2.x!"
            if int(b) == 6:
                witness = self.graphene.rpc.get_object(self.witness)
            else:
                witness = self.graphene.rpc.get_witness_by_account(self.witness)
        else:
            account = Account(self.witness)
            witness = self.graphene.rpc.get_witness_by_account(account["id"])
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness)
        self._cache(witness)

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Witness, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Witness, self).items()

    @property
    def account(self):
        return Account(self["witness_account"])

    def __repr__(self):
        return "<Witness %s>" % str(self.witness)


class Witnesses(list):
    """ Obtain a list of **active** witnesses and the current schedule

        :param graphene graphene_instance: graphene() instance to use when accesing a RPC
    """
    def __init__(self, graphene_instance=None):
        self.graphene = graphene_instance or shared_graphene_instance()
        self.schedule = self.graphene.rpc.get_object("2.12.0").get("current_shuffled_witnesses", [])

        super(Witnesses, self).__init__(
            [
                Witness(x, lazy=True, graphene_instance=self.graphene)
                for x in self.schedule
            ]
        )
