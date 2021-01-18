from rethinkdb import r
import time

if __name__ == '__main__':
    with r.connect('localhost', 28016).repl() as conn:
        if 'proxy_test' not in r.db('test').table_list().run():
            r.db('test').table_create('proxy_test').run()

        r.db('test').insert({'source': 'client', 'time': time.time()})
        r.db('test').run()
