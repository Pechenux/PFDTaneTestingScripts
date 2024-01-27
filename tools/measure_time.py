import cProfile, pstats

def measure_time(exec_function, parameters):
    profiler = cProfile.Profile()

    profiler.enable()
    exec_function(parameters)
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats('tottime')
    return stats.total_tt
