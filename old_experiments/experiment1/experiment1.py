import numpy as np
import json

from tools.measure_time import measure_time
from tools.measure_memory import measure_memory
from tools.executePFDTane import execfullPFDTane
from tools.run_tests import run_tests
from tools.format_for_graph import format_for_graph

error_values = np.arange(0, 1, 0.025)
# error_values = np.arange(0, 1, 0.6) # debug
error_values = np.round(error_values, 3) # round
TEST_COUNT = 20
# TEST_COUNT = 5 # debug
CONFIDENCE = 0.95

# experiments 2a and 2b

def run_experiment_1():
    output_time = ""
    output_memory = ""

    with open('experiment1/experiments_1.json') as fp:
        experiments = json.load(fp)

        # time
        with open('out/experiments_1_time.out', 'w') as fp:
            for table in experiments["tables"]:
                print('Running:', table['TABLE'])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)

                    output_time += f" % {table['TABLE']} {error_measure}\n"

                    for erroe_value in error_values:
                        print('Error:', erroe_value)
                        parameters = {
                            "TABLE": table['TABLE'],
                            "SEPARATOR": table['SEPARATOR'],
                            "HAS_HEADER": table['HAS_HEADER'],
                            "ERROR": erroe_value,
                            "ERROR_MEASURE": error_measure,
                        }
                        test_time_output = run_tests(measure_time, execfullPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Time:', test_time_output)
                        output_time += format_for_graph(erroe_value, test_time_output)
                    
                    output_time += '\n'
                    fp.write(output_time)
                    fp.flush()
                    output_time = ""
        
        # memory
        with open('out/experiments_1_memory.out', 'w') as fp:
            for table in experiments["tables"]:
                print('Running:', table['TABLE'])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)

                    output_memory += f"% {table['TABLE']} {error_measure}\n"

                    for erroe_value in error_values:
                        print('Error:', erroe_value)
                        parameters = {
                            "TABLE": table['TABLE'],
                            "SEPARATOR": table['SEPARATOR'],
                            "HAS_HEADER": table['HAS_HEADER'],
                            "ERROR": erroe_value,
                            "ERROR_MEASURE": error_measure,
                        }
                        test_memory_output = run_tests(measure_memory, execfullPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Memory:', test_memory_output)
                        output_memory += format_for_graph(erroe_value, test_memory_output)
                    
                    output_memory += '\n'
                    fp.write(output_memory)
                    fp.flush()
                    output_memory = ""
    
