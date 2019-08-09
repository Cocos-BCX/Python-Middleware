from .account import PublicKey
from .chains import known_chains
from .signedtransactions import Signed_Transaction
from .operations import (
    Transfer,
    Asset_publish_feed,
    Asset_update,
    Op_wrapper,
    Proposal_create,
    Proposal_update,
    Limit_order_create,
    Limit_order_cancel,
    Call_order_update,
    Asset_fund_fee_pool,
    Override_transfer,
    Account_create,
)
from .objects import Asset
from binascii import hexlify, unhexlify
import struct
from datetime import datetime
import time
# from graphenebase.transactions import getBlockParams, formatTimeFromNow, timeformat
timeformat = '%Y-%m-%dT%H:%M:%S%Z'


def getBlockParams(ws):
    """ Auxiliary method to obtain ``ref_block_num`` and
        ``ref_block_prefix``. Requires a websocket connection to a
        witness node!
    """
    dynBCParams = ws.get_dynamic_global_properties()
    ref_block_num = dynBCParams["head_block_number"] & 0xFFFF
    ref_block_prefix = struct.unpack_from("<I", unhexlify(dynBCParams["head_block_id"]), 4)[0]
    return ref_block_num, ref_block_prefix


def formatTimeFromNow(secs=0):
    """ Properly Format Time that is `x` seconds in the future

     :param int secs: Seconds to go in the future (`x>0`) or the past (`x<0`)
     :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
     :rtype: str

    """
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeformat)

def addRequiredFees(ws, ops, asset_id="1.3.0"):
    """ Auxiliary method to obtain the required fees for a set of
        operations. Requires a websocket connection to a witness node!
    """
    fees = ws.get_required_fees([i.json() for i in ops], asset_id)
    # print("fees>>>:", fees)
    for i, d in enumerate(ops):
        if isinstance(fees[i], list):
            # Operation is a proposal
            ops[i].op.data["fee"] = Asset(
                amount=fees[i][0]["amount"],
                asset_id=fees[i][0]["asset_id"]
            )
            for j, _ in enumerate(ops[i].op.data["proposed_ops"].data):
                ops[i].op.data["proposed_ops"].data[j].data["op"].op.data["fee"] = (
                    Asset(
                        amount=fees[i][1][j]["amount"],
                        asset_id=fees[i][1][j]["asset_id"]))
        else:
            # Operation is a regular operation
            ops[i].op.data["fee"] = Asset(
                amount=fees[i]["amount"],
                asset_id=fees[i]["asset_id"]
            )
    return ops
