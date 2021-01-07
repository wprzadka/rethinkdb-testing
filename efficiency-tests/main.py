from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
from pymongo import MongoClient
import matplotlib.pyplot as plt
import time


class RethinkTest:

    def __init__(self):
        r.connect('localhost', 28015).repl()
        try:
            r.db('test').table_drop('inserts').run()
        except ReqlRuntimeError:
            pass
        r.db('test').table_create('inserts').run()

    @classmethod
    def test_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('inserts').insert({'id': idx, 'time': time.time() - start}).run()
            idx += 1

        print('test finished')

    @classmethod
    def get_results(cls) -> list:
        return list(r.table('inserts').run())


class MongoTest:

    def __init__(self):
        mongo_cli = MongoClient('127.0.0.1', 27017)
        self.db = mongo_cli.test
        self.db.inserts.drop()

    def test_efficiency(self, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            self.db.inserts.insert_one({'id': idx, 'time': time.time() - start})
            idx += 1

        print('test finished')

    def get_results(self) -> list:
        return list(self.db.inserts.find())


def plot_result(rethink_data: list, mongo_data: list):
    rethink_time_series = [row['time'] for row in sorted(rethink_data, key=lambda x: x['id'])]
    mongo_time_series = [row['time'] for row in sorted(mongo_data, key=lambda x: x['id'])]

    print(rethink_time_series)
    print(mongo_time_series)

    plt.plot(rethink_time_series)
    plt.plot(mongo_time_series)

    plt.legend(['RethinkDb', 'MongoDb'])
    plt.xlabel('number of inserted rows')
    plt.ylabel('time (s)')

    plt.savefig('inserts.png')


if __name__ == '__main__':

    inserts_number = 10_000

    rethink_test = RethinkTest()
    rethink_test.test_efficiency(inserts_num=inserts_number)

    mongo_test = MongoTest()
    mongo_test.test_efficiency(inserts_num=inserts_number)

    plot_result(
        rethink_data=rethink_test.get_results(),
        mongo_data=mongo_test.get_results()
    )
