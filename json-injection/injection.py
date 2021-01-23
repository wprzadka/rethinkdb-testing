from rethinkdb import r

if __name__ == '__main__':

    # test cases from:
    # https://github.com/fuzzdb-project/fuzzdb
    with open('data.txt', 'r') as file:
        test_cases = file.readlines()

    with r.connect('127.0.0.1', 28015).repl() as conn:

        if 'json_injection' not in r.db('test').table_list().run():
            r.db('test').table_create('json_injection').run()

        for case in test_cases:
            print(r.table('json_injection').insert({'key': case}).run())

        print(r.table('json_injection').run())
