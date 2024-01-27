import numpy as np
import json

from measure_time import measure_time
from measure_memory import measure_memory
from executePFDTane import execPFDTane
from run_tests import run_tests
from format_for_graph import format_for_graph

error_values = np.arange(0, 1, 0.025)
# error_values = np.arange(0, 1, 0.3) # debug
TEST_COUNT = 50
CONFIDENCE = 0.95

# experiments 2a and 2b

def run_experiment_1():
    output_time = ""
    output_memory = ""

    with open('experiments_1.json') as fp:
        experiments = json.load(fp)

        # time
        for table in experiments["tables"]:
            print('Running:', table['TABLE'])
            experiments_list = table['experiments']
            for i in range(len(experiments_list)):
                print('Experiment with parameters:', experiments_list[i])
                for error_measure in ['per_value', 'per_tuple']:
                    print('Evaluating:', error_measure)

                    output_time += f" % {table['TABLE']} experiment {i + 1} {error_measure}\n"

                    for erroe_value in error_values:
                        print('Error:', erroe_value)
                        parameters = {
                            "TABLE": table['TABLE'],
                            "SEPARATOR": table['SEPARATOR'],
                            "HAS_HEADER": table['HAS_HEADER'],
                            "ISNULLEQNULL": experiments_list[i]["ISNULLEQNULL"],
                            "ERROR": erroe_value,
                            "ERROR_MEASURE": error_measure,
                            "MAXLHS": experiments_list[i]["MAXLHS"]
                        }
                        test_time_output = run_tests(measure_time, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Time:', test_time_output)
                        output_time += format_for_graph(erroe_value, test_time_output)
                    
                    output_time += '\n'
        
        with open('experiments_1_time.out', 'w') as fp:
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
                            "ISNULLEQNULL": experiments_list[i]["ISNULLEQNULL"],
                            "ERROR": erroe_value,
                            "ERROR_MEASURE": error_measure,
                            "MAXLHS": experiments_list[i]["MAXLHS"]
                        }
                        test_memory_output = run_tests(measure_memory, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                        print('  Memory:', test_memory_output)
                        output_memory += format_for_graph(erroe_value, test_memory_output)
                    
                    output_memory += '\n'
        
        with open('experiments_1_memory.out', 'w') as fp:
            fp.write(output_memory)
    
