from .instance import shared_graphene_instance
from .account import Account
from .exceptions import CommitteeMemberDoesNotExistsException


class Committee(dict):
    """ Read data about a Committee Member in the chain

        :param str member: Name of the Committee Member
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC
        :param bool lazy: Use lazy loading

    """
    def __init__(
        self,
        member,
        graphene_instance=None,
        lazy=False
    ):
        self.cached = False
        self.member = member

        self.graphene = graphene_instance or shared_graphene_instance()

        if not lazy:
            self.refresh()

    def refresh(self):
        account = Account(self.member)
        member = self.graphene.rpc.get_committee_member_by_account(account["id"])
        if not member:
            raise CommitteeMemberDoesNotExistsException
        super(Committee, self).__init__(member)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Committee, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Committee, self).items()

    @property
    def account(self):
        return Account(self.member)
