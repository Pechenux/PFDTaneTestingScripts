# from generation.generate_pfdtane_data import generate_pfdtane_data
from tools.run_datasets_with_time_limit import run_datasets

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

run_datasets('good_datasets')

# generate_pfdtane_data()
