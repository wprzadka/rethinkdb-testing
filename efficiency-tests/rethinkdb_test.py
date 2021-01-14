from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
import time


class RethinkTest:

    def __init__(self, collection: str):
        r.connect('localhost', 28015).repl()
        try:
            r.db('test').table_drop(collection).run()
        except ReqlRuntimeError:
            pass
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
    def get_results(cls, schema) -> list:
        return list(r.table(schema).run())
