#: Operation ids
operations = {}
operations["transfer"] = 0 #pass
operations["limit_order_create"] = 1 #pass
operations["limit_order_cancel"] = 2 #pass
operations["call_order_update"] = 3 #pass
operations["fill_order"] = 4 # virtrual
operations["account_create"] = 5 #pass
operations["account_update"] = 6
operations["account_upgrade"] = 7 #pass
operations["asset_create"] = 8 #pass
operations["asset_update"] = 9 #pass
operations["asset_update_restricted"] = 10
operations["asset_update_bitasset"] = 11 #pass
operations["asset_update_feed_producers"] = 12 #pass
operations["asset_issue"] = 13 #pass
operations["asset_reserve"] = 14 #pass
operations["asset_settle"] = 15 #pass
operations["asset_global_settle"] = 16 #pass
operations["asset_publish_feed"] = 17 #pass
operations["witness_create"] = 18 #pass
operations["witness_update"] = 19 #pass
operations["proposal_create"] = 20 #pass
operations["proposal_update"] = 21 #pass
operations["proposal_delete"] = 22 #pass
operations["committee_member_create"] = 23 #pass
operations["committee_member_update"] = 24 #pass
operations["committee_member_update_global_parameters"] = 25 #defficult
operations["vesting_balance_create"] = 26 #pass
operations["vesting_balance_withdraw"] = 27 #pass
operations["worker_create"] = 28 #pass
operations["balance_claim"] = 29 #pass
operations["asset_settle_cancel"] = 30 # vitrual
operations["asset_claim_fees"] = 31 #pass
operations["bid_collateral"] = 32 # virtural
operations["execute_bid"] = 33 # vitrual
operations["contract_create"] = 34 #pass
operations["call_contract_function"] = 35 #pass
operations["temporary_authority_chang"] = 36
operations["register_nh_asset_creator"] = 37 #pass
operations["create_world_view"] = 38 #pass
operations["relate_world_view"] = 39 #pass
operations["create_nh_asset"] = 40 #pass
operations["delete_nh_asset"] = 41 #pass
operations["transfer_nh_asset"] = 42 #pass
operations["create_nh_asset_order"] = 43 #pass
operations["cancel_nh_asset_order"] = 44 #pass
operations["fill_nh_asset_order"] = 45 #pass
operations["create_file"] = 46 #pass
operations["add_file_relate_account"] = 47 #pass
operations["file_signature"] = 48 #pass
operations["relate_parent_file"] = 49 #pass
operations["revise_contract"] = 50 #pass
operations["crontab_create"] = 51 #pass
operations["crontab_cancel"] = 52 #pass
operations["crontab_recover"] = 53 #pass
operations["update_collateral_for_gas"] = 54 #pass


def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i
