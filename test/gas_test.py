import unittest

from config import Config


class GasTestCase(unittest.TestCase):
    def testUpdateCollateralForGas(self):
        params = {
            "beneficiary": "1.2.26",
            "collateral": 1000,
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("UpdateCollateralForGas:", gph.update_collateral_for_gas(**params))
        except Exception as e:
            print(repr(e))

            

if __name__ == "__main__":
    case1 = GasTestCase("testUpdateCollateralForGas")
    case1()