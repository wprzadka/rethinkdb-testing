from pymongo import MongoClient
import time


class MongoTest:

    def __init__(self, collection: str, recreate: bool):
        mongo_cli = MongoClient('127.0.0.1', 27017)
        self.db = mongo_cli.test
        if recreate:
            self.db[collection].drop()

    def test_inserts_efficiency(self, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            self.db.inserts.insert_one({'id': idx, 'time': time.time() - start})
            idx += 1

        print('test finished')

    def test_read_write_efficiency(self, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            self.db.read_write.insert_one({'id': idx, 'time': time.time() - start})
            self.db.read_write.find()
            idx += 1

        print('test finished')

    def get_results(self, schema: str) -> list:
        return list(self.db[schema].find())
