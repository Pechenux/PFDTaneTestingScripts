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

TEST_COUNT = 20
CONFIDENCE = 0.95

# experiments 1
def run_experiment_3():
    output_time = ""
    output_memory = ""

    with open('experiment3/experiments_3.json') as fp:
        experiments = json.load(fp)

        # time
        for error_measure in ['per_value', 'per_tuple']:
            print('Evaluating:', error_measure)
            table_latex = Texttable()
            table_latex.set_cols_align(["c"] * 3)

            output_time += f"% {error_measure}\n"
            rows = [['Datasets', 'PFDTane', 'Tane']]

            for table in experiments["tables"]:
                print('Running:', table['TABLE'])

                row = [os.path.basename(table['TABLE'])]
                
                parameters = {
                    "TABLE": table['TABLE'],
                    "SEPARATOR": table['SEPARATOR'],
                    "HAS_HEADER": table['HAS_HEADER'],
                    "ERROR": 0,
                    "ERROR_MEASURE": error_measure,
                }
                pfdtane_time_output = run_tests(measure_time, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                tane_time_output = run_tests(measure_time, execTane, parameters, TEST_COUNT, CONFIDENCE)
                print('  Time:', 'pfdtane', pfdtane_time_output, 'tane', tane_time_output)
                row += [f"{pfdtane_time_output[0]} +- {pfdtane_time_output[1]}", f"{tane_time_output[0]} +- {tane_time_output[1]}"]
                
                rows.append(row)
            
            table_latex.add_rows(rows)
            output_time += latextable.draw_latex(table_latex, caption=f"Time {error_measure}".replace('_', '\\_'), label=f"table:time_{error_measure}", position='ht')
            output_time += '\n'

    
        with open('out/experiments_3_time.out', 'w') as fp:
            fp.write(output_time)
        
        # memory
        for error_measure in ['per_value', 'per_tuple']:
            print('Evaluating:', error_measure)
            table_latex = Texttable()
            table_latex.set_cols_align(["c"] * 3)

            output_memory += f"% {error_measure}\n"
            rows = [['Datasets', 'PFDTane', 'Tane']]

            for table in experiments["tables"]:
                print('Running:', table['TABLE'])

                row = [os.path.basename(table['TABLE'])]
                
                parameters = {
                    "TABLE": table['TABLE'],
                    "SEPARATOR": table['SEPARATOR'],
                    "HAS_HEADER": table['HAS_HEADER'],
                    "ERROR": 0,
                    "ERROR_MEASURE": error_measure,
                }
                pfdtane_memory_output = run_tests(measure_memory, execPFDTane, parameters, TEST_COUNT, CONFIDENCE)
                tane_memory_output = run_tests(measure_memory, execTane, parameters, TEST_COUNT, CONFIDENCE)
                print('  Memory:', 'pfdtane', pfdtane_memory_output, 'tane', tane_memory_output, 'relation', pfdtane_memory_output[0] / tane_memory_output[0])
                row += [f"{pfdtane_memory_output[0]} +- {pfdtane_memory_output[1]}", f"{tane_memory_output[0]} +- {tane_memory_output[1]}"]
                
                rows.append(row)
            
            table_latex.add_rows(rows)
            output_time += latextable.draw_latex(table_latex, caption=f"Memory {error_measure}".replace('_', '\\_'), label=f"table:memory_{error_measure}", position='ht')
            output_time += '\n'
        
        with open('out/experiments_3_memory.out', 'w') as fp:
            fp.write(output_memory)
    
