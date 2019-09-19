#: Operation ids
operations = {}
operations["transfer"] = 0
operations["limit_order_create"] = 1
operations["limit_order_cancel"] = 2
operations["call_order_update"] = 3
operations["fill_order"] = 4
operations["account_create"] = 5
operations["account_update"] = 6
#operations["account_whitelist"] = 7  #remove
operations["account_upgrade"] = 7
operations["asset_create"] = 8
operations["asset_update"] = 9
operations["asset_update_bitasset"] = 11
operations["asset_update_feed_producers"] = 12
operations["asset_issue"] = 13
operations["asset_reserve"] = 14
operations["asset_fund_fee_pool"] = 15
operations["asset_settle"] = 16
operations["asset_global_settle"] = 17
operations["asset_publish_feed"] = 18
operations["witness_create"] = 19
operations["witness_update"] = 20
operations["proposal_create"] = 21
operations["proposal_update"] = 22
operations["proposal_delete"] = 23
operations["withdraw_permission_create"] = 24
operations["withdraw_permission_update"] = 25
operations["withdraw_permission_claim"] = 26
operations["withdraw_permission_delete"] = 27
operations["committee_member_create"] = 28
operations["committee_member_update"] = 29
operations["committee_member_update_global_parameters"] = 30
operations["vesting_balance_create"] = 31
operations["vesting_balance_withdraw"] = 32
operations["worker_create"] = 33
# operations["custom"] = 35
# operations["assert"] = 36
operations["balance_claim"] = 34
# operations["override_transfer"] = 38
operations["transfer_to_blind"] = 35
operations["blind_transfer"] = 36
operations["transfer_from_blind"] = 37
operations["asset_settle_cancel"] = 38
operations["asset_claim_fees"] = 39
operations["fba_distribute"] = 40
operations["bid_collateral"] = 41
operations["execute_bid"] = 42
operations["contract_create"] = 43
operations["call_contract_function"] = 44
operations["temporary_authority_chang"] = 45
operations["register_nh_asset_creator"] = 46
operations["create_world_view"] = 47
operations["relate_world_view"] = 48
operations["create_nh_asset"] = 49
#operations["relate_nh_asset"] = 50 #remove
operations["delete_nh_asset"] = 50
operations["transfer_nh_asset"] = 51
operations["create_nh_asset_order"] = 52
operations["cancel_nh_asset_order"] = 53
operations["fill_nh_asset_order"] = 54
operations["create_file"] = 55
operations["add_file_relate_account"] = 56
operations["file_signature"] = 57
operations["relate_parent_file"] = 58
operations["revise_contract"] = 59
operations["crontab_create"] = 60
operations["crontab_cancel"] = 61
operations["crontab_recover"] = 62



# operations["register_game_developer"] = 50
# operations["create_game_version"] = 51
# operations["propose_relate_game_version"] = 52
# operations["create_game_item"] = 53
# operations["updata_game_item"] = 54
# operations["delete_game_item"] = 55
# operations["transfer_game_item"] = 56
# operations["create_game_item_order"] = 57
# operations["cancel_game_item_order"] = 58
# operations["fill_game_item_order"] = 59




def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i
