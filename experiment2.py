import numpy as np
import json
from executeTane import execTane

from measure_time import measure_time
from measure_memory import measure_memory
from executePFDTane import execPFDTane
from run_tests import run_tests
from format_for_graph import format_for_graph

# error_values = np.arange(0, 1, 0.025)
error_values = np.arange(0, 1, 0.3) # debug
TEST_COUNT = 50
CONFIDENCE = 0.95

# experiments 1, 3a and 3b

def run_experiment_2():
    output_time = ""
    output_memory = ""

    with open('experiments_2.json') as fp:
        experiments = json.load(fp)

        # time
        for table in experiments["tables"]:
            print('Running:', table['TABLE'])
            experiments_list = table['experiments']
            for i in range(len(experiments_list)):
                print('Experiment with parameters:', experiments_list[i])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)

                    output_time += f"% {table['TABLE']} experiment {i + 1} {error_measure}\n"

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
                        pfdtane_time_output = run_tests(measure_time, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        tane_time_output = run_tests(measure_time, execTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Time:', 'pfdtane', pfdtane_time_output, 'tane', tane_time_output)
                        # output_time += format_for_graph(erroe_value, test_time_output)
                    
                    output_time += '\n'
    
        with open('experiments_2_time.out', 'w') as fp:
            fp.write(output_time)
        
        # memory
        for table in experiments["tables"]:
            print('Running:', table['TABLE'])
            experiments_list = table['experiments']
            for i in range(len(experiments_list)):
                print('Experiment with parameters:', experiments_list[i])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)

                    output_memory += f"% {table['TABLE']} experiment {i + 1} {error_measure}\n"

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
                        pfdtane_memory_output = run_tests(measure_memory, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        tane_memory_output = run_tests(measure_memory, execTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Memory:', 'pfdtane', pfdtane_memory_output, 'tane', tane_memory_output)
                        # output_memory += format_for_graph(erroe_value, test_memory_output)
                    
                    output_memory += '\n'
        
        with open('experiments_2_memory.out', 'w') as fp:
            fp.write(output_memory)
    
