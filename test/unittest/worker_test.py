import unittest

from config import Config


class WorkerTestCase(unittest.TestCase):
    def testCreateWorker(self): #begin time should > expirtion_time(3600), need a half committee approve proposal --->allow_execution:True
        params = {
            "name": "worked",
            "daily_pay": 100,
            "end": "2019-08-09T04:02:00",
            "describe": "sdfasdf",
            "begin": "2019-08-08T04:02:00",
            "payment_type": "vesting",
            "account": "1.2.23"
        }
        gph = Config(proposer="1.2.23",proposal_review=1800).gph
        try:
            print("CreateWorker:", gph.create_worker(**params))
        except Exception as e:
            print(repr(e))

    def testApproveProposal(self):
        params = {
            "proposal_ids": ["1.10.14"],
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("ApproveProposal:", gph.approveproposal(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    # case1 = WorkerTestCase("testCreateWorker")
    # case1()
    case2 = WorkerTestCase("testApproveProposal")
    case2()