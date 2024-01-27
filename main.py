from experiment1.experiment1 import run_experiment_1
from experiment2.experiment2 import run_experiment_2

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

# run_experiment_1()
run_experiment_2()
