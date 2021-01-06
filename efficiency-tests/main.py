from rethinkdb import r
from rethinkdb.errors import ReqlRuntimeError
import matplotlib.pyplot as plt
import time

def prepare_db() -> None:
    r.connect('localhost', 28015).repl()
    try:
        r.db('test').table_drop('inserts').run()
    except ReqlRuntimeError:
        pass
    r.db('test').table_create('inserts').run()


def test_efficiency(inserts_num: int) -> None:
    idx = 0
    print('test started')

    start = time.time()
    while idx < inserts_num:
        r.table('inserts').insert({'id': idx, 'time': time.time() - start}).run()
        idx += 1

    print('test finished')


def plot_result():
    data = sorted(list(r.table('inserts').run()), key=lambda x: x['id'])
    time_series = [row['time'] for row in data]

    # print(time_series)
    plt.plot(time_series)
    plt.savefig('inserts.png')


if __name__ == '__main__':

    inserts_number = 100

    prepare_db()
    test_efficiency(inserts_num=inserts_number)
    plot_result()
