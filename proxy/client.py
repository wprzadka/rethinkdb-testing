from rethinkdb import r
import time

if __name__ == '__main__':
    with r.connect('127.0.0.1', 28016).repl() as conn:
        if 'proxy_test' not in r.db('test').table_list().run():
            r.db('test').table_create('proxy_test').run()

        r.table('proxy_test').insert({'source': 'client', 'time': time.time()}).run()
        print(r.table('proxy_test').run())
