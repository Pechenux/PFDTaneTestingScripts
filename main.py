from experiment1.experiment1 import run_experiment_1
from experiment2.experiment2 import run_experiment_2
from experiment3.experiment3 import run_experiment_3

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

run_experiment_1()
# run_experiment_2()
# run_experiment_3()
