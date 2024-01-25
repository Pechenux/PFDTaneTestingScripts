from confidence_interval import mean_confidence_interval

def run_tests(measure_function, exec_function, parameters, count=50, confidence=0.95):
    measures_time = []
    for _ in range(count):
        measures_time.append(measure_function(exec_function, parameters))

    return mean_confidence_interval(measures_time, confidence)
