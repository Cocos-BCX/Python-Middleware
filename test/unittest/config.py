from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config

'''
test1
{
  "brain_priv_key": "WAKENER PAXIUBA UNCOWED CAMISIA REWEAVE DARDAOL SAFFLOW ADAWE SNOWL MUSCOSE RAS STYLITE VINTRY AXION TARHOOD VIBRATE",
  "wif_priv_key": "5JAt3WmMCqQvAqqq4Mr7ZisN8ztrrPZCTHCN7f8Vrx8j1cHY4hy",
  "address_info": "COCOSMHfYkwN2xezycrrhcijnXwwZn8s1zd89m",
  "pub_key": "COCOS8m1rD2w5q2fJB89MaNJRhnYppdrkEtWB71FLMjfL2xXhCnXAqn"
}
'''

class Config():
    node_address = "ws://127.0.0.1:8049"
    blocking = True
    wifkey = "5JAt3WmMCqQvAqqq4Mr7ZisN8ztrrPZCTHCN7f8Vrx8j1cHY4hy"
    pub_key = ""
    wallet_pwd = "ping"
    config["default_account"] = "test1"
    def __init__(self, **kwargs):
        print("kwargs:", kwargs)

        self.gph = Graphene(node=self.node_address, blocking=self.blocking, **kwargs)
        set_shared_graphene_instance(self.gph)
        if self.gph.wallet.created() is False:
            self.gph.wallet.newWallet(self.wallet_pwd)
        self.gph.wallet.unlock(self.wallet_pwd)
        try:
            self.gph.wallet.addPrivateKey(self.wifkey)
        except:
            pass
