import cProfile, pstats

def measure_time(exec_function, load_fuction, parameters):
    if load_fuction != None:
        # load
        profiler = cProfile.Profile()

        profiler.enable()
        algo = load_fuction(parameters)
        profiler.disable()

        load_time = pstats.Stats(profiler).sort_stats('tottime').total_tt
        profiler.__exit__()

        # exec
        profiler = cProfile.Profile()

        profiler.enable()
        exec_function(algo, parameters)
        profiler.disable()

        exec_time = pstats.Stats(profiler).sort_stats('tottime').total_tt

        return exec_time, load_time
    else:
        profiler = cProfile.Profile()

        profiler.enable()
        exec_function(parameters)
        profiler.disable()

        stats = pstats.Stats(profiler).sort_stats('tottime')
        return stats.total_tt, 0
