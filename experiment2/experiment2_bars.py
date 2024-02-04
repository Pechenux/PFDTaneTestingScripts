# Importing libraries 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as tkr

colors = [
    "#000000", # black
    "#FF0000", # red
    "#0000FF", # blue
    "#422400", # brown
    "#00B7EB", # cyan
    "#CC5500", # burned orange
    "#008000", # green
    "#E952DE", # purple
    "#DA9100", # Harvest Gold
    "#9ACD32", # Yellow-green
]

def sizeof_fmt(x, pos):
    if x<0:
        return ""
    for x_unit in ['bytes', 'kB', 'MB', 'GB', 'TB']:
        if x < 1024.0:
            return "%3.1f %s" % (x, x_unit)
        x /= 1024.0

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])

def add_line(error, values, h, marker, color, label):
    plt.errorbar(error, values, yerr=h, color=color, label=label, linewidth=0.1, marker=marker, markersize=2, capsize=2)
    # plt.plot(error, values, color=color, label=label, linewidth=0.1, marker=marker)

def add_csv(csv_path, color, label, marker=' '):
    data = pd.read_csv(csv_path, sep=' ')
    add_line(data["error"].to_numpy(), data["value"].to_numpy(), data["h"].to_numpy(), marker, color, label)

def add_dataset(filename, perfomanse_measure, color):
    add_csv(f'out/pfdtane_{perfomanse_measure}_per_value_{filename}.csv', color, f'{filename} Per Value', marker='.')
    # add_csv(f'out/pfdtane_{perfomanse_measure}_per_tuple_{filename}.csv', color, f'{filename} Per Tuple', marker='^')
    add_csv(f'out/pfdtane_{perfomanse_measure}_per_tuple_{filename}.csv', color_variant(color, 75), f'{filename} Per Tuple', marker='.')


plt.rcParams['figure.figsize'] = [4, 8] # [4, 5]

groups = [['BKB_WaterQualityData_2020084', 'games', 'nuclear_explosions', 'SEA'], ['EpicVitals', 'measures_v2', 'jena_climate_2009_2016', 'parking_citations']]

perfomanse_measures = {
    'time': 'Time (s)',
    'memory': 'Memory'  # remove 1e8 from top (make in megabytes)
}

error_measures = {
    'per_value': 'Per Value',
    'per_tuple': 'Per Tuple'
}

counter = 0

# experiment 2a 2b bars plot

# for perfomanse_measure in perfomanse_measures.keys():
#     for error_measure in ['per_value', 'per_tuple']:
#         for group_number in range(len(groups)):
#             # plt.title(f"Full comparison")
#             plt.xlabel("Error")
#             plt.ylabel(perfomanse_measures[perfomanse_measure])
#             plt.xlim([0, 1])

#             for dataset in groups[group_number]:
#                 add_csv(f'out/pfdtane_{perfomanse_measure}_{error_measure}_{dataset}.csv', colors[counter], f'{dataset}')
#                 counter += 1

#             plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), fancybox=True, shadow=True, ncol=1)
#             plt.savefig(f"out/{perfomanse_measure}_{error_measure}_{group_number}.pdf", format="pdf", bbox_inches="tight")
#             plt.cla()
#         counter = 0
#     counter = 0

for perfomanse_measure in perfomanse_measures.keys():
    for group_number in range(len(groups)):
        plt.xlabel("Error")
        plt.ylabel(perfomanse_measures[perfomanse_measure])
        
        if (perfomanse_measure == 'memory'):
            ax = plt.subplots()[1]
            ax.yaxis.set_label_text(label=perfomanse_measures[perfomanse_measure])
            ax.yaxis.set_major_formatter(tkr.FuncFormatter(sizeof_fmt))

        for dataset in groups[group_number]:
            add_dataset(dataset, perfomanse_measure, colors[counter])
            counter += 1

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), fancybox=True, shadow=True, ncol=1)
        plt.savefig(f"out/paper/exp2/bar/{perfomanse_measure}_{group_number}.pdf", format="pdf", bbox_inches="tight")
        plt.cla()
    counter = 0