import os

import pandas as pd
from tabloo import show
from functools import reduce

from tools.confidence_interval import mean_confidence_interval


def get_pfdtane_file_name(folder, dataset, perf, measure, error_range, run_number):
    return f"{folder}/{dataset}/{run_number}/pfdtane_{perf}_{error_range}_{measure}.csv"

def get_dataframe_with_sum_values(folder, dataset, perf, measure, error_range, run_number):
    filename = get_pfdtane_file_name(folder, dataset, perf, measure, error_range, run_number)

    data = pd.read_csv(filename, sep=' ')
    data[f"value_{run_number}"] = data['value_exec'] + data['value_load']
    return data[['error', f"value_{run_number}"]].sort_values(by='error')

def get_all_data(folder, dataset, perf, measure, error_range, max_count):
    dataframes = []
    for run_count in range(max_count):
        dataframes.append(get_dataframe_with_sum_values(folder, dataset, perf, measure, error_range, run_count))
    return dataframes

def concat_dataframes(dataframes):
    return pd.concat(dataframes).sort_values(by='error')

def merge_dataframes(dataframes):
    return reduce(lambda  left, right: pd.merge(left,right,on=['error']), dataframes)

def combine_values(dataframe):
    dataframe[['value', 'h']] = dataframe[dataframe.columns[1:]].apply(lambda row: mean_confidence_interval(row.to_numpy()), axis=1, result_type='expand')
    return dataframe[['error', 'value', 'h']]


for dataset in ['measures_v2', 'jena_climate_2009_2016', 'BKB_WaterQualityData_2020084']:
    for measure in ['per_value', 'per_tuple']:
        run_count_1 = 10
        run_count_2 = 22
        run_count_3 = 20

        dataframes_1 = get_all_data('out', dataset, 'time', measure, 1, run_count_1)
        dataframes_1 = merge_dataframes(dataframes_1)
        
        dataframes_2 = get_all_data('out', dataset, 'time', measure, 2, run_count_1)
        dataframes_2 = merge_dataframes(dataframes_2)

        dataframes = [concat_dataframes([dataframes_1, dataframes_2])]

        if (dataset == 'measures_v2'):
            dataframes_3 = get_all_data('out', dataset, 'time', measure, 3, run_count_2)
            dataframes_3 = merge_dataframes(dataframes_3)
            dataframes_3 = dataframes_3.add_suffix('_3')
            dataframes_3.rename(columns={'error_3': 'error'}, inplace=True)
            dataframes.append(dataframes_3)

        dataframes_4 = get_all_data('AdditionalData', dataset, 'time', measure, 3, run_count_3)
        # show(dataframes_4[0])
        dataframes_4 = merge_dataframes(dataframes_4)
        dataframes_4 = dataframes_4.add_suffix('_4')
        dataframes_4.rename(columns={'error_4': 'error'}, inplace=True)
        dataframes.append(dataframes_4)

        dataframe = merge_dataframes(dataframes)

        # show(dataframe[["error", "value_0_4"]])
        
        dataframe = combine_values(dataframe)

        # show(dataframe)

        dataframe.to_csv(path_or_buf=f'out/pfdtane_time_{measure}_{dataset}.csv', sep=' ', encoding='utf-8', index=False)

        # break
    # break

import os
if not os.path.exists('./out/paper'):
    os.makedirs('./out/paper')
if not os.path.exists('./out/paper/exp1'):
    os.makedirs('./out/paper/exp1')
if not os.path.exists('./out/paper/exp2'):
    os.makedirs('./out/paper/exp2')
if not os.path.exists('./out/paper/exp2/band'):
    os.makedirs('./out/paper/exp2/band')
if not os.path.exists('./out/paper/exp2/bar'):
    os.makedirs('./out/paper/exp2/bar')
if not os.path.exists('./out/paper/exp3'):
    os.makedirs('./out/paper/exp3')