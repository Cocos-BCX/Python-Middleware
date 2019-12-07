import unittest

from config import Config


class NhAssetTestCase(unittest.TestCase):
    def testRegisterNHCreator(self):
        params = {
            "account": "1.2.19"
        }
        gph = Config().gph
        try:
            print("RegisterNHAssetCreator:", gph.register_nh_asset_creator(**params))
        except Exception as e:
            print(repr(e))

    def testCreateWorldView(self):
        params = {
            "world_view": "SKY",
            "account": "1.2.19"
        }
        gph = Config().gph
        try:
            print("CreateWorldView:", gph.create_world_view(**params))
        except Exception as e:
            print(repr(e))

    def testRelateWorldView(self):
        params = {
            "world_view": "SKY",
            "account": "1.2.24"
        }
        gph = Config(proposer="1.2.24").gph
        try:
            print("RelateWorldView:", gph.relate_world_view(**params))
        except Exception as e:
            print(repr(e))

    def testApproveProposal(self):
        params = {
            "proposal_ids": ["1.10.15"],
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("ApproveProposal:", gph.approveproposal(**params))
        except Exception as e:
            print(repr(e))

    def testCreateNhAsset(self):
        params = {
            "owner": "1.2.19",
            "assetID": "COCOS",
            "world_view": "SKY",
            "describe": "bird-1",
            "account": "1.2.19"
        }
        gph = Config().gph
        try:
            print("CreateNHAsset:", gph.create_nh_asset(**params))
        except Exception as e:
            print(repr(e))

    def testTransferNhAsset(self):
        params = {
            "to": "1.2.25",
            "nh_asset_id": "4.2.2",
            "account": "1.2.24"
        }
        gph = Config().gph
        try:
            print("TransferNHAsset:", gph.transfer_nh_asset(**params))
        except Exception as e:
            print(repr(e))

    def testDeleteNhAsset(self):
        params = {
            "asset_id": "4.2.2",
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("DeleteNHAsset:", gph.delete_nh_asset(**params))
        except Exception as e:
            print(repr(e))

    def testCreateNhAssetOrder(self):
        params = {
            "otcaccount": "1.2.14",
            "pending_order_fee_amount": 5,
            "pending_order_fee_asset": "TESTCOIN",
            "nh_asset": "4.2.2",
            "memo": "nice toy",
            "price_amount": 100,
            "price": "COCOS",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CreateNHAssetOrder:", gph.create_nh_asset_order(**params))
        except Exception as e:
            print(repr(e))

    def testFillNhAssetOrder(self):
        params = {
            "order": "4.3.2",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("FillNHAssetOrder:", gph.fill_nh_asset_order(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    # case1 = NhAssetTestCase("testRegisterNHCreator")
    # case1()
    # case2 = NhAssetTestCase("testCreateWorldView")
    # case2()
    # case3 = NhAssetTestCase("testRelateWorldView")
    # case3()
    # case4 = NhAssetTestCase("testApproveProposal")
    # case4()
    case5 = NhAssetTestCase("testCreateNhAsset")
    case5()
    # case6 = NhAssetTestCase("testTransferNhAsset")
    # case6()
    # case7 = NhAssetTestCase("testDeleteNhAsset")
    # case7()
    # case8 = NhAssetTestCase("testCreateNhAssetOrder")
    # case8()
    # case9 = NhAssetTestCase("testFillNhAssetOrder")
    # case9()