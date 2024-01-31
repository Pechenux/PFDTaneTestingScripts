import os
import json
import csv
import time

from dataclasses import dataclass
from multiprocessing import Process, Queue

from tools.measure_time import measure_time
from tools.executePFDTane import execPFDTane

@dataclass
class Table:
    TABLE: str
    SEPARATOR: str
    HAS_HEADER: str
    run_time: float

def run_dataset(parameters, ret):
    start_time = time.time()
    execPFDTane(parameters)
    ret.put(time.time() - start_time)

LOW_TIME = 1
HIGH_TIME = 20

def run_datasets(folder_path):
    datasets = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            has_header = True
            delimiter = ','
            with open(f"{folder_path}/{filename}", 'r') as csvfile:
                sniffer = csv.Sniffer()
                has_header = sniffer.has_header(csvfile.read(10000))
            with open(f"{folder_path}/{filename}", 'r') as csvfile:
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(csvfile.read(10000)).delimiter

            print(f"{folder_path}/{filename}", delimiter, has_header)
            
            parameters = {
                "TABLE": f"{folder_path}/{filename}",
                "SEPARATOR": delimiter,
                "HAS_HEADER": has_header,
                "ERROR": 0,
                "ERROR_MEASURE": 'per_tuple',
            }

            run_time = 0
            q = Queue()
            p = Process(target=run_dataset, args=(parameters, q))
            p.start()
            p.join(HIGH_TIME)
            if p.is_alive():
                p.terminate()
                print(f"{folder_path}/{filename} took more than {HIGH_TIME} second(s) to run")
            else:
                run_time = q.get()

                if (run_time >= LOW_TIME):
                    datasets.append(Table(f"{folder_path}/{filename}", delimiter, has_header, run_time))
                else:
                    print(f"{folder_path}/{filename} took less than {LOW_TIME} second(s) to run ({run_time})")
    
    datasets.sort(key=lambda table: table.run_time)
    datasets = list(map(lambda table: {
        "TABLE": table.TABLE,
        "SEPARATOR": table.SEPARATOR,
        "HAS_HEADER": table.HAS_HEADER,
        "run_time": table.run_time
    }, datasets))

    with open("out/datasets_times.json", "w") as outfile: 
        json.dump({"tables": datasets}, outfile, indent = 4)
    
    