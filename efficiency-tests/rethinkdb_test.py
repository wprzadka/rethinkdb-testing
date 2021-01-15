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
    def test_sorting_efficiancy(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('read_write').insert({'id': idx, 'time': time.time() - start}).run()
            r.table('read_write').orderBy({'index': r.desc('id')})
            idx += 1

        print('test finished')

    @classmethod
    def test_join_table_efficiancy(cls, iterations_num: int):
        print('test started')
        idx = 0
        current_iteration = 0

        while current_iteration < iterations_num:

            current_iteration += 1

            while idx < current_iteration * iterations_num:
                r.table('join_table_first').insert({'id': idx, 'a': f'a_value_{idx}'}).run()
                idx += 1

            while idx < 2 * current_iteration * iterations_num:
                r.table('join_table_second').insert({'id': idx, 'b': f'b_value_{idx}'}).run()
                idx += 1

            start = time.time()
            r.table('join_table_first').eq_join('id', r.table('join_table_second')).zip().run()
            end = time.time()
            r.table('join_table').insert({'id': iterations_num, 'time': end - start}).run()

        print('test finished')

    @classmethod
    def test_search_row_efficiancy(cls, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            r.table('table_key').insert({'id': idx, 'time': time.time() - start}).run()
            idx += 1

        r.table('table_key').get('345')

        print('test finished')

    @classmethod
    def test_copy_table_efficiancy(cls, inserts_num: int):
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
