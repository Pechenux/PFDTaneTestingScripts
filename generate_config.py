from tools.run_datasets_with_time_limit import run_datasets

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

run_datasets('good_datasets')