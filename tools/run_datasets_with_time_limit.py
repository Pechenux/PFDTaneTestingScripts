import os
import json
import csv
import signal
from dataclasses import dataclass

from contextlib import contextmanager


from tools.measure_time import measure_time
from tools.executePFDTane import execPFDTane

@dataclass
class Table:
    TABLE: str
    SEPARATOR: str
    HAS_HEADER: str
    run_time: float


class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def run_datasets(folder_path):
    datasets = []

    for filename in os.listdir(folder_path):
        has_header = True
        delimiter = ','
        with open(f"{folder_path}/{filename}", 'r') as csvfile:
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(csvfile.read(2048))
        with open(f"{folder_path}/{filename}", 'r') as csvfile:
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(csvfile.read(2048)).delimiter

        print(f"{folder_path}/{filename}", delimiter, has_header)
        
        parameters = {
            "TABLE": f"{folder_path}/{filename}",
            "SEPARATOR": delimiter,
            "HAS_HEADER": has_header,
            "ERROR": 0,
            "ERROR_MEASURE": 'per_tuple',
        }

        try:
            run_time = 0
            with time_limit(20):
                run_time = measure_time(execPFDTane, parameters)
            if (run_time >= 2):
                datasets.append(Table(f"{folder_path}/{filename}", delimiter, has_header, run_time))
            else:
                print(f"{folder_path}/{filename} took less than 2 seconds to run")
        except TimeoutException as e:
            print(f"{folder_path}/{filename} took more than 20 seconds to run")
    
    datasets.sort(key=lambda table: table.run_time)
    datasets = list(map(lambda table: {
        "TABLE": table.TABLE,
        "SEPARATOR": table.SEPARATOR,
        "HAS_HEADER": table.HAS_HEADER,
        "run_time": table.run_time
    }, datasets))

    with open("out/datasets_times.json", "w") as outfile: 
        json.dump({"tables": datasets}, outfile, indent = 4)
    
    