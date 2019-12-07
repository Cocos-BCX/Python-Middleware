import unittest

from config import Config


class CommitteeTestCase(unittest.TestCase):
    def testCreateCommittee(self):
        params = {
            "url": " ",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CreateCommittee:", gph.committee_member_create(**params))
        except Exception as e:
            print(repr(e))

    def testUpdateCommittee(self):
        params = {
            "work_status": True,
            "new_url": "www.1234.com",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("UpdateCommittee:", gph.committee_member_update(**params))
        except Exception as e:
            print(repr(e))

    def testApproveCommittee(self):
        params = {
            "committees": ["testaccount7"],
            "vote_type": 0,
            "vote_amount": 10,
            "vote_asset": "1.3.0",
            "account": "1.2.16"
        }
        gph = Config().gph
        try:
            print("ApproveCommittee:", gph.approve_committee(**params))
        except Exception as e:
            print(repr(e))

    def testDisApproveCommittee(self):
        params = {
            "committees": ["testaccount7"],
            "vote_type": 0,
            "vote_amount": 1,
            "vote_asset": "1.3.0",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("DisApproveCommittee:", gph.disapprove_committee(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    # case1 = CommitteeTestCase("testCreateCommittee")
    # case1()
    # case2 = CommitteeTestCase("testUpdateCommittee")
    # case2()
    case3 = CommitteeTestCase("testApproveCommittee")
    case3()
    # case4 = CommitteeTestCase("testDisApproveCommittee")
    # case4()