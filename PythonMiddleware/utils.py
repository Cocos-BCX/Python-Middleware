import time
from datetime import datetime
from PythonMiddleware.account import Account, AccountUpdate
from PythonMiddleware.storage import configStorage as config
from PythonMiddlewarebase.account import (
    PrivateKey,PublicKey
    )
import re
import uuid


timeFormat = '%Y-%m-%dT%H:%M:%S'


def formatTime(t):
    """ Properly Format Time for permlinks
    """
    if isinstance(t, float):
        return datetime.utcfromtimestamp(t).strftime(timeFormat)
    if isinstance(t, datetime):
        return t.strftime(timeFormat)


def formatTimeString(t):
    """ Properly Format Time for permlinks
    """
    return datetime.strptime(t, timeFormat)


def formatTimeFromNow(secs=0):
    """ Properly Format Time that is `x` seconds in the future

        :param int secs: Seconds to go in the future (`x>0`) or the
                         past (`x<0`)
        :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
        :rtype: str

    """
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeFormat)


def parse_time(block_time):
    """Take a string representation of time from the blockchain, and parse it into datetime object.
    """
    return datetime.strptime(block_time, timeFormat)




def getRegItem(str, patter, index):
    pattern = re.compile(patter)
    try:
        return pattern.match(str).group(index)
    except:
        return ' '


def str_to_list(listr):
    if not listr:
        return ''
    else:
        pattern = '\[(.*)\]'
        try:
            res = re.match(pattern, listr).group(1)
            if ',' in res:
                return res.split(',')
            else:
                return [res]
        except:
            return ''

# generate uuid
def get_uuid():
    salt=str(datetime.datetime.now())
    u1 = str(uuid.uuid3(uuid.NAMESPACE_DNS, salt))
    u2 = str(uuid.uuid3(uuid.NAMESPACE_DNS, salt))
    _uuid = (u1+u2).replace('-', '')[:50]
    return _uuid

# verify private key
# def priv_verify(account):
#     print("hahahahaha!")
#     try:
#         tag_account = Account(account)
#     except:
#         return make_response(jsonify({'msg': 'account name error ', 'data': [], 'code': '400', }))
#     w_secr = request.form.get('wsrc', '')
#     if not w_secr:
#         return make_response(jsonify({'msg': 'no key!', 'code': '400'}))
#     else:
#         w_secr = w_secr[8:-6]
#     try:    
#         gph.wallet.addPrivateKey(w_secr)
#     except:    
#         pass
#     try:
#         from_account_public = PrivateKey(w_secr, prefix=config["default_prefix"]).pubkey.__str__()
#     except :
#         return make_response(jsonify({'msg': 'PrivateKey error !', 'code': '400', })) 
#     find_account_auths = False
#     for temp_auths in tag_account["active"]["key_auths"]:
#         if from_account_public.lower() == temp_auths[0].lower():
#             find_account_auths = True
#             break
#     if find_account_auths == False:
#         print("find_account_auths:",find_account_auths)
#         if gph.wallet.getAccount(from_account_public)["name"] != config["default_account"]:
#             gph.wallet.removePrivateKeyFromPublicKey(from_account_public)
#         return make_response(jsonify({'msg': 'Mismatch between the user and the private key:'+from_account_public, 'code': '400', }))