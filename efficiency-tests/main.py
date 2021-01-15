from rethinkdb_test import RethinkTest
from mongodb_test import MongoTest
from couchdb_test import CouchTest
import matplotlib.pyplot as plt


def plot_result(
        data_series_li: list,
        series_names_li: list,
        test_case_name: str
):
    time_series = [
        [row['time'] for row in sorted(series, key=lambda x: x['id'])]
        for series in data_series_li
    ]

    # mongo_time_series = [row['time'] for row in sorted(mongo_data, key=lambda x: x['id'])]
    # couch_time_series = [row['time'] for row in sorted(couch_data, key=lambda x: x['id'])]
    # print(rethink_time_series)
    # print(mongo_time_series)
    # print(couch_time_series)
    for name, series in zip(series_names_li, time_series):
        print(f'{name}: {series}')

    for series in time_series:
        plt.plot(series)

    plt.legend(series_names_li)
    plt.xlabel('number of iterations')
    plt.ylabel('time (s)')

    plt.savefig(f'./plots/{test_case_name}.png')
    plt.close()


if __name__ == '__main__':

    iterations_num = 5_00
    tests = ['inserts', 'read_write']

    for test_name in tests:
        test_func_name = f'test_{test_name}_efficiency'
        print(f'TEST: {test_name}')

        series_names = []
        data_series = []

        if hasattr(RethinkTest, test_func_name):
            print('RethinkDb')
            rethink_test = RethinkTest(test_name)
            getattr(rethink_test, test_func_name)(iterations_num)

            data_series.append(rethink_test.get_results(test_name))
            series_names.append('RethinkDb')

        if hasattr(MongoTest, test_func_name):
            print('MongoDb')
            mongo_test = MongoTest(test_name)
            getattr(mongo_test, test_func_name)(iterations_num)

            data_series.append(mongo_test.get_results(test_name))
            series_names.append('MongoDb')

        if hasattr(MongoTest, test_func_name):
            print('Couchdb')
            couch_test = CouchTest(test_name)
            getattr(couch_test, test_func_name)(iterations_num)

            data_series.append(couch_test.get_results(test_name))
            series_names.append('Couchdb')


        plot_result(
            data_series_li=data_series,
            series_names_li=series_names,
            test_case_name=test_name
        )
