from pymongo import MongoClient, ASCENDING
import time
import random


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

    def test_sorting_efficiency(self, inserts_num: int):
        idx = 0
        mod = inserts_num / min(100, inserts_num)

        self.db.source.drop()

        print('test started')

        while idx < inserts_num:
            self.db.source.insert_one({'value': idx})
            if idx % mod == 0:
                start = time.time()
                for row in self.db.source.find().sort('value', ASCENDING):
                    print(row, end=', ')
                end = time.time()
                print()
                self.db.sorting.insert_one({'id': idx, 'time': end - start})
            idx += 1

        print('test finished')

    def test_join_table_efficiency(self, inserts_num: int):

        self.db.join_table_first.drop()
        self.db.join_table_second.drop()

        print('test started')

        idx = 0
        current_iteration = 0

        while current_iteration < inserts_num:

            current_iteration += 1

            fst_idx = idx
            while fst_idx < current_iteration * inserts_num:
                self.db.join_table_first.insert_one({'id': fst_idx, 'a': f'a_value_{fst_idx}'})
                fst_idx += 1
            snd_idx = idx
            while snd_idx < current_iteration * inserts_num:
                self.db.join_table_second.insert_one({'id': snd_idx, 'b': f'b_value_{snd_idx}'})
                snd_idx += 1
            idx += current_iteration * inserts_num

            start = time.time()
            self.db.join_table_first.aggregate([{
                '$lookup': {
                    'from': 'join_table_second',
                    'localField': 'id',
                    'foreignField': 'id',
                    'as': 'joined'
                }
            }])
            end = time.time()
            self.db.join_table.insert_one({'id': current_iteration, 'time': end - start})

        print('test finished')

    def test_search_row_by_id_10_times_efficiency(self, inserts_num: int):
        idx = 0
        mod = inserts_num / min(100, inserts_num)

        self.db.source.drop()

        random.seed(87747)
        print('test started')

        while idx < inserts_num:
            self.db.source.insert_one({'_id': idx})
            if idx % mod == 0:
                start = time.time()
                for _ in range(10):
                    print(self.db.source.find({'_id': random.randint(0, idx)}).next(), end=', ')
                end = time.time()
                print()
                self.db.search_row_by_id_10_times.insert_one({'id': idx, 'time': end - start})
            idx += 1

        print('test finished')

    def test_search_row_by_value_10_times_efficiency(self, inserts_num: int):
        idx = 0
        mod = inserts_num / min(100, inserts_num)

        self.db.source.drop()

        random.seed(87747)
        print('test started')

        while idx < inserts_num:
            self.db.source.insert_one({'value': idx})
            if idx % mod == 0:
                start = time.time()
                for _ in range(10):
                    print(self.db.source.find({'value': random.randint(0, idx)}).next(), end=', ')
                end = time.time()
                print()
                self.db.search_row_by_value_10_times.insert_one({'id': idx, 'time': end - start})
            idx += 1

        print('test finished')

    def test_copy_table_efficiency(self, iterations_num: int):
        idx = 0
        mod = iterations_num / min(10, iterations_num)

        self.db.table_to_copy.drop()
        self.db.source.drop()

        print('test started')

        while idx < iterations_num:
            self.db.source.insert_one({'value': idx})
            if idx % mod == 0:
                start = time.time()
                self.db.table_to_copy.insert_many(self.db.source.find())
                end = time.time()
                self.db.copy_table.insert_one({'id': idx, 'time': end - start})
                self.db.table_to_copy.drop()
            idx += 1

        print('test finished')

    def get_results(self, schema: str) -> list:
        return list(self.db[schema].find())