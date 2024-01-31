import json

import numpy as np

from tools.measure_time import measure_time
from tools.measure_memory import measure_memory
from tools.executePFDTane import execPFDTane
from generation.generate_common_data import generate_common_data


STEP = 0.025
ERROR_VALUES = np.arange(0, 1 + STEP, STEP)
ERROR_VALUES = np.round(ERROR_VALUES, 3)

def generate_pfdtane_data():
    experiments = None
    with open('generation/parameters.json') as fp:
        experiments = json.load(fp)

    generate_common_data('pfdtane_time', experiments, ERROR_VALUES, measure_time, execPFDTane)
    generate_common_data('pfdtane_memory', experiments, ERROR_VALUES, measure_memory, execPFDTane)