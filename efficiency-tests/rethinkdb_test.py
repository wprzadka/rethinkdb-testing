from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
import time
import random


class RethinkTest:

    def __init__(self, collection: str, recreate: bool):
        r.connect('localhost', 28015).repl()

        if recreate:
            try:
                r.db('test').table_drop(collection).run()
            except ReqlRuntimeError:
                pass

        if collection not in r.db('test').table_list().run():
            r.db('test').table_create(collection).run()
        # r.table(collection).reconfigure(shards=2, replicas=1).run()

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
    def test_sorting_efficiency(cls, iterations_num: int):
        idx = 0
        mod = iterations_num / min(100, iterations_num)

        if 'source' in r.db('test').table_list().run():
            r.db('test').table_drop('source').run()
        r.db('test').table_create('source').run()

        print('test started')

        while idx < iterations_num:
            r.table('source').insert({'value': idx}).run()
            if idx % mod == 0:
                start = time.time()
                r.table('source').order_by(r.desc('value')).run()
                end = time.time()
                r.table('sorting').insert({'id': idx, 'time': end - start}).run()
            idx += 1

        print('test finished')

    @classmethod
    def test_join_table_efficiency(cls, iterations_num: int):

        if 'join_table_first' in r.db('test').table_list().run():
            r.db('test').table_drop('join_table_first').run()
        r.db('test').table_create('join_table_first').run()

        if 'join_table_second' in r.db('test').table_list().run():
            r.db('test').table_drop('join_table_second').run()
        r.db('test').table_create('join_table_second').run()

        print('test started')

        idx = 0
        current_iteration = 0

        while current_iteration < iterations_num:

            current_iteration += 1

            fst_idx = idx
            while fst_idx < current_iteration * iterations_num:
                r.table('join_table_first').insert({'id': fst_idx, 'a': f'a_value_{fst_idx}'}).run()
                fst_idx += 1
            snd_idx = idx
            while snd_idx < current_iteration * iterations_num:
                r.table('join_table_second').insert({'id': snd_idx, 'b': f'b_value_{snd_idx}'}).run()
                snd_idx += 1
            idx += current_iteration * iterations_num

            start = time.time()
            r.table('join_table_first').eq_join('id', r.table('join_table_second')).zip().run()
            end = time.time()
            r.table('join_table').insert({'id': current_iteration, 'time': end - start}).run()

        print('test finished')

    @classmethod
    def test_search_row_by_id_10_times_efficiency(cls, iterations_num: int):
        idx = 0
        mod = iterations_num / min(100, iterations_num)

        if 'source' in r.db('test').table_list().run():
            r.db('test').table_drop('source').run()
        r.db('test').table_create('source').run()

        random.seed(87747)
        print('test started')

        while idx < iterations_num:
            r.table('source').insert({'id': idx}).run()
            if idx % mod == 0:
                start = time.time()
                for _ in range(10):
                    print(r.table('source').get(random.randint(0, idx)).run(), end=', ')
                end = time.time()
                print()
                r.table('search_row_by_id_10_times').insert({'id': idx, 'time': end - start}).run()
            idx += 1

        print('test finished')

    @classmethod
    def test_search_row_by_value_10_times_efficiency(cls, iterations_num: int):
        idx = 0
        mod = iterations_num / min(100, iterations_num)

        if 'source' in r.db('test').table_list().run():
            r.db('test').table_drop('source').run()
        r.db('test').table_create('source').run()

        random.seed(87747)
        print('test started')

        while idx < iterations_num:
            r.table('source').insert({'value': idx}).run()
            if idx % mod == 0:
                start = time.time()
                for _ in range(10):
                    print(r.table('source').filter({'value': random.randint(0, idx)}).run(), end=', ')
                end = time.time()
                print()
                r.table('search_row_by_value_10_times').insert({'id': idx, 'time': end - start}).run()
            idx += 1

        print('test finished')

    @classmethod
    def test_copy_table_efficiency(cls, iterations_num: int):
        idx = 0
        mod = iterations_num / min(10, iterations_num)

        if 'table_to_copy' in r.db('test').table_list().run():
            r.db('test').table_drop('table_to_copy').run()
        r.db('test').table_create('table_to_copy').run()

        if 'source' in r.db('test').table_list().run():
            r.db('test').table_drop('source').run()
        r.db('test').table_create('source').run()

        print('test started')

        while idx < iterations_num:
            r.table('source').insert({'value': idx}).run()
            if idx % mod == 0:
                start = time.time()
                r.table('table_to_copy').insert(r.table('source')).run()
                end = time.time()
                r.table('copy_table').insert({'id': idx, 'time': end - start}).run()

                r.db('test').table_drop('table_to_copy').run()
                r.db('test').table_create('table_to_copy').run()
            idx += 1

        print('test finished')

    @classmethod
    def get_results(cls, schema) -> list:
        return list(r.table(schema).run())
