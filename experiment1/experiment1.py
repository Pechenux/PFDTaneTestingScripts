
from texttable import Texttable
import latextable
import pandas as pd
import numpy as np

datasets = ['BKB_WaterQualityData_2020084', 'EpicVitals', 'jena_climate_2009_2016', 'measures_v2', 'nuclear_explosions', 'parking_citations', 'SEA', 'games']

perfomanse_measures = {
    'time': 'Time (s)',
    'memory': 'Memory (MB)'
}

def parse_csv(csv_path):
    data = pd.read_csv(csv_path, sep=' ')
    return data.loc[data['error'] == 0, ['value', 'h']].values.flatten().tolist()

BYTES_IN_MEGABYTE = 1024*1024

# experiment 1 table
for perfomanse_measure in perfomanse_measures.keys():
    table_latex = Texttable()
    table_latex.set_cols_align(['c'] * 4)
    rows = [['',
             f'PFDTane per\_value',
             f'PFDTane per\_tuple',
             f'Tane']]

    for dataset in datasets:
        value_pfdtane_per_value = parse_csv(f'out/pfdtane_{perfomanse_measure}_per_value_{dataset}.csv')
        value_pfdtane_per_tuple = parse_csv(f'out/pfdtane_{perfomanse_measure}_per_tuple_{dataset}.csv')
        value_tane = parse_csv(f'out/tane_{perfomanse_measure}_{dataset}.csv')
        conversion_ratio = 1 if perfomanse_measure == 'time' else BYTES_IN_MEGABYTE
        rows.append([dataset.replace('_', '\\_'),
                     f"{np.round(value_pfdtane_per_value[0] / conversion_ratio, 3)} \\pm {np.round(value_pfdtane_per_value[1] / conversion_ratio, 3)}",
                     f"{np.round(value_pfdtane_per_tuple[0] / conversion_ratio, 3)} \\pm {np.round(value_pfdtane_per_tuple[1] / conversion_ratio, 3)}",
                     f"{np.round(value_tane[0] / conversion_ratio, 3)} \\pm {np.round(value_tane[1] / conversion_ratio, 3)}"])
    
    table_latex.add_rows(rows)
    multicolumn_header = [("Datasets", 1), (perfomanse_measures[perfomanse_measure], 3)]
    latex_output = latextable.draw_latex(table_latex, caption=f"{perfomanse_measures[perfomanse_measure]}".replace('_', '\\_'), label=f"table:{perfomanse_measure}", position='ht', multicolumn_header=multicolumn_header)

    with open(f'out/experiments_1_{perfomanse_measure}.out', 'w') as fp:
        fp.write(latex_output)

