import numpy as np
import json
import os

from texttable import Texttable
import latextable

from tools.measure_time import measure_time
from tools.measure_memory import measure_memory
from tools.executePFDTane import execPFDTane
from tools.executeTane import execTane
from tools.run_tests import run_tests

error_values = np.arange(0, 1, 0.025)
# error_values = np.arange(0, 1, 0.3) # debug
error_values = np.round(error_values, 3) # round
error_values = np.delete(error_values, [0]) # remove value 0\
TEST_COUNT = 20
CONFIDENCE = 0.95

# experiments 3a and 3b
def run_experiment_2():
    output_time = ""
    output_memory = ""

    with open('experiment2/experiments_2.json') as fp:
        experiments = json.load(fp)

        # time
        for error_measure in ['per_value', 'per_tuple']:
            print('Evaluating:', error_measure)

            table_latex = Texttable()
            table_latex.set_cols_align(["c"] * (1 + len(error_values)))

            output_time += f"% {error_measure}\n"
            rows = [['Datasets', *list(map(str, error_values))]]

            for table in experiments["tables"]:
                print('Running:', table['TABLE'])

                row = [os.path.basename(table['TABLE'])]

                for erroe_value in error_values:
                    print('Error:', erroe_value)

                    parameters = {
                        "TABLE": table['TABLE'],
                        "SEPARATOR": table['SEPARATOR'],
                        "HAS_HEADER": table['HAS_HEADER'],
                        "ERROR": erroe_value,
                        "ERROR_MEASURE": error_measure,
                    }
                    pfdtane_time_output = run_tests(measure_time, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                    tane_time_output = run_tests(measure_time, execTane, parameters, TEST_COUNT, CONFIDENCE)
                    print('  Time:', 'pfdtane', pfdtane_time_output, 'tane', tane_time_output, 'relation', pfdtane_time_output[0] / tane_time_output[0])
                    row.append(pfdtane_time_output[0] / tane_time_output[0])
                
                rows.append(row)
            
            table_latex.add_rows(rows)
            multicolumn_header = [("", 1), ("error threshold", len(error_values))]
            output_time += latextable.draw_latex(table_latex, caption=f"Time {error_measure}".replace('_', '\\_'), label=f"table:time_{error_measure}", position='ht', multicolumn_header=multicolumn_header)
            output_time += '\n'

    
        with open('out/experiments_2_time.out', 'w') as fp:
            fp.write(output_time)
        
        # memory
        for error_measure in ['per_value', 'per_tuple']:
            print('Evaluating:', error_measure)

            table_latex = Texttable()
            table_latex.set_cols_align(["c"] * (1 + len(error_values)))

            output_memory += f"% {error_measure}\n"
            rows = [['Datasets', *list(map(str, error_values))]]

            for table in experiments["tables"]:
                print('Running:', table['TABLE'])

                row = [os.path.basename(table['TABLE'])]

                for erroe_value in error_values:
                    print('Error:', erroe_value)
                    parameters = {
                        "TABLE": table['TABLE'],
                        "SEPARATOR": table['SEPARATOR'],
                        "HAS_HEADER": table['HAS_HEADER'],
                        "ERROR": erroe_value,
                        "ERROR_MEASURE": error_measure,
                    }
                    pfdtane_memory_output = run_tests(measure_memory, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                    tane_memory_output = run_tests(measure_memory, execTane, parameters, TEST_COUNT, CONFIDENCE)
                    print('  Memory:', 'pfdtane', pfdtane_memory_output, 'tane', tane_memory_output, 'relation', pfdtane_memory_output[0] / tane_memory_output[0])
                    row.append(pfdtane_memory_output[0] / tane_memory_output[0])
                
                rows.append(row)
            
            table_latex.add_rows(rows)

            multicolumn_header = [("", 1), ("error threshold", len(error_values))]
            output_memory += latextable.draw_latex(table_latex, caption=f"Memory {error_measure}".replace('_', '\\_'), label=f"table:memory_{error_measure}", position='ht', multicolumn_header=multicolumn_header)
            output_memory += '\n'
        
        with open('out/experiments_2_memory.out', 'w') as fp:
            fp.write(output_memory)
    
