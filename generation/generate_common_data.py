import csv
import os
import sys

from pathlib import Path

from tools.run_tests import run_tests

TEST_COUNT = 10

def generate_common_data(prefix, experiments, error_values, measure_function, exec_function, load_function=None):
    print('Measuring', prefix)
    for test_run in range(TEST_COUNT):
        print('Run number', test_run)
        for table in experiments["tables"]:
            print('Running:', table['TABLE'])
            for error_measure in ['per_value', 'per_tuple']:
                print('Evaluating:', error_measure)
                filename = f"out/{Path(table['TABLE']).stem}/{test_run}/{prefix}_{error_measure}.csv"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                try:
                    with open(filename, 'w', newline='') as csvfile:
                        outcsv = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
                        outcsv.writerow(['error', 'value_exec', 'value_load'])

                        for erroe_value in error_values:
                            print('Error:', erroe_value)
                            parameters = {
                                "TABLE": table['TABLE'],
                                "SEPARATOR": table['SEPARATOR'],
                                "HAS_HEADER": table['HAS_HEADER'],
                                "ERROR": erroe_value,
                                "ERROR_MEASURE": error_measure,
                            }
                            testout = measure_function(exec_function, load_function, parameters)
                            outcsv.writerow([erroe_value, testout[0], testout[1]])
                except:
                    print(f"Report {filename} did not complete, deleting incomplete data")
                    os.remove(filename)
                    sys.exit()