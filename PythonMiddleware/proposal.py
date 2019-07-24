from .instance import shared_graphene_instance
from .account import Account
from .exceptions import ProposalDoesNotExistException
import logging
log = logging.getLogger(__name__)


class Proposal(dict):
    """ Read data about a Proposal Balance in the chain

        :param str id: Id of the proposal
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC

    """
    def __init__(
        self,
        id,
        graphene_instance=None,
    ):
        self.graphene = graphene_instance or shared_graphene_instance()

        if isinstance(id, str):
            self.id = id
            self.refresh()
        elif isinstance(id, dict) and "id" in id:
            self.id = id["id"]
            super(Proposal, self).__init__(id)

    def refresh(self):
        a, b, c = self.id.split(".")
        assert int(a) == 1 and int(b) == 10, "Valid proposal ids are 1.10.x"
        proposal = self.graphene.rpc.get_objects([self.id])
        if not any(proposal):
            raise ProposalDoesNotExistException
        super(Proposal, self).__init__(proposal[0])

    def __repr__(self):
        return "<proposal %s>" % str(self.id)


class Proposals(list):
    """ Obtain a list of pending proposals for an account

        :param str account: Account name
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC
    """
    def __init__(self, account, graphene_instance=None):
        self.graphene = graphene_instance or shared_graphene_instance()

        account = Account(account)
        proposals = self.graphene.rpc.get_proposed_transactions(account["id"])

        super(Proposals, self).__init__(
            [
                Proposal(x, graphene_instance=self.graphene)
                for x in proposals
            ]
        )
