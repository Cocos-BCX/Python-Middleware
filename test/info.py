#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PythonMiddleware.graphene import Graphene
from PythonMiddleware.instance import set_shared_graphene_instance
from pprint import pprint

import time

#nodeAddress = "wss://api.cocosbcx.net" 
nodeAddress = "ws://test.cocosbcx.net" 
#nodeAddress = "ws://127.0.0.1:8049" 
gph = Graphene(node=nodeAddress) 
set_shared_graphene_instance(gph) 

while True:
    print('>> info')
    pprint(gph.info())
    time.sleep(2)
    
