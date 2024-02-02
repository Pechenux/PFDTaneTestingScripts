import json

import numpy as np

from tools.measure_time import measure_time
from tools.measure_memory import measure_memory
from tools.executeTane import execTane, loadTane, execfullTane
from generation.generate_common_tane_data import generate_common_tane_data


ERROR_VALUES_1 = np.array([0, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5])
ERROR_VALUES_1 = np.round(ERROR_VALUES_1, 3)

# ERROR_VALUES_2 = np.arange(0.025, 1, STEP)
# ERROR_VALUES_2 = np.round(ERROR_VALUES_2, 3)

TEST_COUNT = 10

def generate_tane_data():
    experiments = None
    with open('generation/parameters.json') as fp:
        experiments = json.load(fp)

    for test_run in range(TEST_COUNT):
        generate_common_tane_data(test_run, 'tane_time_1', experiments, ERROR_VALUES_1, measure_time, execTane, loadTane)
        generate_common_tane_data(test_run, 'tane_memory_1', experiments, ERROR_VALUES_1, measure_memory, execfullTane)