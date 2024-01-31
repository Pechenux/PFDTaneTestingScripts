from generation.generate_pfdtane_data import generate_pfdtane_data

import os
if not os.path.exists('./out'):
    os.makedirs('./out')

generate_pfdtane_data()
