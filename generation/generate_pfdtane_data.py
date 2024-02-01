import json

import numpy as np

from tools.measure_time import measure_time
from tools.measure_memory import measure_memory
from tools.executePFDTane import execPFDTane, loadPFDTane, execfullPFDTane
from generation.generate_common_data import generate_common_data


# STEP = 0.025
STEP = 0.05
ERROR_VALUES_1 = np.arange(0, 1 + STEP, STEP)
ERROR_VALUES_1 = np.round(ERROR_VALUES_1, 3)

ERROR_VALUES_2 = np.arange(0.025, 1, STEP)
ERROR_VALUES_2 = np.round(ERROR_VALUES_2, 3)

TEST_COUNT = 10

def generate_pfdtane_data():
    experiments = None
    with open('generation/parameters.json') as fp:
        experiments = json.load(fp)

    for test_run in range(TEST_COUNT):
        generate_common_data(test_run, 'pfdtane_time_1', experiments, ERROR_VALUES_1, measure_time, execPFDTane, loadPFDTane)
        # generate_common_data(test_run, 'pfdtane_memory_1', experiments, ERROR_VALUES_1, measure_memory, execfullPFDTane)

        # generate_common_data(test_run, 'pfdtane_time_2', experiments, ERROR_VALUES_2, measure_time, execPFDTane, loadPFDTane)
        # generate_common_data(test_run, 'pfdtane_memory_2', experiments, ERROR_VALUES_2, measure_memory, execfullPFDTane)