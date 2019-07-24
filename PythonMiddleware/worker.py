from PythonMiddleware.instance import shared_graphene_instance
from .account import Account
from .exceptions import WorkerDoesNotExistsException


class Worker(dict):
    """ Read data about a worker in the chain

        :param str id: id of the worker
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC

    """

    def __init__(
        self,
        worker,
        lazy=False,
        graphene_instance=None,
    ):
        self.graphene = graphene_instance or shared_graphene_instance()
        self.cached = False

        if isinstance(worker, (Worker, dict)):
            self.identifier = worker["id"]
            super(Worker, self).__init__(worker)
            self.cached = True
        else:
            self.identifier = worker
            if not lazy:
                self.refresh()

    def refresh(self):
        parts = self.identifier.split(".")
        assert len(parts) == 3, "Worker() class needs a worker id"
        assert int(parts[0]) == 1 and int(parts[1]) == 14, "Worker id's need to be 1.14.x!"
        worker = self.graphene.rpc.get_object(self.identifier)
        if not worker:
            raise WorkerDoesNotExistsException
        super(Worker, self).__init__(worker)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Worker, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Worker, self).items()

    @property
    def account(self):
        return Account(self["worker_account"])

    def __repr__(self):
        return "<Worker %s>" % str(self.identifier)


class Workers(list):
    """ Obtain a list of workers for an account

        :param str account_name/id: Name/id of the account
        :param graphene graphene_instance: graphene() instance to use when accesing a RPC
    """
    def __init__(self, account_name, graphene_instance=None):
        self.graphene = graphene_instance or shared_graphene_instance()
        account = Account(account_name)
        self.workers = self.graphene.rpc.get_workers_by_account(account["id"])

        super(Workers, self).__init__(
            [
                Worker(x, lazy=True, graphene_instance=self.graphene)
                for x in self.workers
            ]
        )
