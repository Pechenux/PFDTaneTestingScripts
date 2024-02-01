import os


# TODO: create function to find max runs between error ranges
# TODO: create function that combines data on parameters on previous step
# TODO: save report on combined data

for filename in os.listdir('out'):
    if os.path.isdir(f"out/{filename}"):
        test_runs_count = os.listdir(f"out/{filename}")
        for algo in ['pfdtane', 'tane']:
            for perf in ['time', 'memory']:
                for measure in ['per_value', 'per_tuple']:
                    for error_range in [1, 2]:
                        for test_run_number in range(test_runs_count):
                            if (not os.path.exists(f"out/{filename}/{test_run_number}/{algo}_{perf}_{error_range}_{measure}")):
                                print(f"Run {test_run_number} of {filename} on {perf} by algorith {algo} with parameters {error_range} {measure} does not exist. ")