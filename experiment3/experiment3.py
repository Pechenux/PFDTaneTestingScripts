
from texttable import Texttable
import latextable
import pandas as pd
from functools import reduce

datasets = ['BKB_WaterQualityData_2020084', 'EpicVitals', 'jena_climate_2009_2016', 'measures_v2', 'nuclear_explosions', 'parking_citations', 'SEA', 'games']

perfomanse_measures = {
    'time': 'Time (s)',
    'memory': 'Memory (bytes)'
}

def get_dataframe(csv_path):
    data = pd.read_csv(csv_path, sep=' ')
    row_with_zero = data['error'] == 0
    return data[~row_with_zero][['error', 'value']]

def get_relation_between_dataframes(dataset, dataframe_pfdtane, dataframe_tane):
    dataframe_pfdtane.drop(columns=['h'])
    dataframe_tane.drop(columns=['h'])

    dataframe_pfdtane.rename(columns={"value": "pfdvalue"})
    dataframe_tane.rename(columns={"value": "tanevalue"})

    pfdtane_values_by_tane = dataframe_pfdtane[dataframe_pfdtane['error'].isin(dataframe_tane['error'].tolist())]
    merged_dataframe = pd.merge(pfdtane_values_by_tane, dataframe_tane, on=['error'])
    merged_dataframe["relation"] = merged_dataframe["pfdvalue"] / merged_dataframe["tanevalue"]

    return merged_dataframe[['error', f'{dataset}']]

def merge_dataframes(dataframes):
    return reduce(lambda  left, right: pd.merge(left,right,on=['error']), dataframes)


# experiment 3a 3b table
for perfomanse_measure in perfomanse_measures.keys():
    for error_measure in ['per_value', 'per_tuple']:
        # rows = [['Datasets',
        #          f'PFDTane {perfomanse_measures[perfomanse_measure]}',
        #          f'Tane {perfomanse_measures[perfomanse_measure]}']
        #         ]

        relation_dataframes = []

        for dataset in datasets:
            dataframe_pfdtane = get_dataframe(f'out/pfdtane_{perfomanse_measure}_{error_measure}_{dataset}.csv')
            dataframe_tane = get_dataframe(f'out/tane_{perfomanse_measure}_{dataset}.csv')
            relation_dataframes.append(get_relation_between_dataframes(dataset, dataframe_pfdtane, dataframe_tane))
        
        merged_dataframes = merge_dataframes(relation_dataframes)
        error_values = merged_dataframes.iloc[[0]].to_numpy()
        relations = merged_dataframes.iloc[1:, :]

        table_latex = Texttable()
        table_latex.set_cols_align(["c"] * (1 + len(error_values)))

        rows = [['Datasets', *error_values]]

        for i, row in relations.iterrows():
            rows.append([i, *row])
        
        table_latex.add_rows(rows)

        multicolumn_header = [("", 1), ("error threshold", len(error_values))]
        latex_output = latextable.draw_latex(table_latex, caption=f"Memory {error_measure}".replace('_', '\\_'), label=f"table:memory_{error_measure}", position='ht', multicolumn_header=multicolumn_header)

        with open(f'out/experiments_3_{perfomanse_measure}_{error_measure}.out', 'w') as fp:
            fp.write(latex_output)
        
