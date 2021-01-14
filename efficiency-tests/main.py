from rethinkdb_test import RethinkTest
from mongodb_test import MongoTest
import matplotlib.pyplot as plt


def plot_result(rethink_data: list, mongo_data: list, test_name: str):
    rethink_time_series = [row['time'] for row in sorted(rethink_data, key=lambda x: x['id'])]
    mongo_time_series = [row['time'] for row in sorted(mongo_data, key=lambda x: x['id'])]

    print(rethink_time_series)
    print(mongo_time_series)

    plt.plot(rethink_time_series)
    plt.plot(mongo_time_series)

    plt.legend(['RethinkDb', 'MongoDb'])
    plt.xlabel('number of iterations')
    plt.ylabel('time (s)')

    plt.savefig(f'{test_name}.png')
    plt.close()


if __name__ == '__main__':

    iterations_num = 1_000
    tests = ['inserts', 'read_write']

    for test_name in tests:
        print(f'TEST: {test_name}')
        print("RethinkDb")
        rethink_test = RethinkTest(test_name)
        getattr(rethink_test, f'test_{test_name}_efficiency')(iterations_num)

        print("MongoDb")
        mongo_test = MongoTest(test_name)
        getattr(mongo_test, f'test_{test_name}_efficiency')(inserts_num=iterations_num)

        plot_result(
            rethink_data=rethink_test.get_results(test_name),
            mongo_data=mongo_test.get_results(test_name),
            test_name=test_name
        )
