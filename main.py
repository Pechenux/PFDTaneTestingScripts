from generation.generate_pfdtane_data import generate_pfdtane_data
from generation.generate_tane_data import generate_tane_data

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

generate_tane_data()
generate_pfdtane_data()
