
from texttable import Texttable
import latextable
import pandas as pd

datasets = ['BKB_WaterQualityData_2020084', 'EpicVitals', 'jena_climate_2009_2016', 'measures_v2', 'nuclear_explosions', 'parking_citations', 'SEA', 'games']

perfomanse_measures = {
    'time': 'Time (s)',
    'memory': 'Memory (bytes)'
}

def get_dataframe(csv_path):
    data = pd.read_csv(csv_path, sep=' ')
    row_with_zero = data['error'] == 0
    return data[~row_with_zero]

def parse_csv(csv_path):
    data = pd.read_csv(csv_path, sep=' ')
    row_with_zero = data['error'] == 0
    data = data[~row_with_zero]
    return data["error"].to_numpy(), data["value"].to_numpy(), data["h"].to_numpy()

# experiment 3a 3b table
for perfomanse_measure in perfomanse_measures.keys():
    for error_measure in ['per_value', 'per_tuple']:
        table_latex = Texttable()
        table_latex.set_cols_align(['c'] * 3)
        rows = [['Datasets',
                 f'PFDTane {perfomanse_measures[perfomanse_measure]}',
                 f'Tane {perfomanse_measures[perfomanse_measure]}']
                ]

        for dataset in datasets:
            value_pfdtane = parse_csv(f'out/pfdtane_{perfomanse_measure}_{error_measure}_{dataset}.csv')
            value_tane = parse_csv(f'out/tane_{perfomanse_measure}_{dataset}.csv')
            rows.append([dataset, f"{value_pfdtane[0]} +- {value_pfdtane[1]}", f"{value_tane[0]} +- {value_tane[1]}"])
        
        table_latex.add_rows(rows)
        latex_output = latextable.draw_latex(table_latex, caption=f"{error_measure}".replace('_', '\\_'), label=f"table:{perfomanse_measure}_{error_measure}", position='ht')

        with open(f'out/experiments_1_{perfomanse_measure}_{error_measure}.out', 'w') as fp:
            fp.write(latex_output)

