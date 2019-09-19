Python Middleware For Cocos—BCX
==============
* [入门](#入门)
* [使用API](#使用API)
* [Main-Packages](#Main-Packages)

入门
---------------

我们建议在Ubuntu 16.04 LTS（64位）上构建 ，默认python3.5

**手动安装：**

    cd python-PythonMiddleware
    python3 setup.py install --user
	
**修改链参数：**

    vi python-PythonMiddleware/PythonMiddlewarebase/chains.py # 编辑链相关参数
	
	```python
	known_chains = {
    "xxxxxx": {
        "chain_id": "xxxxxx",
        "core_symbol": "xxxxxx",
        "prefix": "xxxxxx"} # chains.py中所编辑的代码
	```
	python3 setup.py install --user # 重新加载python库

**构建pyhton脚本：**
```python
from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from PythonMiddleware.storage import configStorage as config
from pprint import pprint

nodeAddress = "ws://127.0.0.1:8000" # 所需要连接的RPC节点
gph = Graphene(node=nodeAddress, blocking=True) # 实例化对象
set_shared_graphene_instance(gph) # 将gph设置为共享的全局实例

if gph.wallet.created() is False: # 创建本地钱包数据库，如果没有，则创建一个新的钱包数据库
    gph.newWallet("xxxxxx")
gph.wallet.unlock("xxxxxx") # 解锁钱包，若后续操作需要与钱包交互，则需要解锁钱包

config["default_prefix"] = gph.rpc.chain_params["prefix"] # 向钱包数据库中添加默认信息
gph.wallet.addPrivateKey(privateKey) # 向钱包中添加私钥
config["default_account"] = yourname # 向钱包数据库中添加默认信息
```

API接口
-------------
* [钱包相关](#钱包相关)
* [账户相关](#账户相关)  
* [资产相关](#资产相关)  
* [NH资产相关](#NH资产相关)  
* [合约相关](#合约相关)  
* [市场相关](#市场相关)  
* [见证人相关](#见证人相关)  
* [理事会相关](#理事会相关)  
* [提议相关](#提议相关)  

----------

### 钱包相关
* [Graphene创建钱包](#Graphene创建钱包)
* [wallet创建钱包1](#wallet创建钱包1)
* [wallet创建钱包2](#wallet创建钱包2)
* [钱包解锁](#钱包解锁)
* [钱包锁定](#钱包锁定)
* [钱包解锁密码修改](#钱包解锁密码修改)
* [钱包添加私钥](#钱包添加私钥)
* [钱包获取私钥](#钱包获取私钥)
* [钱包获取私钥](#钱包获取私钥)
* [钱包加密私钥](#钱包加密私钥)
* [钱包解密私钥](#钱包解密私钥)
* [钱包获取owner、active、memo私钥](#钱包获取owner、active、memo私钥)
* [私钥获取账户ID](#私钥获取账户ID)
* [公钥获取账户ID](#公钥获取账户ID)
* [钱包获取账户信息](#钱包获取账户信息)
* [获取公钥类型](#获取公钥类型)
* [获取钱包所有账户](#获取钱包所有账户)
* [获取钱包所有公钥](#获取钱包所有公钥)
* [清空钱包私钥](#清空钱包私钥)


#### Graphene创建钱包
    方法：newWallet(pwd)
    功能：创建钱包
    参数：pwd：str类型，钱包lock和unlock密码
    返回值：
        > 成功：None
        > 失败：对应错误信息
    说明：
        > 此接口是对wallet.newWallet接口的封装，并不是wallet api
        > 本质还是调用wallet创建钱包
        > 钱包创建完后，可以通过Graphene::instance.wallet直接使用钱包instance，操作钱包的接口。

#### wallet创建钱包1
    方法：newWallet(pwd)
    功能：创建钱包
    参数：pwd：str类型，钱包lock和unlock密码
    返回值：
        > 成功：None
        > 失败：对应错误信息

#### wallet创建钱包2
    方法：create(pwd)
    功能：创建钱包，Alias for newWallet()
    参数：
        > pwd：str类型，钱包lock和unlock密码
    返回值：
        > 成功：None
        > 失败：对应错误信息

#### 钱包解锁
    方法：unlock(pwd=None)
    功能：解锁钱包
    参数：pwd -- str类型，钱包密码
    返回值：
        > 成功：None
        > 失败：对应错误信息

#### 钱包锁定
    方法：lock()
    功能：解锁钱包
    参数：无
    返回值：
        > 成功：None
        > 失败：对应错误信息

#### 钱包解锁密码修改
    方法：changePassphrase(new_pwd)
    功能：修改钱包解锁密码
    参数：pwd：str类型，要修改的钱包新密码
    返回值：
        > 成功：None
        > 失败：对应错误信息

#### 钱包添加私钥
    方法：addPrivateKey(wif)
    功能：修改钱包解锁密码
    参数：wif：str类型，私钥

####  钱包获取私钥
    方法：getPrivateKeyForPublicKey(pub)
    功能：从钱包获取公钥对应的私钥
    参数：pub：str类型，公钥

#### 钱包获取私钥
    方法：removePrivateKeyFromPublicKey(pub)
    功能：从钱包移除公钥对应的私钥
    参数：pub：str类型，公钥

#### 钱包加密私钥
    方法：encrypt_wif(wif)
    功能：对私钥进行加密，
    参数：wif：str类型，私钥
    返回值：加密过的私钥，str类型

#### 钱包解密私钥
    方法：decrypt_wif(encwif)
    功能：对加密过的私钥进行解密
    参数：encwif：str类型，加密过的私钥
    返回值：私钥，str类型

#### 钱包获取owner、active、memo私钥
    方法：
        > getOwnerKeyForAccount(name)
        > getActiveKeyForAccount(name)
        > getMemoKeyForAccount(name)
    功能：通过账户名，获取owner、active、memo私钥
    参数：name：str类型，账户名
    返回值：私钥，str类型

#### 私钥获取账户ID
    方法：getAccountFromPrivateKey(wif)
    功能：通过私钥，获取账户ID
    参数：wif：str类型，私钥
    返回值：私钥，str类型

#### 公钥获取账户ID
    方法：getAccountFromPublicKey(pub)
    功能：通过公钥，获取账户ID
    参数：pub：str类型，公钥
    返回值：公钥，str类型

#### 钱包获取账户信息
    方法：getAccount(pub)
    功能：通过公钥，获取账户信息
    参数：pub：str类型，公钥


#### 获取公钥类型
    方法：getKeyType(account, pub)
    功能：获取公钥类型
    参数：
        > account：Account类型，账户
        > pub：str类型，公钥
    返回值：str类型
  
#### 获取钱包所有账户
    方法：getAccounts()
    功能：通过钱包里的所有账户信息
    参数：无
    返回值：Account 数组

#### 获取钱包所有公钥
    方法：getPublicKeys()
    功能：获取钱包里所有公钥
    参数：无
    返回值：str数组

#### 清空钱包私钥
    方法：wipe()
    功能：清空导入钱包的所有私钥
    参数：无

示例：
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

#创建钱包1
#可以通过gph.wallet 直接使用钱包instance，操作钱包的接口。
if gph.wallet.created() is False: 
    gph.newWallet("123456")

#创建钱包2
if gph.wallet.created() is False: 
    gph.wallet.create("123456")

#钱包解锁
gph.wallet.unlock("123456")

#钱包锁住
gph.wallet.lock()

#查看钱包锁定状态
#返回: False 或 True
pprint(gph.wallet.locked())

#更改钱包解锁密码
#钱包需要unlock状态
gph.wallet.changePassphrase("654321")

#查看钱包导入账户信息
pprint(gph.wallet.getAccounts())

#钱包导入私钥
privateKey="5JWKbGLfkZNtnSAb7fuk1pD4jsdPyMpJz4jyhwgu8RBk9RNzDYA"
pub="COCOS78WwFk5YJVoCVa97NAKVALVZdhnYUdD2oHe2LCiX2KZaYNf4G8"
gph.wallet.addPrivateKey(privateKey) 

#钱包获取导入的私钥
pprint(gph.wallet.getPrivateKeyForPublicKey(pub))

#加密私钥
encWif = gph.wallet.encrypt_wif(privateKey)
pprint(encWif)

#解密私钥
pprint(gph.wallet.decrypt_wif(encWif) == privateKey)

#钱包移除导入的私钥
gph.wallet.removePrivateKeyFromPublicKey(pub)

#移除导入的账户None
gph.wallet.removeAccount(None)
gph.wallet.removeAccount('test1')

#获取账号的owner private key
pprint(gph.wallet.getOwnerKeyForAccount('test1'))
pprint(gph.wallet.getMemoKeyForAccount('test1'))
pprint(gph.wallet.getActiveKeyForAccount('test1'))

#获取账户ID
pprint(gph.wallet.getAccountFromPrivateKey(privateKey))
pprint(gph.wallet.getAccountFromPublicKey(pub))

#获取账户信息
pprint(gph.wallet.getAccount(pub))

#获取钱包所有账户信息
pprint(gph.wallet.getAccounts())

#获取钱包所有公钥
pprint(gph.wallet.getPublicKeys())

#获取钱包公钥类型
pprint(gph.wallet.getKeyType(Account('test1'), pub))

#清除钱包所有私钥
#  慎用！！！
#gph.wallet.wipe()
```


### 账户相关


----------


方法：create_account  
功能：创建一个账户并将私钥导入到钱包  
参数：  
   account_name：账户名注册规则，/^[a-z][a-z0-9\.-]{4,63}$/，小写字母开头+数字或小写字母或点.或短横线-，长度4至63  
    password：账户密码  
注：只有终身账户才可以创建账户  
示例：  
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
示例输出：
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

方法：upgrade_account  
功能：将账户升级为终身账户，可以创建子账户，此操作需要消耗一定的手续费  
参数：  
    account：升级的账户  
示例：
```python
pprint(gph.upgrade_account("test1"))
```


### 资产相关


----------


方法：transfer  
功能：向目标对象发送代币  
参数：  
    to：接收方账户名  
    amount(int)：发送的代币数量  
    asset：资产ID或代币符号  
    memo：转账备注  
    account：发送方账户名  
示例：
```python
pprint(gph.transfer("test2",100, "1.3.0", " ", "test1"))
```
方法：asset_create  
功能：创建token  
参数：  
    symbol：资产符号，正则^\[\.A-Z\]+$  
    precision(int)：精度(小数位数)  
    amount(int)：基准资产数量(即创建的代币，默认1)  
    asset：基准资产ID  
    _amount(int)：标价资产(即核心资产，默认1)  
    _asset：标价资产  
    common_options(dict)：代币选项  
    bitasset_opts(dict)：比特代币选项(非必填)，若使用默认参数来创建比特代币，则只需传入{}即可  
    is_prediction_market(bool)：是否为预测市场(非比特代币无需关注此参数)  
    account：代币创建者  
commen_options参数示例：  
```Python
common_options = {
    "max_supply": 10000000000000, # 最大发行量
    "market_fee_percent": 0, # 市场交易手续费百分比，默认
    "max_market_fee": 0, # 市场交易手续费最大值，默认
    "issuer_permissions": 79, # 发行者可以更新的权限，默认
    "flags": 0, # 当前权限
    "core_exchange_rate": {"base": {}, "quote": {}}, # 与核心资产的转换率，由上述基准资产与标价资产决定
    "whitelist_authorities": [], # 白名单账户
    "blacklist_authorities": [], # 黑名单账户
    "whitelist_markets": [], # 白名单资产
    "blacklist_markets": [], # 黑名单资产
    "description": '{"main":"","short_name":"","market":""}', #内容描述
    "extension": {}
}
```
示例：
```python
pprint(gph.asset_create("TESTS", 5, 1, "1.3.0", 1, "1.3.1", common_options=common_options, bitasset_opts={}, account="test1"))

```
方法：asset_issue  
功能：代币资产token发行  
参数：  
    amount(int)：发行数量  
    asset：发行资产符号  
    issue_to_account：发行对象  
    memo：附加消息(非必填)  
    account：代币创建者  
示例：
```python
pprint(gph.asset_issue(10000, "TESTS", "test1", account="test1"))

```

### NH资产相关


----------
**方法：register_nh_asset_creator**  

原型：
```python
    def register_nh_asset_creator(self, account=None):  
```
功能：将当前账户注册成为开发者  
参数：  
> account：注册者账户名  

示例：
```python
account="nicotest"
pprint(gph.register_nh_asset_creator(account))
```

**方法：create_world_view**  

原型：
```python
    def create_world_view(self, world_view, account=None):  
```
功能：创建支持的NH资产世界观，向区块链系统注册当前账号（通常为游戏的账号）支持的NH资产世界观  
参数：  
> world_view：世界观名称  
> account：创建者账户名  

示例：
```python
account="nicotest"
#2019-09-19T02:45:06 register_nh_asset_creator_operation nicotest fee: 1 COCOS   result: 4.0.1 
pprint(gph.create_world_view("snacktest", account))
```

**方法：create_nh_asset**  

原型：
```python
    def create_nh_asset(self, owner, assetID, world_view, describe, account=None):
```
功能：创建一个唯一的NH资产，具有唯一性  

参数：  
> owner：指定NH资产拥有者(NH资产归属权账户，默认为NH资产创建者)  
> assetID：当前NH资产交易时，使用的资产符号  
> world_view：世界观  
> describe：当前NH资产的具体内容描述，由创建者定义  
> account：创建者  

示例：
```python
account="nicotest"
#2019-09-19T02:45:26 create_world_view_operation nicotest fee: 1 COCOS   result: 4.1.1 
pprint(gph.create_nh_asset(account, "COCOS", "snacktest", '{"name":"test1"}', account))
```

**方法：delete_nh_asset**  

原型：
```python
    def delete_nh_asset(self, asset_id, account=None):  
```
功能：删除非同质资产  
参数：
> asset_id: 非同质资产ID  
> account: 操作付费账户  

示例：
```python
account="nicotest"
pprint(gph.delete_nh_asset("4.2.4", account))
```

**方法：transfer_nh_asset**  

原型：
```python
    def transfer_nh_asset(self, to, nh_asset_id, account=None):  
```
功能：转移非同质资产 将自己拥有的非同质资产转移给另外一个账户  
参数：
> to：to account，非同质资产的接收账户  
> nh_asset_id: 非同质资产ID  
> account: from account，非同质资产转出账户  

示例：
```python
account="nicotest"
#2019-09-19T06:08:46 create_nh_asset_operation nicotest fee: 1 COCOS   result: 4.2.5
pprint(gph.transfer_nh_asset("test1", "4.2.5", account))
```

**方法：create_nh_asset_order**  

原型：
```python
    def create_nh_asset_order(self, otcaccount, pending_order_fee_amount, pending_order_fee_asset, nh_asset, memo, price_amount, price, account=None):  
```
功能：卖出NH资产  
参数：  
> otcaccount：OTC交易平台账户，用于收取挂单费用  
> pending_order_fee_amount：挂单费用数量，用户向OTC平台账户支付的挂单费用  
> pending_order_fee_asset：挂单费用所用资产符号或ID，用户向OTC平台账户支付的挂单费用  
> nh_asset：NH资产ID  
> memo：挂单备注信息  
> price_amount：商品挂单价格数量  
> price：商品挂单价格所用资产符号或ID  
> account：挂单人  

示例：
```python
account="nicotest"
#2019-09-19T05:27:40 create_nh_asset_operation nicotest fee: 1 COCOS   result: 4.2.4 
pprint(gph.create_nh_asset_order("test1", 1, "1.3.0", "4.2.4", " sell nh asset order test ", 100, "1.3.0", account))
```

**方法：cancel_nh_asset_order**  

原型：
```python
    def cancel_nh_asset_order(self, order, account=None):  
```
功能：取消NH资产订单  
参数：
> order: 非同质资产订单ID  
> account: 操作付费账户  

示例：
```python
account="nicotest"
#2019-09-19T05:29:16 create_nh_asset_order_operation nicotest fee: 1 COCOS   result: 4.3.1 
pprint(gph.cancel_nh_asset_order("4.3.1", account))
```

**方法：fill_nh_asset_order**  

原型：
```python
    def fill_nh_asset_order(self, order, account=None):
```
功能：购买非同质资产  
参数：
> order: 非同质资产出售单 ID  
> account: 购买者  

示例：
```python
account="nicotest"
#2019-09-19T06:20:38 create_nh_asset_order_operation nicotest fee: 1 COCOS   result: 4.3.2 
pprint(gph.fill_nh_asset_order("4.3.2", account))
```


### 合约相关


----------
方法：create_contract  
功能：创建智能合约  
参数：  
    name：合约名，正则/^[a-z][a-z0-9\.-]{4,63}$/，首字母开头+字母或数字或点.或短横线-，长度4至63  
    data：合约lua代码  
    con_authority：合约权限(一对公私钥中的公钥publicKey)  
    account：合约创建者  
示例：
```python
print(gph.create_contract("contract.test01", data=data, con_authority="COCOS6esv8d6u2eqzKyiQvCYJa6XK74c7BrmzUqL4Z7zfhtvB4dbLh4", account="developer"))
```
方法：call_contract_function  
功能：调用合约函数接口  
参数：  
    contract：合约名称或者合约ID  
    function：合约中函数名称  
    value_list(list)：调用合约函数的参数列表  
    account：调用者账户名  
value_list参数示例：  
```Python
value_list = [
        [2, {"baseValue": "test1"}], 
        [2, {"baseValue": "100")}]
    ]
```
示例：
```python
pprint(gph.call_contract_function("1.16.1", "draw", value_list=value_list, account="test1"))

```
### 市场相关


----------
方法：limit_order_create  
功能：创建在给定市场中的订单  
参数：
    amount(int)：出售的代币数量  
    asset：出售的资产ID或代币符号  
    min_amount(int)：所要求获取的代币的最低数量  
    min_amount_asset：所要求获取的资产ID或代币符号  
    fill(bool)：默认为False，如果这个标志被设置为True，那么这个订单必须被完整的购买或者被拒绝  
    account：出售者账户名  
示例：
```python
pprint(gph.limit_order_create(1, "1.3.0", 1, "1.3.1", account="test1"))
```
方法：limit_order_cancel  
功能：取消您在给定市场中的订单  
参数：  
    order_number(list)：要取消的限价单的ID  
    account：操作人账户名  
示例：
```python
pprint(gph.limit_order_cancel(["1.7.1"], account="test1"))
```

### 见证人相关


----------
方法：create_witness  
功能：创建见证人候选人  
参数：  
    account_name：见证人候选人账户  
    url：见证人网页链接  
    key：见证人块签名公钥  
示例：
```python
pprint(gph.create_witness("test2", "", "COCOS5YnQru8mtYo9HkckwnuPe8fUcE4LSxdCfVheqBj9fMMK5zwiHb"))
```
方法：approve_witness  
功能：为见证人候选人投票  
参数：  
    witnesses(list)：见证人账户名或见证人ID  
    account：投票账户名  
示例：
```python
pprint(gph.disapprove_worker(["1.14.1"], "test1"))
```
### 理事会相关


----------
方法：committee_member_create  
功能：创建理事会候选人  
参数：  
    url：网页链接  
    account：理事会候选人的账户  
示例：
```python
pprint(gph.committee_member_create(" ", "test2"))
```
方法：committee_member_update  
功能：跟新理事会候选人  
参数：  
    new_url：新的网页链接  
    account：更新的理事会候选人的账户  
示例：
```python
pprint(gph.committee_member_update(" ", "test2"))
```
### 提议相关


----------
方法：relate_world_view  
功能：关联世界观，开发者只有在关联了某一个世界观后，才可以创建这个世界观的NH资产，该操作需要通过提议来完成，需要此世界观的创建者审批  
参数：  
    world_view：世界观名称  
    account：关联人账户名  
示例：
```python
pprint(gph.relate_world_view("DRBALL", "test2"))
```
方法：approveproposal  
功能：批准其他用户关联自己的世界观的提议  
参数：  
    proposal_ids(list)：提议ID  
    account：更新提议的账户  
示例：
```python
pprint(gph.approveproposal(["1.10.1"], "test1"))
```

**钱包api调用示例：**  
方法：unlock  
功能：解锁钱包，进行相关钱包操作  
参数：  
	pwd：钱包密码  
示例：  
```python
print(gph.wallet.unlock(pwd))
```
方法：getAccounts  
功能：获取钱包数据库中的账户信息  
```python
print(gph.wallet.getAccounts())
```
方法：getPrivateKeyForPublicKey  
功能：根据所给出的公钥在钱包中获取对应的私钥  
参数：  
	pub：公钥字符串  
```python
print(gph.wallet.getPrivateKeyForPublicKey(pub))
```
**RPC接口调用示例：**  
方法：get_object   
功能：获取此object对象信息  
参数：  
	object_id：对象id  
示例：
```python
print(gph.rpc.get_object("1.2.18")) # 获取id为"1.2.17"的账户信息
```
方法：get_contract    
功能：获取合约的详细信息  
参数：  
	contract_id：合约id或合约名称
示例：  
```python
print(gph.rpc.get_contract("1.16.0")) # 获取id为"1.16.0"的合约信息
```

Main-Packages
-------------
**PythonMiddleware**
说明：其中的子模块一一对应了链系统中涉及到的所有类，比如账户、资产、区块、提议、合约等，每个类下有相应的方法可以调用。graphene模块中有与操作operation有关的api接口可供调用，比如转账、创建账户、创建资产、创建合约等。

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
 说明：其中的子模块涉及到一些与底层设计相关的内容，比如链信息、对象类型、操作、数据结构等，一般不需要改变，chains模块需要初始化时依据链使用情况进行修改操作。
 
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

 
