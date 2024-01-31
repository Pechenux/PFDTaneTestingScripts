# Importing libraries 
import matplotlib.pyplot as plt
import pandas as pd

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])

def add_line(error, values, h, marker, color, label):
    band_color = color_variant(color, 100)
    plt.plot(error, values, color=color, label=label, linewidth=0.1, marker=marker)
    plt.fill_between(error, values-h, values+h, alpha=0.5, facecolor=band_color)  # , edgecolor=color

def add_csv(csv_path, color, label, marker=' '):
    data = pd.read_csv(csv_path, sep=' ')
    add_line(data["error"].to_numpy(), data["value"].to_numpy(), data["h"].to_numpy(), marker, color, label)


plt.rcParams['figure.figsize'] = [4, 5]

datasets = ['LegacyPayors', 'EpicVitals']

perfomanse_measures = {
    'time': 'Time (s)',
    # 'memory': 'Memory (kb)'
}

for perfomanse_measure in perfomanse_measures.keys():
    for dataset in datasets:
        plt.title(f"{dataset}.csv")
        plt.xlabel("Error")
        plt.ylabel(perfomanse_measures[perfomanse_measure])
        add_csv(f'out/pfdtane_{perfomanse_measure}_per_value_{dataset}.csv', '#FF0000', 'Per Value')
        add_csv(f'out/pfdtane_{perfomanse_measure}_per_tuple_{dataset}.csv', '#0000FF', 'Per Tuple')
        plt.legend()
        plt.savefig(f"out/{perfomanse_measure}_{dataset}.pdf", format="pdf", bbox_inches="tight")
        plt.cla()
