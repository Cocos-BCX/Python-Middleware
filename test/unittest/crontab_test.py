import unittest

from config import Config


class CrontabTestCase(unittest.TestCase):
    def testCreateCrontab(self):
        params = {
            "to" : "testaccount7",
            "amount": "100",
            "asset": "1.3.0",
            "memo" : "",
            "account" : "1.2.14"
        }
        gph = Config(crontaber="1.2.14", crontab_start_time="2019-08-08T06:52:00", crontab_execute_interval=30, crontab_scheduled_execute_times=10).gph
        try:
            print("CreateCrontab:", gph.transfer(**params))
        except Exception as e:
            print(repr(e))

    def testCancelCrontab(self):
        params = {
            "task": "1.12.3",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("CancelCrontab", gph.crontab_cancel(**params))
        except Exception as e:
            print(repr(e))

    def testRecoverCrontab(self):
        params = {
            "crontab": "1.12.3",
            "restart_time": "2019-08-08T06:55:00",
            "account": "1.2.14"
        }
        gph = Config().gph
        try:
            print("RecoverCrontab:", gph.crontab_recover(**params))
        except Exception as e:
            print(repr(e))

            

if __name__ == "__main__":
    # case1 = CrontabTestCase("testCreateCrontab")
    # case1()
    case2 = CrontabTestCase("testCancelCrontab")
    case2()
    # case3 = CrontabTestCase("testRecoverCrontab")
    # case3()