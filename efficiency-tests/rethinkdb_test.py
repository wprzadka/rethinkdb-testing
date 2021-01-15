from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
import time


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
    def test_sorting_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('read_write').insert({'id': idx, 'time': time.time() - start}).run()
            r.table('read_write').orderBy({'index': r.desc('id')})
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
    def test_search_row_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('table_key').insert({'id': idx, 'time': time.time() - start}).run()
            idx += 1

        r.table('table_key').get('345')

        print('test finished')

    @classmethod
    def test_copy_table_efficiency(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('table_copy').insert({'id': idx, 'time': time.time() - start}).run()
            idx += 1

        r.table('talbe_to_copy').insert(r.table('table_copy')).run()

        print('test finished')

    @classmethod
    def get_results(cls, schema) -> list:
        return list(r.table(schema).run())
