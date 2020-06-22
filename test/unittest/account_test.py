import unittest

from config import Config


class AccountTestCase(unittest.TestCase):
    def testCreateAccount(self):
        params = {
            "account_name": "testaccount7",
            "password": "123456"
        }
        gph = Config().gph
        try:
            print("CreateAccount:", gph.create_account(**params))
        except Exception as e:
            print(repr(e))
            gph.wallet.removeAccount(None)

    def testTransfer(self):
        params = {
            "to" : "testaccount7",
            "amount": "10000000",
            "asset": "1.3.0",
            "memo" : ["123124134",0],
            "account" : "1.2.16"
        }
        gph = Config().gph
        try:
            print("Transfer:", gph.transfer(**params))
        except Exception as e:
            print(repr(e))

    def testUpgradeAccount(self):
        params = {
            "account" : "testaccount7"
        }
        gph = Config().gph
        try:
            print("UpgradeAccount:", gph.upgrade_account(**params))
        except Exception as e:
            print(repr(e))

if __name__ == "__main__":
    # case1 = AccountTestCase("testCreateAccount")
    # case1()
    case2 = AccountTestCase("testTransfer")
    case2()
    # case3 = AccountTestCase("testUpgradeAccount")
    # case3()