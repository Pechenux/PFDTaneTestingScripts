import csv

from pathlib import Path

from tools.run_tests import run_tests

TEST_COUNT = 10
CONFIDENCE = 0.95

def generate_common_data(prefix, experiments, error_values, measure_function, exec_function):
    print('Measuring', prefix)
    for table in experiments["tables"]:
        print('Running:', table['TABLE'])
        for error_measure in ['per_value', 'per_tuple']:
            print('Evaluating:', error_measure)
            with open(f"out/{prefix}_{error_measure}_{Path(table['TABLE']).stem}.csv", 'w', newline='') as csvfile:
                outcsv = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
                outcsv.writerow(['error', 'value', 'h'])

                for erroe_value in error_values:
                    print('Error:', erroe_value)
                    parameters = {
                        "TABLE": table['TABLE'],
                        "SEPARATOR": table['SEPARATOR'],
                        "HAS_HEADER": table['HAS_HEADER'],
                        "ERROR": erroe_value,
                        "ERROR_MEASURE": error_measure,
                    }
                    testout = run_tests(measure_function, exec_function, parameters, TEST_COUNT, CONFIDENCE)
                    outcsv.writerow([erroe_value, testout[0], testout[1]])