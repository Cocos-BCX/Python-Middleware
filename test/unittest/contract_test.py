import unittest

from config import Config


class ContractTestCase(unittest.TestCase):
    def testCreateContract(self):
        data = """
                function hello()
                    chainhelper:log('Hello World! Hello Python')
                end"""

        params = {
            "name": "contract.test02",
            "data": data,
            "con_authority": "COCOS5gnHLSysPddPg8aHmgxbdt6JoDJHKtJiW57UkL854C3sW9BXoK",
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("CreateContract:", gph.create_contract(**params))
        except Exception as e:
            print(repr(e))

    def testReviseContract(self):
        data = """
                function hello()
                    chainhelper:log('Hello World! Hello')
                end"""

        params = {
            "contract": "contract.test02",
            "data": data,
            "account": "1.2.26"
        }
        gph = Config().gph
        try:
            print("ReviseContract:", gph.revise_contract(**params))
        except Exception as e:
            print(repr(e))

    def testCallContractFunction(self):
        params = {
            "contract": "contract.test02",
            "function": "hello",
            "value_list": [],
            "account": "1.2.25"
        }
        gph = Config().gph
        try:
            print("CallContractFunction:", gph.call_contract_function(**params))
        except Exception as e:
            print(repr(e))
            

if __name__ == "__main__":
    case1 = ContractTestCase("testCreateContract")
    case1()
    case2 = ContractTestCase("testReviseContract")
    case2()
    case3 = ContractTestCase("testCallContractFunction")
    case3()