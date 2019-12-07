import unittest

from config import Config


class BalanceClaimTestCase(unittest.TestCase):
    def testClaimBalance(self):
        params = {
            "balance_to_claim": "1.15.0",
            "balance_owner_key": "COCOS7yE9skpBAirth3eSNMRtwq1jYswEE3uSbbuAtXTz88HtbpQsZf",
            "amount": 5000000000000,
            "asset": "1.3.0",
            "account": "1.2.16"
        }
        gph = Config().gph
        try:
            print("ClaimBalance:", gph.balance_claim(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    case1 = BalanceClaimTestCase("testClaimBalance")
    case1()