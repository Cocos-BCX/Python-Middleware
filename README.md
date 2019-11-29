Python Middleware For BCX
==============
* [安装和入门](#安装和入门)
* [使用API](#使用API)
* [Main-Packages](#Main-Packages)

安装和入门
---------------


下面的安装说明是在Ubuntu 16.04 LTS（64位）上构建，需要python3环境。  

## 1. 准备工作
### 1.1 python3 环境  
python版本：≥ python3.5  
ubuntu 16.04 python3.5 安装：  
``` shell  
sudo apt-get install python3.5 -y  
```  

### 1.2 Python-Middleware链参数配置  
主要是chain_id，修改文件： PythonMiddlewarebase/chains.py  
``` text
known_chains = {
"xxxxxx": {
    "chain_id": "xxxxxx", # 链ID
    "core_symbol": "xxxxxx", # 核心资产，默认COCOS
    "prefix": "xxxxxx"} # 前缀，默认COCOS
```  

示例：  
``` python 
default_prefix = "COCOS"

known_chains = { 
    "COCOS": {
        "chain_id": "c1ac4bb7bd7d94874a1cb98b39a8a582421d03d022dfa4be8c70567076e03ad0",
        "core_symbol": "COCOS",
        "prefix": "COCOS"
    }
} 
```

## 2. 安装命令：  
``` shell
python3 setup.py install --user
```

## 3. 可能遇到的问题：  
### 3.1 缺少 setuptools 依赖：  
``` text   
test@test01:/mnt/Python-Middleware# python3 setup.py install --user
Traceback (most recent call last):
  File "setup.py", line 3, in <module>
    from setuptools import setup
ImportError: No module named 'setuptools'
```  

**解决：**   
``` shell  
sudo apt-get install python3-setuptools  
```  

### 3.2 缺少gcc等相关依赖  
``` text   
test@test01:/mnt/Python-Middleware# python3 setup.py install --user
zip_safe flag not set; analyzing archive contents...

Installed /mnt/Python-Middleware/.eggs/pytest_runner-5.2-py3.5.egg

......

Processing pycrypto-2.6.1.tar.gz
Writing /tmp/easy_install-6s2q9_bu/pycrypto-2.6.1/setup.cfg
Running pycrypto-2.6.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-6s2q9_bu/pycrypto-2.6.1/egg-dist-tmp-dnhffkfr
src/_fastmath.c:31:20: fatal error: Python.h: No such file or directory
compilation terminated.
error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```  


**解决：**
``` shell  
sudo apt-get install build-essential python3-dev libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev -y  
```

## 4. 安装验证：   

### 4.1 pip list查看
pip list可以查看到PythonMiddleware。  

``` text  
test@test01:/mnt/Python-Middleware# pip3 list
appdirs (1.4.3)
certifi (2019.11.28)
chardet (3.0.4)
ecdsa (0.13.3)
Events (0.3)
idna (2.7)
pip (8.1.1)
pycrypto (2.6.1)
pycryptodome (3.6.6)
pylibscrypt (1.7.1)
PythonMiddleware (1.0.0)
requests (2.20.0)
scrypt (0.8.6)
setuptools (20.7.0)
six (1.13.0)
urllib3 (1.24.3)
websocket-client (0.48.0)
websockets (6.0)
wheel (0.29.0)
```  

**如果没有pip3需要先安装：**
``` shell  
sudo apt install python3-pip -y
```  

### 4.2 使用PythonMiddleware
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

使用API  
-------------  

**Graphene实例调用示例：**  
* [账户相关](#账户相关)  
* [资产相关](#资产相关)  
* [NH资产相关](#NH资产相关)  
* [合约相关](#合约相关)  
* [市场相关](#市场相关)  
* [见证人相关](#见证人相关)  
* [理事会相关](#理事会相关)  
* [提议相关](#提议相关)  

###### 账户相关


----------


方法：create_account  
功能：创建一个账户并将私钥导入到钱包  
参数：  
    account_name：账户名注册规则，/^[a-z][a-z0-9\.-]{4,63}$/，小写字母开头+数字或小写字母或点.或短横线-，长度4至63  
    password：账户密码  
注：只有终身账户才可以创建账户  
示例：  
```python
pprint(gph.create_account(account_name="test3", password="password"))
```
方法：upgrade_account  
功能：将账户升级为终身账户，可以创建子账户，此操作需要消耗一定的手续费  
参数：  
    account：升级的账户  
示例：
```python
pprint(gph.upgrade_account(account="test1"))
```

###### 资产相关


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
pprint(gph.transfer(to="test2",amount=100, asset="1.3.0", memo=" ", account="test1"))
```
方法：asset_create  
功能：创建token  
参数：  
    symbol：资产符号，正则^\[\.A-Z\]+$  
    precision(int)：精度(小数位数)    
    common_options(dict)：代币选项     
    account：代币创建者  
commen_options参数示例：  
```Python
common_options = {
    "max_supply": 10000000000000, # 最大发行量
    "market_fee_percent": 0, # 市场交易手续费百分比，默认
    "max_market_fee": 0, # 市场交易手续费最大值，默认
    "issuer_permissions": 0, # 发行者可以更新的权限，默认
    "flags": 0, # 当前权限
    "description": '', #内容描述
    "extension": {}
}
```
示例：
```python
pprint(gph.asset_create(symbol="TESTS", precision=5, common_options=common_options, account="test1"))

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
pprint(gph.asset_issue(amount=10000, asset="TESTS", issue_to_account="test1", memo=' ', account="test1"))

```

###### NH资产相关


----------
方法：register_nh_asset_creator  
功能：将当前账户注册成为开发者  
参数：  
    account：注册者账户名
示例：
```python
pprint(gph.register_nh_asset_creator(account="test2"))
```
方法：create_world_view  
功能：创建支持的NH资产世界观，向区块链系统注册当前账号（通常为游戏的账号）支持的NH资产世界观  
参数：  
    world_view：世界观名称  
    account：创建者账户名  
示例：
```python
pprint(gph.create_world_view(world_view="DRBALL", account="test1"))
```
方法：create_nh_asset  
功能：创建一个唯一的NH资产，具有唯一性  
参数：  
    owner：指定NH资产拥有者(NH资产归属权账户，默认为NH资产创建者)  
    assetID：当前NH资产交易时，使用的资产符号  
    world_view：世界观  
    describe：当前NH资产的具体内容描述，由制造者定义  
    account：创建者
示例：
```python
pprint(gph.create_nh_asset(owner="test2", assetID="XXX", world_view="FLY", describe='{"name":"tom"}', account="test1"))
```
方法：create_nh_asset_order  
功能：卖出NH资产  
参数：  
    otcaccount：OTC交易平台账户，用于收取挂单费用  
    pending_order_fee_amount：挂单费用数量，用户向OTC平台账户支付的挂单费用  
    pending_order_fee_asset：挂单费用所用资产符号或ID，用户向OTC平台账户支付的挂单费用  
    nh_asset：NH资产ID  
    memo：挂单备注信息  
    price_amount：商品挂单价格数量  
    price：商品挂单价格所用资产符号或ID  
    account：挂单人  
示例：
```python
pprint(gph.create_nh_asset_order(otcaccount="official-account", pending_order_fee_amount=1, pending_order_fee_asset="1.3.0", nh_asset="4.2.1", memo=" ", price_amount=100, price="1.3.0", account="test1"))
```

###### 合约相关


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
data = """
    function hello()
        chainhelper:log('Hello World! Hello Python')
    end"""
print(gph.create_contract(name="contract.test01", data=data, con_authority="xxxxxxxxxxxxxxxxxxxx", account="developer"))
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
pprint(gph.call_contract_function(contract="1.16.1", function="draw", value_list=value_list, account="test1"))

```
###### 市场相关


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
pprint(gph.limit_order_create(amount=1, asset="1.3.0", min_amount=1, min_amount_asset="1.3.1", account="test1"))
```
方法：limit_order_cancel  
功能：取消您在给定市场中的订单  
参数：  
    order_numbers(list)：要取消的限价单的ID  
    account：操作人账户名  
示例：
```python
pprint(gph.limit_order_cancel(order_numbers=["1.7.1"], account="test1"))
```
###### 见证人相关


----------
方法：create_witness  
功能：创建见证人候选人  
参数：  
    account_name：见证人候选人账户  
    url：见证人网页链接  
    key：见证人块签名公钥  
示例：
```python
pprint(gph.create_witness(account_name="test2", url="", key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"))
```
方法：approve_witness  
功能：为见证人候选人投票  
参数：  
    witnesses(list)：见证人账户名或见证人ID 
    vote_type：投票类型(0代表理事会，1代表见证人)  
    vote_amount: 投票数量  
    vote_asset：投票所用的资产
    account：投票账户名  
示例：
```python
pprint(gph.approve_witness(witnesses=["test2"], vote_amount=10, vote_asset="1.3.0", account="test1"))
```
###### 理事会相关


----------
方法：committee_member_create  
功能：创建理事会候选人  
参数：  
    url：网页链接  
    account：理事会候选人的账户  
示例：
```python
pprint(gph.committee_member_create(url=" ", account="test2"))
```
方法：committee_member_update  
功能：更新理事会候选人  
参数： 
    work_status: 状态  
    new_url：新的网页链接  
    account：更新的理事会候选人的账户  
示例：
```python
pprint(gph.committee_member_update(work_status=True, new_url=" ", account="test2"))
```
###### 提议相关


----------
方法：relate_world_view  
功能：关联世界观，开发者只有在关联了某一个世界观后，才可以创建这个世界观的NH资产，该操作需要通过提议来完成，需要此世界观的创建者审批  
参数：  
    world_view：世界观名称  
    account：关联人账户名  
示例：
```python
gph = Graphene(node=nodeAddress, blocking=True, proposer="xxx") #proposer为关联世界观的创建者
pprint(gph.relate_world_view(world_view="DRBALL", account="test2"))
```
方法：approveproposal  
功能：批准其他用户关联自己的世界观的提议  
参数：  
    proposal_ids(list)：提议ID  
    account：更新提议的账户  
示例：
```python
pprint(gph.approveproposal(proposal_ids=["1.10.1"], account="test1"))
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

 
