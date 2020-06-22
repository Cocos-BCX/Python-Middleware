import unittest

from config import Config


class FileTestCase(unittest.TestCase):
    def testCreateFile(self):
        params = {
            "filename": "hi-2",
            "content": "hi,2",
            "account": "1.2.24"
        }
        gph = Config().gph
        try:
            print("CreateFile:", gph.create_file(**params))
        except Exception as e:
            print(repr(e))

    def testAddFileRelateAccount(self):
        params = {
            "file": "hi-1",
            "related_account": ["1.2.25"],
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("AddFileRelateAccount", gph.add_file_relate_account(**params))
        except Exception as e:
            print(repr(e))

    def testSignatureFile(self):
        params = {
            "file": "hi-1",
            "signature": "ok!",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("SignatureFile:", gph.file_signature(**params))
        except Exception as e:
            print(repr(e))

    def testRelateParentFile(self):
        params = {
            "parent_file": "hi-1",
            "sub_file": "hi-2"
        }
        gph = Config(proposer="1.2.24").gph
        try:
            print("RelateParentFile:", gph.relate_parent_file(**params))
        except Exception as e:
            print(repr(e))

    def testApproveProposal(self):
        params = {
            "proposal_ids": ["1.10.18"],
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("ApproveProposal:", gph.approveproposal(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    # case1 = FileTestCase("testCreateFile")
    # case1()
    # case2 = FileTestCase("testAddFileRelateAccount")
    # case2()
    # case3 = FileTestCase("testSignatureFile")
    # case3()
    # case4 = FileTestCase("testRelateParentFile")
    # case4()
    case5 = FileTestCase("testApproveProposal")
    case5()