import unittest

from config import Config


class AssetTestCase(unittest.TestCase):
    def testCreateAsset(self):
        params = {
            "symbol": "TESTCOIN",
            "precision": 5,
            "common_options": {
                "max_supply": 10000000000000,
                "market_fee_percent": 0,
                "max_market_fee": 10000000000000,
                "issuer_permissions": 0,
                "flags": 0,
                "description": '',
                "extension": {}
            },
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CreateAsset:", gph.asset_create(**params))
        except Exception as e:
            print(repr(e))

    def testCreateBitAsset(self):
        params = {
            "symbol": "TESTBCOIN",
            "precision": 5,
            "common_options": {
                "max_supply": 10000000000000,
                "market_fee_percent": 0,
                "max_market_fee": 10000000000000,
                "issuer_permissions": 32,
                "flags": 0,
                "description": '',
                "extension": {}
            },
            "bitasset_opts": {
                "feed_lifetime_sec": 60*60,
                "minimum_feeds": 1,
                "force_settlement_delay_sec": 60*60,
                "force_settlement_offset_percent": 0,
                "maximum_force_settlement_volume": 3000,
                "short_backing_asset": "1.3.0",
                "extensions": {}
            },
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CreateBitAsset:", gph.asset_create(**params))
        except Exception as e:
            print(repr(e))

    def testUpdateAsset(self):
        params = {
            "asset": "1.3.3",
            "new_options": {
                "max_supply": 10000000000000,
                "market_fee_percent": 0,
                "max_market_fee": 10000000000000,
                "issuer_permissions": 1,
                "flags": 0,
                "description": '',
                "extension": {}
            },
            "issuer": None,
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("UpdateAsset:", gph.asset_update(**params))
        except Exception as e:
            print(repr(e))

    def testUpdateBitAsset(self):
        params = {
            "asset": "1.3.4",
            "new_options": {
                "feed_lifetime_sec": 60*60,
                "minimum_feeds": 1,
                "force_settlement_delay_sec": 60*60,
                "force_settlement_offset_percent": 0,
                "maximum_force_settlement_volume": 2000,
                "short_backing_asset": "1.3.0",
                "extensions": {}
            },
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("UpdateBitAsset:", gph.asset_update_bitasset(**params))
        except Exception as e:
            print(repr(e))

    def testIssueAsset(self):
        params = {
            "amount": 10000000,
            "asset": "1.3.3",
            "issue_to_account": "1.2.25",
            "memo": ["",0],
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("IssueAsset:", gph.asset_issue(**params))
        except Exception as e:
            print(repr(e))

    def testReserveAsset(self):
        params = {
            "amount": 1000000,
            "asset": "1.3.3",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("ReserveAsset:", gph.asset_reserve(**params))
        except Exception as e:
            print(repr(e))

    def testUpdateFeedProducers(self):
        params = {
            "asset": "1.3.4",
            "feed_producers": ["1.2.25"],
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("UpdateFeedProducers:", gph.asset_update_feed_producers(**params))
        except Exception as e:
            print(repr(e))

    def testPublishPriceFeed(self):
        params = {
            "symbol": "TESTBCOIN",
            "settlement_price": {
                "base": {
                    "amount": 1,
                    "asset_id": "1.3.4"
                    },
                "quote": {
                    "amount": 2,
                    "asset_id": "1.3.0"
                    }
                },
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("PublishPriceFeed:", gph.publish_price_feed(**params))
        except Exception as e:
            print(repr(e))

    def testBorrow(self):
        params = {
            "amount": 50,
            "asset": "1.3.0",
            "_amount": 10,
            "_asset": "1.3.4",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("BorrowAsset:", gph.call_order_update(**params))
        except Exception as e:
            print(repr(e))

    def testSettleAsset(self):
        params = {
            "amount": 2,
            "asset": "1.3.4",
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("SettleAsset:", gph.asset_settle(**params))
        except Exception as e:
            print(repr(e))

    def testGlobalSettleAsset(self):
        params = {
            "asset_to_settle": "1.3.4",
            "settle_price": {
                "base": {
                    "amount":1,
                    "asset_id":"1.3.4"
                    },
                "quote":{
                    "amount":2,
                    "asset_id":"1.3.0"
                    }
                },
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("GlobalSettleAsset:", gph.asset_global_settle(**params))
        except Exception as e:
            print(repr(e))

    def testCreateLimitOrder(self):
        params = {
            "amount": 1000,
            "asset": "1.3.3",
            "min_amount": 990,
            "min_amount_asset": "1.3.0" ,
            "fill": False,
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CreateLimitOrder:", gph.limit_order_create(**params))
        except Exception as e:
            print(repr(e))

    def testCancelLimitOrder(self):
        params = {
            "order_numbers": ["1.7.0"],
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CancelLimitOrder:", gph.limit_order_cancel(**params))
        except Exception as e:
            print(repr(e))

    def testAssetClaimFees(self):
        params = {
            "amount": 1,
            "asset": "1.3.1",
            "account": "1.2.16"
        }
        gph = Config().gph
        try:
            print("CancelLimitOrder:", gph.asset_claim_fees(**params))
        except Exception as e:
            print(repr(e))

if __name__ == "__main__":
    # case1 = AssetTestCase("testCreateAsset")
    # case1()
    # case2 = AssetTestCase("testCreateBitAsset")
    # case2()
    # case3 = AssetTestCase("testUpdateAsset")
    # case3()
    # case4 = AssetTestCase("testUpdateBitAsset")
    # case4()
    case5 = AssetTestCase("testIssueAsset")
    case5()
    # case6 = AssetTestCase("testReserveAsset")
    # case6()
    # case7 = AssetTestCase("testUpdateFeedProducers")
    # case7()
    # case8 = AssetTestCase("testPublishPriceFeed")
    # case8()
    # case9 = AssetTestCase("testBorrow")
    # case9()
    # case10 = AssetTestCase("testSettleAsset")
    # case10()
    # case11 = AssetTestCase("testGlobalSettleAsset")
    # case11()
    # case12 = AssetTestCase("testCreateLimitOrder")
    # case12()
    # case13 = AssetTestCase("testCancelLimitOrder")
    # case13()
    #case14 = AssetTestCase("testAssetClaimFees")
    #case14()