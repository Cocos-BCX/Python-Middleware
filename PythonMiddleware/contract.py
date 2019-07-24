from .instance import shared_graphene_instance
from .exceptions import ContractDoesNotExistsException


class Contract(dict):
    """ This class allows to easily access Contract data

        :param str Contract_name: Name of the Contract
        :param graphene.graphene.graphene graphene_instance: graphene instance
        :param bool lazy: Use lazy loading
        :param bool full: Obtain all Contract data including orders, positions, etc.
        :returns: Contract data
        :rtype: dictionary
        :raises graphene.exceptions.ContractDoesNotExistsException: if Contract does not exist

        Instances of this class are dictionaries that come with additional
        methods (see below) that allow dealing with an Contract and it's
        corresponding functions.

        .. code-block:: python

            from graphene.Contract import Contract
            Contract = Contract("init0")
            print(Contract)

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Contract.refresh()``.

    """

    contracts_cache = dict()

    def __init__(
        self,
        contract,
        lazy=False,
        graphene_instance=None
    ):
        self.cached = False
        self.graphene = graphene_instance or shared_graphene_instance()

        if isinstance(contract, Contract):
            # print("1:",contract)
            super(Contract, self).__init__(contract)
            self.name = contract["name"]
        elif isinstance(contract, str):
            # print("2:", contract)
            self.name = contract.strip()
        else:
            raise ValueError("Contract() expects a contract name, id or an instance of Contract")

        if not lazy:
            self.refresh()

        # if self.name in Contract.contracts_cache and not self.full:
        #     super(Contract, self).__init__(Contract.contracts_cache[self.name])
        #     self.cached = True
        # elif not lazy and not self.cached:
        #     self.refresh()
        #     self.cached = True

    def refresh(self):
        """ Refresh/Obtain an contract's data from the API server
        """
        # import re
        # if re.match(r"^1\.16\.[0-9]*$", self.name):
        #     contract = self.graphene.rpc.get_objects([self.name])[0]
        # else:
        #     contract = self.graphene.rpc.lookup_account_names([self.name])[0]
        try:
            contract = self.graphene.rpc.get_contract(self.name)
        except:
            raise ContractDoesNotExistsException(self.name)
        # if not contract:
        #     raise AccountDoesNotExistsException(self.name)

        super(Contract, self).__init__(contract)
        self._cache(contract)
        self.cached = True
        self.name = self["name"]

    def _cache(self, contract):
        # store in cache
        Contract.contracts_cache[contract["name"]] = contract

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Contract, self).__getitem__(key)

    def __repr__(self):
        return "<Contract: {}".format(self.name)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Contract, self).items()

    

