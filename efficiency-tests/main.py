from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
from pymongo import MongoClient
import matplotlib.pyplot as plt
import time


class RethinkTest:

    def __init__(self, collection: str):
        r.connect('localhost', 28015).repl()
        try:
            r.db('test').table_drop(collection).run()
        except ReqlRuntimeError:
            pass
        r.db('test').table_create(collection).run()

    @classmethod
    def test_inserts_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('inserts').insert({'id': idx, 'time': time.time() - start}).run()
            idx += 1

        print('test finished')

    @classmethod
    def test_read_write_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('read_write').insert({'id': idx, 'time': time.time() - start}).run()
            r.table('read_write').run()
            idx += 1

        print('test finished')

    @classmethod
    def get_results(cls, schema) -> list:
        return list(r.table(schema).run())


class MongoTest:

    def __init__(self, collection: str):
        mongo_cli = MongoClient('127.0.0.1', 27017)
        self.db = mongo_cli.test
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


def plot_result(rethink_data: list, mongo_data: list, test_name: str):
    rethink_time_series = [row['time'] for row in sorted(rethink_data, key=lambda x: x['id'])]
    mongo_time_series = [row['time'] for row in sorted(mongo_data, key=lambda x: x['id'])]

    print(rethink_time_series)
    print(mongo_time_series)

    plt.plot(rethink_time_series)
    plt.plot(mongo_time_series)

    plt.legend(['RethinkDb', 'MongoDb'])
    plt.xlabel('number of inserted rows')
    plt.ylabel('time (s)')

    plt.savefig(f'{test_name}.png')


if __name__ == '__main__':

    inserts_number = 1_000
    test_name = 'read_write'

    rethink_test = RethinkTest(test_name)
    rethink_test.test_read_write_efficiency(inserts_num=inserts_number)

    mongo_test = MongoTest(test_name)
    mongo_test.test_read_write_efficiency(inserts_num=inserts_number)

    plot_result(
        rethink_data=rethink_test.get_results(test_name),
        mongo_data=mongo_test.get_results(test_name),
        test_name=test_name
    )
