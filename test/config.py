from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config

class Config():
    node_address = "ws://xxxxxxxxx"
    blocking = True
    wifkey = "xxxxxxx"
    wallet_pwd = "xxxxxx"
    config["default_account"] = "xxxxxx"
    def __init__(self, **kwargs):
        # print("kwargs:", kwargs)

        self.gph = Graphene(node=self.node_address, blocking=self.blocking, **kwargs)
        set_shared_graphene_instance(self.gph)
        if self.gph.wallet.created() is False:
            self.gph.wallet.newWallet(self.wallet_pwd)
        self.gph.wallet.unlock(self.wallet_pwd)
        try:
            self.gph.wallet.addPrivateKey(self.wifkey)
        except:
            pass
