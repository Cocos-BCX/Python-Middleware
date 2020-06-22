import unittest

from config import Config


class VestingBalanceTestCase(unittest.TestCase):
    def testCreateVestingBalance(self):
        params = {
            "owner": "testaccount6",
            "amount": 10000,
            "asset": "1.3.4",
            "start": "2019-08-6T10:00:00",
            "_type": "cdd",
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("CreateVestingBalance:", gph.vesting_balance_create(**params))
        except Exception as e:
            print(repr(e))

    def testWithdrawVestingBalance(self):
        params = {
            "vesting_id": "1.13.10",
            "amount": 1000,
            "asset": "1.3.4",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("DisApproveWitness:", gph.vesting_balance_withdraw(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    case1 = VestingBalanceTestCase("testCreateVestingBalance")
    case1()
    case2 = VestingBalanceTestCase("testWithdrawVestingBalance")
    case2()