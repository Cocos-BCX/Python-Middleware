[中文](https://github.com/Cocos-BCX/Python-Middleware/blob/master/README_cn.md)

Python Middleware For Cocos—BCX
==============
* [Get Started](#Get-Started)
* [API User Guide](#API-User-Guide)
* [Main-Packages](#Main-Packages)

Get Started
---------------

We propose to build on Ubuntu 16.04 LTS (64 bit) with a default of python 3.5

**Manual installation:**

    cd python-PythonMiddleware
    python3 setup.py install --user
	
**Modify the blockchain parameters:**

    vi python-PythonMiddleware/PythonMiddlewarebase/chains.py # Edit blockchain related parameters
	
	```python
	known_chains = {
    "xxxxxx": {
        "chain_id": "xxxxxx",
        "core_symbol": "xxxxxx",
        "prefix": "xxxxxx"} # Code edited in chains.py
	```
	python3 setup.py install --user # Reload the python library

**Build the python script:**
```python
from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config
from pprint import pprint

nodeAddress = "ws://127.0.0.1:8000" # The RPC node to be connected
gph = Graphene(node=nodeAddress, blocking=True) #  Instantiated object
set_shared_graphene_instance(gph) # Set gph as a shared global instance

if gph.wallet.created() is False: # Create a local wallet database, if not, create a new wallet database
    gph.newWallet("xxxxxx")
gph.wallet.unlock("xxxxxx") # Unlock the wallet, if you need to interact with the wallet in subsequent operations, you need to unlock the wallet

config["default_prefix"] = gph.rpc.chain_params["prefix"] # Add default information to the wallet database
gph.wallet.addPrivateKey(privateKey) # Add a private key to the wallet
config["default_account"] = yourname # Add default information to the wallet database
```

API User Guide
-------------
* [Wallet](#Wallet)
* [Account](#Account)  
* [Asset](#Asset)  
* [NH Asset](#NH-Asset)  
* [Contract](#Contract)  
* [Market](#Market)  
* [Withness](#Withness)  
* [Committee](#Committee)  
* [Proposal](#Proposal)
----------

### Wallet

- [Python Middleware For Cocos—BCX](#python-middleware-for-cocosbcx)
  - [Get Started](#get-started)
  - [API User Guide](#api-user-guide)
  - [* Proposal](#proposal)
    - [Wallet](#wallet)
      - [Create a wallet by Graphene](#create-a-wallet-by-graphene)
      - [Create a wallet 1](#create-a-wallet-1)
      - [Create a wallet 2](#create-a-wallet-2)
      - [Unlock the wallet](#unlock-the-wallet)
      - [Lock the wallet](#lock-the-wallet)
      - [Modify wallet unlock password](#modify-wallet-unlock-password)
      - [Add private key to the wallet](#add-private-key-to-the-wallet)
      - [Get the private key of the wallet](#get-the-private-key-of-the-wallet)
      - [Remove the private key in the wallet](#remove-the-private-key-in-the-wallet)
      - [Encrypt wallet private key](#encrypt-wallet-private-key)
      - [Decrypt wallet private key](#decrypt-wallet-private-key)
      - [Get owner/active/memo private key](#get-owneractivememo-private-key)
      - [Get account ID through private key](#get-account-id-through-private-key)
      - [Get account ID through public key](#get-account-id-through-public-key)
      - [Get account info](#get-account-info)
      - [Get public key type](#get-public-key-type)
      - [Get all the accounts in the wallet](#get-all-the-accounts-in-the-wallet)
      - [Get all the public keys in the wallet](#get-all-the-public-keys-in-the-wallet)
      - [Wipe the private key in the wallet](#wipe-the-private-key-in-the-wallet)
  - [### Account](#account)
    - [Method：upgrade_account](#methodupgradeaccount)
    - [Asset](#asset)
    - [NH Asset](#nh-asset)
    - [Contract](#contract)
    - [Market](#market)
    - [Witness](#witness)
    - [Committee](#committee)
    - [Proposal](#proposal)
  - [Main-Packages](#main-packages)

#### Create a wallet by Graphene
    Method: newWallet(pwd)
	Function: Create a wallet
	Parameters: pwd: str type, wallet lock and unlock password
	Return value
    	> Succeed: None
	    > Fail: Corresponding error message
	Description:
    	> This interface is the wallet.newWallet interface encapsulation, but not a wallet api
	    > Essentially it is to call wallet to create a wallet.
    	> After the wallet is created, you can use the wallet instance directly through Graphene::instance.wallet to operate the interface of the wallet.

#### Create a wallet 1
    Method: newWallet(pwd)
    Function: Create a wallet
    Parameters: pwd: str type, wallet lock and unlock password
    Return value
        > Succeed: None
        > Fail: Corresponding error message

#### Create a wallet 2
    Method: create(pwd)
    Function: Create a wallet, Alias for newWallet()
    Parameters:
        > pwd: str type, wallet lock and unlock password
    Return value:
        > Succeed: None
        > Fail: Corresponding error message

#### Unlock the wallet
    Method: unlock(pwd=None)
    Function: Unlock the wallet 
    Parameters: pwd: str type, wallet lock and unlock password
    Return value:
        > Succeed: None
        > Fail: Corresponding error message

#### Lock the wallet
    Method: lock()
    Function: Lock the wallet
    Parameters: None
    Return value
        > Succeed: None
        > Fail: Corresponding error message


#### Modify wallet unlock password
	Method: changePassphrase(new_pwd)
    Function: Modify wallet unlock password
    Parameters: pwd: str type, the new password of the wallet
    Return value:
        > Succeed: None
        > Fail: Corresponding error message


#### Add private key to the wallet
    Method: addPrivateKey(wif)
    Function: Add private key to the wallet
    Parameters: wif: str type, private key
#### Get the private key of the wallet
    Method: getPrivateKeyForPublicKey(pub)
    Function: Get the private key corresponding to the public key in the wallet
    Parameters: wif: str type, public key
#### Remove the private key in the wallet 
    Method: removePrivateKeyFromPublicKey(pub)
    Function: Remove the private key corresponding to the public key in the wallet
    Parameters: wif: str type, public key


#### Encrypt wallet private key
    Method: encrypt_wif(wif)
    Function: Encrypt the private key
    Parameters: wif: str type, private key
    Return value: encrypted private key, str type
    
#### Decrypt wallet private key
    Method: decrypt_wif(encwif)
    Function: Decrypt the encrypted private key
    Parameters: encwif: str type, encrypted private key
    Return value: private key, str type
    
#### Get owner/active/memo private key
    Method:
        > getOwnerKeyForAccount(name)
        > getActiveKeyForAccount(name)
        > getMemoKeyForAccount(name)
    Function: Get the owner/active/memo private key by account name
    Parameters: name: str type, account name
    Return value: private key, str type
    
#### Get account ID through private key
    Method: getAccountFromPrivateKey(wif)
    Function: Get the account ID by private key
    Parameters: wif: str type, private key
    Return value: private key, str type
    
#### Get account ID through public key
    Method: getAccountFromPublicKey(pub)
    Function: Get the account ID by public key
    Parameters: pub: str type, public key
    Return value: public key, str type

#### Get account info
    Method: getAccount(pub)
    Function: Get the account info by public key
    Parameters: pub: str type, public key
#### Get public key type
    Method: getKeyType(account, pub)
    Function: Get the public key type
    Parameters:
        > account: Account type, account
        > pub: str type, public key
    Return value: str type
#### Get all the accounts in the wallet
    Method: getAccounts()
    Function: Get all the accounts info in the wallet
    Parameters: None
    Return value: Account array
#### Get all the public keys in the wallet
    Method: getPublicKeys()
    Function: Get all the public keys in the wallet
    Parameters: None
    Return value: str array
#### Wipe the private key in the wallet
    Method: wipe()
    Function: Wipe all private keys imported into the wallet
    Parameters: None


Example:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config
from pprint import pprint
from PythonMiddleware.account import Account

nodeAddress = "ws://127.0.0.1:8020" 
gph = Graphene(node=nodeAddress, blocking=True) 
set_shared_graphene_instance(gph) 

#Create wallet 1
# You can use the wallet instance directly through gph.wallet to operate the interface of the wallet.
if gph.wallet.created() is False: 
    gph.newWallet("123456")

#Create wallet 2
if gph.wallet.created() is False: 
    gph.wallet.create("123456")

#Unlock the wallet
gph.wallet.unlock("123456")

#Lock the wallet
gph.wallet.lock()

#Check the status of the wallet
#Return: False or True
pprint(gph.wallet.locked())

#Modify wallet unlock password
#The wallet should be unlocked
gph.wallet.changePassphrase("654321")

#Get the info of accounts imported into the wallet
pprint(gph.wallet.getAccounts())

#Import private key into the wallet
privateKey="5JWKbGLfkZNtnSAb7fuk1pD4jsdPyMpJz4jyhwgu8RBk9RNzDYA"
pub="COCOS78WwFk5YJVoCVa97NAKVALVZdhnYUdD2oHe2LCiX2KZaYNf4G8"
gph.wallet.addPrivateKey(privateKey) 

#Get the private key improted to the walelt
pprint(gph.wallet.getPrivateKeyForPublicKey(pub))

#Encrypt the private key
encWif = gph.wallet.encrypt_wif(privateKey)
pprint(encWif)

#Decrypt the private key
pprint(gph.wallet.decrypt_wif(encWif) == privateKey)

#Remove imported private key from the wallet
gph.wallet.removePrivateKeyFromPublicKey(pub)

#Remove imported account
gph.wallet.removeAccount(None)
gph.wallet.removeAccount('test1')

#Get owner private key of the account
pprint(gph.wallet.getOwnerKeyForAccount('test1'))
pprint(gph.wallet.getMemoKeyForAccount('test1'))
pprint(gph.wallet.getActiveKeyForAccount('test1'))

#Get the account ID
pprint(gph.wallet.getAccountFromPrivateKey(privateKey))
pprint(gph.wallet.getAccountFromPublicKey(pub))

#Get the account info
pprint(gph.wallet.getAccount(pub))

#Get all the accounts in the wallet
pprint(gph.wallet.getAccounts())

#Get all the public keys in the wallet
pprint(gph.wallet.getPublicKeys())

#Get public key type
pprint(gph.wallet.getKeyType(Account('test1'), pub))

#Wipe all the private keys imported into the wallet
#Use with caution!!
#gph.wallet.wipe()
```

### Account
----------

    Method: create_account
    Function: Create an account and import the private key into the wallet
    Parameters:
        account_name: Account name registration rules, /^[a-z][a-z0-9.-]{4,63}$/, begin with lowercase letters + digits or lowercase letters or dots or dashes -, with a length of 4 to 63 characters
        password: account password
	Note: Only a lifetime account can create an account

Example:  
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config
from pprint import pprint

nodeAddress = "ws://127.0.0.1:8020" #Modify to the blockchain node you are using
gph = Graphene(node=nodeAddress, blocking=True) 
set_shared_graphene_instance(gph) 

if gph.wallet.created() is False: 
    gph.newWallet("123456")
gph.wallet.unlock("123456") 

pprint(gph.create_account(account_name="test14", password="123456", proxy_account="init0"))
```
Sample output:
```text
chain_params {'prefix': 'COCOS', 'chain_id': '725fdc4a727a6aa84aea37376bb51e419febbf0f59830c05f3e82f607631e5fc', 'core_symbol': 'COCOS'}
tx.buffer>>>: {'expiration': '2019-08-16T07:16:38', 'signatures': ['1f5823d16f972a4407544a2388a014a3070caa0b073dc8a7310a26f09534db300d7892b0df9720fe478808b5f5ac317921ad1bc87f1f29317f4767e5b6336f2726'], 'operations': [[5, {'options': {'votes': [], 'num_witness': 0, 'voting_account': '1.2.4', 'extensions': [], 'memo_key': 'COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', 'num_committee': 0}, 'fee': {'amount': 514160, 'asset_id': '1.3.0'}, 'referrer_percent': 5000, 'referrer': '1.2.4', 'extensions': [], 'registrar': '1.2.4', 'owner': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS6gpgm7FqpeZUC8KuG5JuwN5Fe6iV7Cr3U3SJEYcsXQZ8S7ygUJ', '1']]}, 'active': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', '1']]}, 'name': 'test14'}]], 'extensions': [], 'ref_block_num': 34508, 'ref_block_prefix': 1299955552}
tx======>>: {'expiration': '2019-08-16T07:16:38', 'signatures': ['1f5823d16f972a4407544a2388a014a3070caa0b073dc8a7310a26f09534db300d7892b0df9720fe478808b5f5ac317921ad1bc87f1f29317f4767e5b6336f2726'], 'operations': [[5, {'options': {'votes': [], 'num_witness': 0, 'voting_account': '1.2.4', 'extensions': [], 'memo_key': 'COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', 'num_committee': 0}, 'fee': {'amount': 514160, 'asset_id': '1.3.0'}, 'referrer_percent': 5000, 'referrer': '1.2.4', 'extensions': [], 'registrar': '1.2.4', 'owner': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS6gpgm7FqpeZUC8KuG5JuwN5Fe6iV7Cr3U3SJEYcsXQZ8S7ygUJ', '1']]}, 'active': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', '1']]}, 'name': 'test14'}]], 'extensions': [], 'ref_block_num': 34508, 'ref_block_prefix': 1299955552}
transaction>>>: {'expiration': '2019-08-16T07:16:38', 'signatures': ['1f5823d16f972a4407544a2388a014a3070caa0b073dc8a7310a26f09534db300d7892b0df9720fe478808b5f5ac317921ad1bc87f1f29317f4767e5b6336f2726'], 'operations': [[5, {'options': {'votes': [], 'num_witness': 0, 'voting_account': '1.2.4', 'extensions': [], 'memo_key': 'COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', 'num_committee': 0}, 'fee': {'amount': 514160, 'asset_id': '1.3.0'}, 'referrer_percent': 5000, 'referrer': '1.2.4', 'extensions': [], 'registrar': '1.2.4', 'owner': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS6gpgm7FqpeZUC8KuG5JuwN5Fe6iV7Cr3U3SJEYcsXQZ8S7ygUJ', '1']]}, 'active': {'extensions': [], 'account_auths': [], 'weight_threshold': 1, 'key_auths': [['COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h', '1']]}, 'name': 'test14'}]], 'extensions': [], 'ref_block_num': 34508, 'ref_block_prefix': 1299955552}

['c4d9e437f4a9f7f717ba4b5b61f0646b49a6bae98f83d614db5b7e33abefb14f',
 {'block': 34509,
  'expiration': '2019-08-16T07:16:38',
  'extensions': [],
  'operation_results': [[2, {'real_running_time': 182, 'result': '1.2.17'}]],
  'operations': [[5,
                  {'active': {'account_auths': [],
                              'address_auths': [],
                              'key_auths': [['COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h',
                                             1]],
                              'weight_threshold': 1},
                   'extensions': {},
                   'fee': {'amount': 514160, 'asset_id': '1.3.0'},
                   'name': 'test14',
                   'options': {'extensions': [],
                               'memo_key': 'COCOS8GY2vkoK8gpLTuDxNfzD6JjwqYDmCRnpoUfZ78J4z8ChdcZi6h',
                               'num_committee': 0,
                               'num_witness': 0,
                               'votes': [],
                               'voting_account': '1.2.4'},
                   'owner': {'account_auths': [],
                             'address_auths': [],
                             'key_auths': [['COCOS6gpgm7FqpeZUC8KuG5JuwN5Fe6iV7Cr3U3SJEYcsXQZ8S7ygUJ',
                                            1]],
                             'weight_threshold': 1},
                   'referrer': '1.2.4',
                   'referrer_percent': 5000,
                   'registrar': '1.2.4'}]],
  'ref_block_num': 34508,
  'ref_block_prefix': 1299955552,
  'signatures': ['1f5823d16f972a4407544a2388a014a3070caa0b073dc8a7310a26f09534db300d7892b0df9720fe478808b5f5ac317921ad1bc87f1f29317f4767e5b6336f2726']}]
```

### Method：upgrade_account

----------

    Function: You can create a sub-account by upgrading your account to a lifetime account, which requires a certain fee.
    Parameters：  
        account：account to be upgraded
    Example:
    ```python
    pprint(gph.upgrade_account("test1"))
    ```


### Asset

----------

Method: transfer
Prototype：
```python
    def transfer(self, to, amount, asset, memo=["", 0], account=None):
```
    Function: Send tokens to the recipient
    Parameters：
        to：Recipient account name or id
        amount(int)：Amount of tokens sent
        asset：Asset ID or token symbol
        memo：Transfer memo, [transfer_memo_message, is_encrypt], is_encrypt: 0 -- don't encrypt, 1 -- encrypt
        account：Sender account name or id
Example:
```python
from_account = "nicotest"
to_account1 = "init7"
to_account2 = "init8"
pprint(gph.transfer("test1", 100, "COCOS", defaultAccount))
pprint(gph.transfer(to=to_account1, amount=11, asset="COCOS", memo=["test memo 0", 0], account=from_account))
pprint(gph.transfer(to=to_account2, amount=12, asset="1.3.0", memo=["test memo 1", 1], account=from_account))
```
Result:
```text
{'expiration': '2019-11-29T09:15:39',
 'extensions': [],
 'operations': [[0,
                 {'amount': {'amount': 1100000, 'asset_id': '1.3.0'},
                  'extensions': [],
                  'from': '1.2.16',
                  'memo': [0, 'test memo 0'],
                  'to': '1.2.12'}]],
 'ref_block_num': 10048,
 'ref_block_prefix': 307051849,
 'signatures': ['206433a625fdcbe46c2dbc96e73759039dc11dc4b5cca25bbd7c57df2481c31bc94fdcf4cc311eefa695b3dde56a2a9de0454bc3b4fbd08d7daee46b807f4dca6b']}
{'block_num': 10049,
 'transaction': {'expiration': '2019-11-29T09:15:39',
                 'extensions': [],
                 'operation_results': [[1,
                                        {'fees': [{'amount': 2013671,
                                                   'asset_id': '1.3.0'}],
                                         'real_running_time': 77}]],
                 'operations': [[0,
                                 {'amount': {'amount': 1100000,
                                             'asset_id': '1.3.0'},
                                  'extensions': [],
                                  'from': '1.2.16',
                                  'memo': [0, 'test memo 0'],
                                  'to': '1.2.12'}]],
                 'ref_block_num': 10048,
                 'ref_block_prefix': 307051849,
                 'signatures': ['206433a625fdcbe46c2dbc96e73759039dc11dc4b5cca25bbd7c57df2481c31bc94fdcf4cc311eefa695b3dde56a2a9de0454bc3b4fbd08d7daee46b807f4dca6b']},
 'trx_id': '0d8ca24ee057cc6df3fe9b1ab92211c3cd37b8081ca756237630cd22868ef0ea'}
{'expiration': '2019-11-29T09:15:43',
 'extensions': [],
 'operations': [[0,
                 {'amount': {'amount': 1200000, 'asset_id': '1.3.0'},
                  'extensions': [],
                  'from': '1.2.16',
                  'memo': [1,
                           {'from': 'COCOS56a5dTnfGpuPoWACnYj65dahcXMpTrNQkV3hHWCFkLxMF5mXpx',
                            'message': '8b39723f22fda4c1475fb0bc7ffc47fe',
                            'nonce': 2935580316419343781,
                            'to': 'COCOS5fW5NuvGjaVQTGwcJLwogxheq2KMjm3y5ccAShJqQnB3gNkGbL'}],
                  'to': '1.2.13'}]],
 'ref_block_num': 10049,
 'ref_block_prefix': 1721579182,
 'signatures': ['2066f971cccf92d6bfba4b06b802a65b6098d6d7262db103b41c256c15ce79c23003de26a17d514ed8e22a9099f3a5c9300e8fe1dfe5ee5419f66ceb4de5dd6f46']}
{'block_num': 10051,
 'transaction': {'expiration': '2019-11-29T09:15:43',
                 'extensions': [],
                 'operation_results': [[1,
                                        {'fees': [{'amount': 2090820,
                                                   'asset_id': '1.3.0'}],
                                         'real_running_time': 77}]],
                 'operations': [[0,
                                 {'amount': {'amount': 1200000,
                                             'asset_id': '1.3.0'},
                                  'extensions': [],
                                  'from': '1.2.16',
                                  'memo': [1,
                                           {'from': 'COCOS56a5dTnfGpuPoWACnYj65dahcXMpTrNQkV3hHWCFkLxMF5mXpx',
                                            'message': '8b39723f22fda4c1475fb0bc7ffc47fe',
                                            'nonce': '2935580316419343781',
                                            'to': 'COCOS5fW5NuvGjaVQTGwcJLwogxheq2KMjm3y5ccAShJqQnB3gNkGbL'}],
                                  'to': '1.2.13'}]],
                 'ref_block_num': 10049,
                 'ref_block_prefix': 1721579182,
                 'signatures': ['2066f971cccf92d6bfba4b06b802a65b6098d6d7262db103b41c256c15ce79c23003de26a17d514ed8e22a9099f3a5c9300e8fe1dfe5ee5419f66ceb4de5dd6f46']},
 'trx_id': '81e6aca64fbd3d9b288a15395a9789b2220f819e492ef314b689ed67f0d245a2'}
```

Method: asset_create
Prototype:
```python
    def asset_create(self, symbol, precision, amount, asset, _amount, _asset, common_options, bitasset_opts={}, account=None):
```
    Function: Create token
    Parameters:
    symbol: Asset symbol, regular ^[.A-Z]+$
    precision(int): precise to decimal digit
    amount(int): The amount of base assets (i.e. the created token, default 1)
    asset: Base asset ID
    _amount(int): quote asset (i.e. core asset, default 1)
    _asset: quote asset
    common_options(dict): Token option
    bitasset_opts(dict): Bit token option (not required), if the default parameters is used to create bit tokens, just pass {}
    account: Token creator
    commen_options parameters example:

```Python
common_options = {
    "max_supply": 10000000000000, # Maximum supply
    "market_fee_percent": 0, # Market transaction fee percent, default
    "max_market_fee": 0, # Maximum market transaction fee, default
    "flags": 0, # Current permissions
    "core_exchange_rate": {"base": {}, "quote": {}}, # Exchange rate with core assets, determined by the above base assets and quote assets
    "description": '{"main":"","short_name":"","market":""}', #Content description
"extension": {}
}
```
Example:
```python
defaultAccount="nicotest"
options = {
    "max_supply":"2100000000000000",
    "market_fee_percent":0,
    "max_market_fee":0,
    "issuer_permissions":79,
    "flags":0,
    "core_exchange_rate":{
        "base":{
            "amount":100000000,
            "asset_id":"1.3.1"
        },
        "quote":{
            "amount":100000,
            "asset_id":"1.3.0"
        }
    },
    "description":'{"main":"YUAN 2100","short_name":"","market":""}',
    "extensions":[]
}
#base: amount asset
#quote: _amount _asset
pprint(gph.asset_create(symbol="YUAN", precision=5, amount=1000, asset="1.3.1", _amount=1, _asset="1.3.0", common_options=options, bitasset_opts=None, account=defaultAccount))
```
Result:
``` text
tx.buffer>>>:  {'signatures': ['2015f7d1371d701d5ecbaef348ffed1120bc391cc0f8767492f1d4f271536dfdea0c62998134222d66b1402284f322eef4ae01087ee373ec4b3e5b68ca92266459'], 'ref_block_prefix': 1981534917, 'extensions': [], 'expiration': '2019-09-20T09:20:02', 'ref_block_num': 19227, 'operations': [[8, {'precision': 5, 'symbol': 'YUAN', 'fee': {'amount': 30000000001, 'asset_id': '1.3.0'}, 'extensions': [], 'common_options': {'market_fee_percent': 0, 'core_exchange_rate': {'quote': {'amount': 100000, 'asset_id': '1.3.0'}, 'base': {'amount': 100000000, 'asset_id': '1.3.1'}}, 'flags': 0, 'description': '{"main":"YUAN 2100","short_name":"","market":""}', 'issuer_permissions': 79, 'max_supply': 2100000000000000, 'max_market_fee': 0, 'extensions': []}, 'issuer': '1.2.15'}]]}
transaction>>>: {'signatures': ['2015f7d1371d701d5ecbaef348ffed1120bc391cc0f8767492f1d4f271536dfdea0c62998134222d66b1402284f322eef4ae01087ee373ec4b3e5b68ca92266459'], 'ref_block_prefix': 1981534917, 'extensions': [], 'expiration': '2019-09-20T09:20:02', 'ref_block_num': 19227, 'operations': [[8, {'precision': 5, 'symbol': 'YUAN', 'fee': {'amount': 30000000001, 'asset_id': '1.3.0'}, 'extensions': [], 'common_options': {'market_fee_percent': 0, 'core_exchange_rate': {'quote': {'amount': 100000, 'asset_id': '1.3.0'}, 'base': {'amount': 100000000, 'asset_id': '1.3.1'}}, 'flags': 0, 'description': '{"main":"YUAN 2100","short_name":"","market":""}', 'issuer_permissions': 79, 'max_supply': 2100000000000000, 'max_market_fee': 0, 'extensions': []}, 'issuer': '1.2.15'}]]}
['3db554f452a55f8ff62c1728bcb7c687fc1d691fa1835f25a6891ee4e5cecc39',
 {'block': 84764,
  'expiration': '2019-09-20T09:20:02',
  'extensions': [],
  'operation_results': [[2, {'real_running_time': 319, 'result': '1.3.5'}]],
  'operations': [[8,
                  {'common_options': {'core_exchange_rate': {'base': {'amount': 100000000,
                                                                      'asset_id': '1.3.1'},
                                                             'quote': {'amount': 100000,
                                                                       'asset_id': '1.3.0'}},
                                      'description': '{"main":"YUAN '
                                                     '2100","short_name":"","market":""}',
                                      'extensions': [],
                                      'flags': 0,
                                      'issuer_permissions': 79,
                                      'market_fee_percent': 0,
                                      'max_market_fee': 0,
                                      'max_supply': '2100000000000000'},
                   'extensions': [],
                   'fee': {'amount': '30000000001', 'asset_id': '1.3.0'},
                   'issuer': '1.2.15',
                   'precision': 5,
                   'symbol': 'YUAN'}]],
  'ref_block_num': 19227,
  'ref_block_prefix': 1981534917,
  'signatures': ['2015f7d1371d701d5ecbaef348ffed1120bc391cc0f8767492f1d4f271536dfdea0c62998134222d66b1402284f322eef4ae01087ee373ec4b3e5b68ca92266459']}]
```

    Method: asset_issue
    Function: Issue token
    Parameters:
        amount(int): Issuance amount
        asset: Token to be issued
        issue_to_account: target account
        memo: Additional message (not required)
        account: Token creator
    Example:

```python
pprint(gph.asset_issue(10000, "TESTS", "test1", account="test1"))

```

### NH Asset

----------
**Method: register_nh_asset_creator**  
    Function: Register current account as a developer
    Parameters:
	    account: Registrar account name
    Example:

```python
account="nicotest"
pprint(gph.register_nh_asset_creator(account))
```

**Method: create_world_view**  

```python
    def create_world_view(self, world_view, account=None):  
```
    Function: Create a supported NH asset worldview and register the NH asset worldview supported by current account (generally the game account) with the blockchain system
    Parameters:

> world_view：Worldview name
> account：Creator account name

Example：
```python
account="nicotest"
#2019-09-19T02:45:06 register_nh_asset_creator_operation nicotest fee: 1 COCOS   result: 4.0.1 
pprint(gph.create_world_view("snacktest", account))
```

**Method：create_nh_asset**  

```python
    def create_nh_asset(self, owner, assetID, world_view, describe, account=None):
```
    Function: Create a unique NH asset
    Parameters:
        > owner：Specify the NH asset owner (NH asset ownership account, which is defaulted as NH asset creator)
        > assetID：The native token used for the transaction of current NH asset
        > world_view：Worldview
        > describe：Description of the current content of the NH asset, as defined by the creator
        > account：creator

Example：
```python
account="nicotest"
#2019-09-19T02:45:26 create_world_view_operation nicotest fee: 1 COCOS   result: 4.1.1 
pprint(gph.create_nh_asset(account, "COCOS", "snacktest", '{"name":"test1"}', account))
```

**Method：create_nh_asset_order**  

```python
    def create_nh_asset_order(self, otcaccount, pending_order_fee_amount, pending_order_fee_asset, nh_asset, memo, price_amount, price, account=None):  
```
Function: Sell the NH asset
Parameters:
    > otcaccount：Account on OTC transaction platform for charging pending orders
    > pending_order_fee_amount：Amount of fees for pending orders. Pending order fees paid by users to OTC platform accounts
    > pending_order_fee_asset：The native token or ID of the asset used to pay for the pending order. The pending order fee paid by the user to the OTC platform account
    > nh_asset：NH Asset ID
    > memo：Pending order memo
    > price_amount：Price amount of pending order
    > price：The native token or ID used for the pending order price
    > account：Seller

Example：
```python
account="nicotest"
#2019-09-19T05:27:40 create_nh_asset_operation nicotest fee: 1 COCOS   result: 4.2.4 
pprint(gph.create_nh_asset_order("test1", 1, "1.3.0", "4.2.4", " sell nh asset order test ", 100, "1.3.0", account))
```

### Contract


----------
**Method：create_contract**  

```python
    def create_contract(self, name, data, con_authority, account=None):
```  
    Method: create_contract
    Function: Create a smart contract
	Parameters：  
        > name： Contract name, regular /^[a-z][a-z0-9.-]{4,63}$/, begin with a letter + letters or numbers or dot or dash -, length 4 to 63
        > data：Contract lua code
        > con_authority：Contract authority (publicKey in a pair of public and private keys)
        > account：Contract creator

Example：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from pprint import pprint
from PythonMiddleware.account import Account
from PythonMiddleware.storage import configStorage as config

nodeAddress = "ws://127.0.0.1:8049" 
gph = Graphene(node=nodeAddress, blocking=True) 
set_shared_graphene_instance(gph) 

#account info for test
defaultAccount="nicotest"
privateKey="5KgiWEMJPYbLpMhX6jvS9yBehhr4mWZhxX7hfxZQEo3rs8iakUQ"
pub="COCOS5X4bfMnAmeWhLoiHKUNrRu7D3LTXKBZQkZvWGj9YCTDBAYaSXU"

#Create wallet
if gph.wallet.created() is False: 
    gph.newWallet("123456")

#Unlock wallet
if gph.wallet.locked() is True:
    gph.wallet.unlock("123456")

#add key
if gph.wallet.getAccountFromPublicKey(pub) is None:
    gph.wallet.addPrivateKey(privateKey) 
pprint(gph.wallet.getPrivateKeyForPublicKey(pub))

#config
config["default_prefix"] = gph.rpc.chain_params["prefix"] 
config["default_account"] = defaultAccount 

#create contract
contract_name = "contract.debug.hello"
data = "function hello() \
    chainhelper:log('Hello World!') \
    chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) \
end "
pprint(gph.create_contract(contract_name, data=data, con_authority=pub, account=defaultAccount))
```

result：
``` text
tx.buffer>>>: {'ref_block_num': 2565, 'ref_block_prefix': 3142243287, 'extensions': [], 'signatures': ['2075b4799df8add77b27383290af79cf4107c681ee50bfdeb58aee14cd87cc5b431603813a402e326b9c432cc2c5f1cbdad3f32ea29cb63010e8f90615082337ed'], 'operations': [[43, {'owner': '1.2.15', 'extensions': [], 'contract_authority': 'COCOS5X4bfMnAmeWhLoiHKUNrRu7D3LTXKBZQkZvWGj9YCTDBAYaSXU', 'name': 'contract.debug.hello', 'data': "function hello()     chainhelper:log('Hello World!')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'fee': {'amount': 2122070, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:15:08'}
tx======>>: {'ref_block_num': 2565, 'ref_block_prefix': 3142243287, 'extensions': [], 'signatures': ['2075b4799df8add77b27383290af79cf4107c681ee50bfdeb58aee14cd87cc5b431603813a402e326b9c432cc2c5f1cbdad3f32ea29cb63010e8f90615082337ed'], 'operations': [[43, {'owner': '1.2.15', 'extensions': [], 'contract_authority': 'COCOS5X4bfMnAmeWhLoiHKUNrRu7D3LTXKBZQkZvWGj9YCTDBAYaSXU', 'name': 'contract.debug.hello', 'data': "function hello()     chainhelper:log('Hello World!')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'fee': {'amount': 2122070, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:15:08'}
transaction>>>: {'ref_block_num': 2565, 'ref_block_prefix': 3142243287, 'extensions': [], 'signatures': ['2075b4799df8add77b27383290af79cf4107c681ee50bfdeb58aee14cd87cc5b431603813a402e326b9c432cc2c5f1cbdad3f32ea29cb63010e8f90615082337ed'], 'operations': [[43, {'owner': '1.2.15', 'extensions': [], 'contract_authority': 'COCOS5X4bfMnAmeWhLoiHKUNrRu7D3LTXKBZQkZvWGj9YCTDBAYaSXU', 'name': 'contract.debug.hello', 'data': "function hello()     chainhelper:log('Hello World!')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'fee': {'amount': 2122070, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:15:08'}
['21379327f71198e16d87e98ec143340f616abfb6d0d499598b236b8940df07e7',
 {'block': 2566,
  'expiration': '2019-08-23T10:15:08',
  'extensions': [],
  'operation_results': [[2, {'real_running_time': 870, 'result': '1.16.1'}]],
  'operations': [[43,
                  {'contract_authority': 'COCOS5X4bfMnAmeWhLoiHKUNrRu7D3LTXKBZQkZvWGj9YCTDBAYaSXU',
                   'data': "function hello()     chainhelper:log('Hello "
                           "World!')     "
                           "chainhelper:log(date('%Y-%m-%dT%H:%M:%S', "
                           'chainhelper:time())) end ',
                   'extensions': [],
                   'fee': {'amount': 2122070, 'asset_id': '1.3.0'},
                   'name': 'contract.debug.hello',
                   'owner': '1.2.15'}]],
  'ref_block_num': 2565,
  'ref_block_prefix': 3142243287,
  'signatures': ['2075b4799df8add77b27383290af79cf4107c681ee50bfdeb58aee14cd87cc5b431603813a402e326b9c432cc2c5f1cbdad3f32ea29cb63010e8f90615082337ed']}]
```

**方法：call_contract_function**  

```python
    def call_contract_function(self, contract, function, value_list, account=None):
```
    Method: call_contract_function
    Function: Call contract function interface
    Parameters:
        > contract：Contract name or contract ID
        > function：Function name in the contract
        > value_list(list)： Call the parameter list of the contract function
        > account：Caller account name

value_list parameters 
```Python
value_list = [
        [2, {"baseValue": "test1"}], 
        [2, {"baseValue": "100")}]
    ]
```
Example：
```python
pprint(gph.call_contract_function("1.16.1", "draw", value_list=value_list, account="test1"))
```

result：
``` text
value_list:>>> []
value_list:>>> []
tx.buffer>>>: {'signatures': ['1f1dd6e131e3078857fed44fb6ae55e4d309fb5f9ef775a7c323d7ead60b58ca06218ae0b9d7feacb704a864c824c1997cdf8e42bf20a12776701402f53cf08884'], 'operations': [[44, {'function_name': 'hello', 'extensions': [], 'caller': '1.2.15', 'value_list': [], 'contract_id': '1.16.1', 'fee': {'amount': 2007812, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:16:50', 'extensions': [], 'ref_block_prefix': 2891025332, 'ref_block_num': 2612}
tx======>>: {'signatures': ['1f1dd6e131e3078857fed44fb6ae55e4d309fb5f9ef775a7c323d7ead60b58ca06218ae0b9d7feacb704a864c824c1997cdf8e42bf20a12776701402f53cf08884'], 'operations': [[44, {'function_name': 'hello', 'extensions': [], 'caller': '1.2.15', 'value_list': [], 'contract_id': '1.16.1', 'fee': {'amount': 2007812, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:16:50', 'extensions': [], 'ref_block_prefix': 2891025332, 'ref_block_num': 2612}
transaction>>>: {'signatures': ['1f1dd6e131e3078857fed44fb6ae55e4d309fb5f9ef775a7c323d7ead60b58ca06218ae0b9d7feacb704a864c824c1997cdf8e42bf20a12776701402f53cf08884'], 'operations': [[44, {'function_name': 'hello', 'extensions': [], 'caller': '1.2.15', 'value_list': [], 'contract_id': '1.16.1', 'fee': {'amount': 2007812, 'asset_id': '1.3.0'}}]], 'expiration': '2019-08-23T10:16:50', 'extensions': [], 'ref_block_prefix': 2891025332, 'ref_block_num': 2612}
['96207b09abdd65aef8355a4b2efde03268cdc3e841ccba48ee4263756a0b8603',
 {'block': 2613,
  'expiration': '2019-08-23T10:16:50',
  'extensions': [],
  'operation_results': [[4,
                         {'additional_cost': {'amount': 644109,
                                              'asset_id': '1.3.0'},
                          'contract_affecteds': [[3,
                                                  {'affected_account': '1.2.15',
                                                   'message': 'Hello World!'}],
                                                 [3,
                                                  {'affected_account': '1.2.15',
                                                   'message': '2019-08-23T09:16:50'}]],
                          'contract_id': '1.16.1',
                          'existed_pv': False,
                          'process_value': '',
                          'real_running_time': 607}]],
  'operations': [[44,
                  {'caller': '1.2.15',
                   'contract_id': '1.16.1',
                   'extensions': [],
                   'fee': {'amount': 2007812, 'asset_id': '1.3.0'},
                   'function_name': 'hello',
                   'value_list': []}]],
  'ref_block_num': 2612,
  'ref_block_prefix': 2891025332,
  'signatures': ['1f1dd6e131e3078857fed44fb6ae55e4d309fb5f9ef775a7c323d7ead60b58ca06218ae0b9d7feacb704a864c824c1997cdf8e42bf20a12776701402f53cf08884']}]
```

### Market


----------
Method: limit_order_create
Function: Create orders in a given market
Parameters:
    > amount(int)：Amount of tokens sold
    > asset： Asset ID or native token sold
    > min_amount(int)： The minimum amount of tokens required to be obtained
    > min_amount_asset： Asset ID or native token required to be obtained
    > fill(bool)： It is defaulted as False. If this flag is set to True, then this order must be completely purchased or rejected.
    > account：Seller account name

Example：
```python
pprint(gph.limit_order_create(1, "1.3.0", 1, "1.3.1", account="test1"))
```
Method: limit_order_cancel
Function: Cancel the order in a given market
Parameters:
    > order_number(list)：ID of the limit order to be canceled
    > account：Operator account name

Example：
```python
pprint(gph.limit_order_cancel(["1.7.1"], account="test1"))
```

### Witness

----------
    Method: create_witness
    Function: Create a witness candidate
    Parameters:
        > account_name：Witness candidate account
        > url：Witness weblink
        > key：Witness block signature public key
Example:

```python
pprint(gph.create_witness("test2", "", "COCOS5YnQru8mtYo9HkckwnuPe8fUcE4LSxdCfVheqBj9fMMK5zwiHb"))
```
    Method: approve_witness
    Function: Vote for witness candidates
    Parameters:
        > witnesses(list)：Witness account name or witness ID
        > account：Voting account name

Example：
```python
pprint(gph.disapprove_worker(["1.14.1"], "test1"))
```
### Committee

----------
    Method: committee_member_create
    Function: Create a committee member candidate
    Parameters:
        > url：weblink
        > account：Committee member candidate's account

Example
```python
pprint(gph.committee_member_create(" ", "test2"))
```

    Method: committee_member_update
    Function: Update committee member candidate
    Parameters: 
        > new_url：New weblink
        > account：Updated committee member candidate’s account

Example：
```python
pprint(gph.committee_member_update(" ", "test2"))
```

### Proposal

----------

	Method: relate_world_view
    Function: To link with the worldview, the developer can create the NH asset of the worldview only after linking to a certain worldview. The operation needs to be completed through a proposal to be approved by the creator of the worldview
    Parameters:
        > world_view：Worldview name
        > account：Linked account name 
Example：
```python
pprint(gph.relate_world_view("DRBALL", "test2"))
```

    Method: approveproposal
    Function: Approve proposals of other users to be linked with your worldview
    Parameters:
        > proposal_ids(list)：Proposal ID
        > account：Update proposed account
Example：

```python
pprint(gph.approveproposal(["1.10.1"], "test1"))
```

--------

**Example of Wallet API Call: **  

Method: unlock
Function: Unlock the wallet for related wallet operations
Parameters:
	pwd：wallet password
Example  
```python
print(gph.wallet.unlock(pwd))
```
Method: getAccounts
Function: Get account information in the wallet database

```python
print(gph.wallet.getAccounts())
```
Function: Get the corresponding private key in the wallet according to the public key given
Parameters:
	pub：Public key string
```python
print(gph.wallet.getPrivateKeyForPublicKey(pub))
```
**Example of RPC Interface Call: **  
Method: get_object
Function: Get this object information
Parameters:
	object_id：Object id
Example：
```python
print(gph.rpc.get_object("1.2.18")) 
```
Function: Get contract details
Parameters:
	contract_id：Contract id or contract name
Example：  
```python
print(gph.rpc.get_contract("1.16.0"))
```

Main-Packages
-------------
**PythonMiddleware**
	Description: The sub-modules correspond to all the classes involved in the blockchain system, such as accounts, assets, blocks, proposals, contracts, etc. Each class has a corresponding method to call. The graphene module has APIs related to the operation that can be called, such as transferring funds, creating accounts, creating assets, creating contracts, and so on.

 - PythonMiddleware.account module 
 - PythonMiddleware.aes module
 - PythonMiddleware.amount module
 - PythonMiddleware.asset module
 - PythonMiddleware.block module
 - PythonMiddleware.blockchain module
 - PythonMiddleware.committee module
 - PythonMiddleware.contract module
 - PythonMiddleware.dex module
 - PythonMiddleware.exceptions module
 - PythonMiddleware.extensions module
 - PythonMiddleware.graphene module
 - PythonMiddleware.instance module
 - PythonMiddleware.market module
 - PythonMiddleware.memo module
 - PythonMiddleware.notify module
 - PythonMiddleware.price module
 - PythonMiddleware.proposal module
 - PythonMiddleware.storage module
 - PythonMiddleware.transactionbuilder module
 - PythonMiddleware.utils module
 - PythonMiddleware.vesting module
 - PythonMiddleware.wallet module
 - PythonMiddleware.witness module
 - PythonMiddleware.worker module
 
 **PythonMiddlewarebase**
	Description: The sub-modules involve contents related to the underlying design, such as blockchain information, object type, operation, data structure, etc., which do not need to be changed in general. The chains module needs to be modified according to the use of the blockchain when initializing.
 
 - PythonMiddlewarebase.account module
 - PythonMiddlewarebase.asset_permissions module
 - PythonMiddlewarebase.bip38 module
 - PythonMiddlewarebase.chains module
 - PythonMiddlewarebase.memo module
 - PythonMiddlewarebase.objects module
 - PythonMiddlewarebase.objecttypes module
 - PythonMiddlewarebase.operationids module
 - PythonMiddlewarebase.operations module
 - PythonMiddlewarebase.signedtransactions module
 - PythonMiddlewarebase.transactions module

 
