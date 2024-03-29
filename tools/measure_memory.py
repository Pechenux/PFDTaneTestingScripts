from multiprocessing import Process
import psutil
import time

def measure_memory(exec_function, _, parameters):  # second parameter is unused, memory measure should always use full exec function
    p = Process(target=exec_function, args=(parameters, ))
    p.start()
    ps = psutil.Process(p.pid)
    max_usage = 0
    while (p.is_alive()):
        curr_usage = ps.memory_info().rss
        if (curr_usage > max_usage):
            max_usage = curr_usage
        time.sleep(0.001)
    
    return max_usage, 0  # second value is always zero for compatibility with time measure function
