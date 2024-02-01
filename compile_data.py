import os
from numpy import result_type

import pandas as pd
from dataclasses import dataclass
from functools import reduce

from tools.confidence_interval import mean_confidence_interval

@dataclass
class DatasetTest:
    filename: str
    algo: str
    perf: str
    measure: str
    only_error_measure: None | int
    run_count: int


def get_max_runs_count(filename, algo, perf, measure, error_range, max_count):
    for run_number in range(max_count - 1, -1, -1):
        if os.path.exists(f"out/{filename}/{run_number}/{algo}_{perf}_{error_range}_{measure}.csv"):
            return run_number + 1
    return -1

def get_dataframe_with_sum_values(filename, algo, perf, measure, error_range, run_number):
    data = pd.read_csv(f"out/{filename}/{run_number}/{algo}_{perf}_{error_range}_{measure}.csv", sep=' ')
    data[f"value_{run_number}"] = data['value_exec'] + data['value_load']
    return data[['error', f"value_{run_number}"]]

def get_all_data(filename, algo, perf, measure, error_range, max_count):
    dataframes = []
    for run_count in range(max_count):
        dataframes.append(get_dataframe_with_sum_values(filename, algo, perf, measure, error_range, run_count))
    return dataframes

def concat_dataframes(dataframes):
    return pd.concat(dataframes).sort_values(by='error')

def merge_dataframes(dataframes):
    return reduce(lambda  left, right: pd.merge(left,right,on=['error']), dataframes)

def combine_values(dataframe):
    dataframe[['value', 'h']] = dataframe[dataframe.columns[1:]].apply(lambda row: mean_confidence_interval(row.to_numpy()), axis=1, result_type='expand')
    return dataframe[['error', 'value', 'h']]


to_process: list[DatasetTest] = []

for filename in os.listdir('out'):
    if os.path.isdir(f"out/{filename}"):
        max_test_runs_count = len(os.listdir(f"out/{filename}"))
        for algo in ['pfdtane', 'tane']:
            for perf in ['time', 'memory']:
                for measure in ['per_value', 'per_tuple']:
                    err_range_1 = get_max_runs_count(filename, algo, perf, measure, 1, max_test_runs_count)
                    err_range_2 = get_max_runs_count(filename, algo, perf, measure, 2, max_test_runs_count)
                    min_run_count = min(err_range_1, err_range_2)
                    if min_run_count > 0:
                        to_process.append(DatasetTest(filename, algo, perf, measure, None, min_run_count))
                    else:
                        if err_range_1 > 0:
                            to_process.append(DatasetTest(filename, algo, perf, measure, 1, err_range_1))
                        elif err_range_2 > 0:
                            to_process.append(DatasetTest(filename, algo, perf, measure, 2, err_range_2))
                        else:
                            print("Not including", filename, algo, perf, measure, min_run_count, err_range_1, err_range_2)

report = ""

for dataset_test in to_process:
    if (dataset_test.only_error_measure == None):
        dataframes_1 = get_all_data(dataset_test.filename, dataset_test.algo, dataset_test.perf, dataset_test.measure, 1, dataset_test.run_count)
        dataframes_1 = merge_dataframes(dataframes_1)
        dataframes_2 = get_all_data(dataset_test.filename, dataset_test.algo, dataset_test.perf, dataset_test.measure, 2, dataset_test.run_count)
        dataframes_2 = merge_dataframes(dataframes_2)
        dataframe = concat_dataframes([dataframes_1, dataframes_2])
        dataframe = combine_values(dataframe)
    else:
        dataframes = get_all_data(dataset_test.filename, dataset_test.algo, dataset_test.perf, dataset_test.measure, dataset_test.only_error_measure, dataset_test.run_count)
        dataframe = merge_dataframes(dataframes)
        dataframe = combine_values(dataframe)

    report += str(dataset_test) + '\n'
    
    dataframe.to_csv(path_or_buf=f'out/{dataset_test.algo}_{dataset_test.perf}_{dataset_test.measure}_{dataset_test.filename}.csv', sep=' ', encoding='utf-8', index=False)

with open('out/report.txt', 'w') as report_file:
    report_file.write(report)
