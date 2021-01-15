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

    for name, series in zip(series_names_li, time_series):
        print(f'{name}: {series}')

    for series in time_series:
        plt.plot(series)

    plt.legend(series_names_li)
    plt.xlabel('number of iterations')
    plt.ylabel('time (s)')

    plt.savefig(f'./plots/{test_case_name}.png')
    plt.close()


def get_average_time(data_series: list):
    return data_series[-1]['time'] / len(data_series)


if __name__ == '__main__':

    iterations_num = 1_00
    tests = [('join_table', True)]
    # [('join_table', True), ('inserts', True), ('read_write', True)]

    for test_name, recreate_collection in tests:
        test_func_name = f'test_{test_name}_efficiency'
        print(f'TEST: {test_name}')

        series_names = []
        data_series = []

        if hasattr(RethinkTest, test_func_name):
            print('RethinkDb')
            rethink_test = RethinkTest(test_name, recreate_collection)
            getattr(rethink_test, test_func_name)(iterations_num)

            data_series.append(rethink_test.get_results(test_name))
            series_names.append('RethinkDb')
            print(f'RethinkDb average operation time: {get_average_time(rethink_test.get_results(test_name))}')

        if hasattr(MongoTest, test_func_name):
            print('MongoDb')
            mongo_test = MongoTest(test_name, recreate_collection)
            getattr(mongo_test, test_func_name)(iterations_num)

            data_series.append(mongo_test.get_results(test_name))
            series_names.append('MongoDb')
            print(f'MongoDb average operation time: {get_average_time(mongo_test.get_results(test_name))}')

        if hasattr(CouchTest, test_func_name):
            print('Couchdb')
            couch_test = CouchTest(test_name, recreate_collection)
            getattr(couch_test, test_func_name)(iterations_num)

            data_series.append(couch_test.get_results(test_name))
            series_names.append('Couchdb')
            print(f'Couchdb average operation time: {get_average_time(couch_test.get_results(test_name))}')

        plot_result(
            data_series_li=data_series,
            series_names_li=series_names,
            test_case_name=test_name
        )
