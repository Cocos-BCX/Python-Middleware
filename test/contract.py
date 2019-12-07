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

#创建钱包
if gph.wallet.created() is False: 
    gph.newWallet("123456")

#钱包解锁
if gph.wallet.locked() is True:
    gph.wallet.unlock("123456")

#add key
if gph.wallet.getAccountFromPublicKey(pub) is None:
    gph.wallet.addPrivateKey(privateKey) #账号私钥导入钱包
pprint(gph.wallet.getPrivateKeyForPublicKey(pub))

#config
config["default_prefix"] = gph.rpc.chain_params["prefix"] # 向钱包数据库中添加默认信息
config["default_account"] = defaultAccount # 向钱包数据库中添加默认信息

#account test
#pprint(gph.wallet.removeAccount(None))
#pprint(gph.wallet.getAccounts())

#合约创建
#contract_name = "contract.debug.hello"
contract_name = "contract.test1.hello"

data = "function hello() \
    chainhelper:log('Hello World!') \
    chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) \
end "
pprint(gph.create_contract(contract_name, data=data, con_authority=pub, account=defaultAccount))

#合约调用: contract.debug.hello
value_list=[]
#pprint(gph.call_contract_function(contract_name, "hello", value_list=value_list, account=defaultAccount))

# 修改合约内容
revise_data = "function hello() \
    chainhelper:log('hello revise contract test. 2019-08-20 11:13:15') \
    chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) \
end "
#pprint(gph.revise_contract(contract_name, data=revise_data, account=defaultAccount))


#test result data:
#1. 创建合约
'''
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
'''

#2. 调用合约
'''
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
'''

#3. 修改合约内容
‘’‘
tx.buffer>>>: {'ref_block_num': 11181, 'ref_block_prefix': 1022871651, 'extensions': [], 'signatures': ['1f33824255bc213b2b3a1ced2c1dd970ffc11345f95250870179d40154a4432dc11b16a373a8527cb0cf617de49669d52d25ef5fa4a4b6826908132aa674201e4d'], 'operations': [[59, {'reviser': '1.2.15', 'fee': {'amount': 2157226, 'asset_id': '1.3.0'}, 'extensions': [], 'data': "function hello()     chainhelper:log('hello revise contract test. 2019-08-20 11:13:15')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'contract_id': '1.16.2'}]], 'expiration': '2019-09-20T04:15:42'}
tx======>>: {'ref_block_num': 11181, 'ref_block_prefix': 1022871651, 'extensions': [], 'signatures': ['1f33824255bc213b2b3a1ced2c1dd970ffc11345f95250870179d40154a4432dc11b16a373a8527cb0cf617de49669d52d25ef5fa4a4b6826908132aa674201e4d'], 'operations': [[59, {'reviser': '1.2.15', 'fee': {'amount': 2157226, 'asset_id': '1.3.0'}, 'extensions': [], 'data': "function hello()     chainhelper:log('hello revise contract test. 2019-08-20 11:13:15')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'contract_id': '1.16.2'}]], 'expiration': '2019-09-20T04:15:42'}
transaction>>>: {'ref_block_num': 11181, 'ref_block_prefix': 1022871651, 'extensions': [], 'signatures': ['1f33824255bc213b2b3a1ced2c1dd970ffc11345f95250870179d40154a4432dc11b16a373a8527cb0cf617de49669d52d25ef5fa4a4b6826908132aa674201e4d'], 'operations': [[59, {'reviser': '1.2.15', 'fee': {'amount': 2157226, 'asset_id': '1.3.0'}, 'extensions': [], 'data': "function hello()     chainhelper:log('hello revise contract test. 2019-08-20 11:13:15')     chainhelper:log(date('%Y-%m-%dT%H:%M:%S', chainhelper:time())) end ", 'contract_id': '1.16.2'}]], 'expiration': '2019-09-20T04:15:42'}
['9e46323a09989f4b302ad717f7ec1d31237c7b94468cb7a8098f5b508b813894',
 {'block': 76718,
  'expiration': '2019-09-20T04:15:42',
  'extensions': [],
  'operation_results': [[5,
                         {'message': 'e11db591ee109c7e46de186ab93335792c2b6c8cbf69a03a10a3670e603183b0',
                          'real_running_time': 1017}]],
  'operations': [[59,
                  {'contract_id': '1.16.2',
                   'data': "function hello()     chainhelper:log('hello revise "
                           "contract test. 2019-08-20 11:13:15')     "
                           "chainhelper:log(date('%Y-%m-%dT%H:%M:%S', "
                           'chainhelper:time())) end ',
                   'extensions': [],
                   'fee': {'amount': 2157226, 'asset_id': '1.3.0'},
                   'reviser': '1.2.15'}]],
  'ref_block_num': 11181,
  'ref_block_prefix': 1022871651,
  'signatures': ['1f33824255bc213b2b3a1ced2c1dd970ffc11345f95250870179d40154a4432dc11b16a373a8527cb0cf617de49669d52d25ef5fa4a4b6826908132aa674201e4d']}]
’‘’

