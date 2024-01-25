import numpy as np
import json

from measure_time import measure_time
from measure_memory import measure_memory
from executePFDTane import execPFDTane
from run_tests import run_tests

error_values = np.arange(0, 1, 0.025)
TEST_COUNT = 50
CONFIDENCE = 0.95

def run_experiment_1():
    with open('experiments_1.json') as fp:
        experiments = json.load(fp)

        for table in experiments["tables"]:
            print('Running:', table['TABLE'])
            experiments_list = table['experiments']
            for i in range(len(experiments_list)):
                print('Experiment with parameters:', experiments_list[i])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)
                    for erroe_value in error_values:
                        print('Error:', erroe_value)
                        parameters = {
                            "TABLE": table['TABLE'],
                            "SEPARATOR": table['SEPARATOR'],
                            "HAS_HEADER": table['HAS_HEADER'],
                            "ISNULLEQNULL": True,
                            "ERROR": erroe_value,
                            "ERROR_MEASURE": error_measure,
                            "MAXLHS": 5
                        }
                        print('  Time:', run_tests(measure_time, execPFDTane, parameters, TEST_COUNT, CONFIDENCE))
                        print('  Memory:', run_tests(measure_memory, execPFDTane, parameters, TEST_COUNT, CONFIDENCE))
    
