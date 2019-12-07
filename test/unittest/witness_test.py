import unittest

from config import Config


class WitnessTestCase(unittest.TestCase):
    def testCreateWitness(self):
        params = {
            "account_name": "1.2.26",
            "url": "",
            "key": "COCOS8mv3AjCiVaLhp1varnw7E4ztSbykA1D7Wko3hQweKF5yMV2vN7"
        }
        gph = Config().gph
        try:
            print("CreateWitness:", gph.create_witness(**params))
        except Exception as e:
            print(repr(e))

    def testUpdateWitness(self):
        params = {
            "witness_identifier": "1.2.26",
            "work_status": True,
            "url": "www.12.com",
            "key": "COCOS8mv3AjCiVaLhp1varnw7E4ztSbykA1D7Wko3hQweKF5yMV2vN7"
        }
        gph = Config().gph
        try:
            print("UpdateWitness:", gph.update_witness(**params))
        except Exception as e:
            print(repr(e))

    def testApproveWitness(self):
        params = {
            "witnesses": ["testaccount7"],
            "vote_type": 1,
            "vote_amount": 10,
            "vote_asset": "1.3.0",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("ApproveWitness:", gph.approve_witness(**params))
        except Exception as e:
            print(repr(e))

    def testDisApproveWitness(self):
        params = {
            "witnesses": ["testaccount7"],
            "vote_type": 1,
            "vote_amount": 10,
            "vote_asset": "1.3.0",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("DisApproveWitness:", gph.disapprove_witness(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    case1 = WitnessTestCase("testCreateWitness")
    case1()
    case2 = WitnessTestCase("testUpdateWitness")
    case2()
    case3 = WitnessTestCase("testApproveWitness")
    case3()
    case4 = WitnessTestCase("testDisApproveWitness")
    case4()