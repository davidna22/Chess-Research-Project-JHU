import numpy as np
import scipy.stats as stats

from IPython.core.display import display, HTML

def display_dict(m, precision = 3):
    table = "<table>"
    for item in m.items():
        table += ("<tr><th>{0}</th><td>{1:." + str(precision) + "f}</td></tr>").format(*item)
    table += "</table>"
    return display(HTML(table))

def calculate_tukey_five(data):
    values = list(np.concatenate([[np.min(data)], stats.mstats.mquantiles( data, [0.25, 0.5, 0.75]),[np.max(data)]]))
    labels = ["Min", "Q1", "Median", "Q3", "Max"]
    data = {"Stats": labels, "Values": values}
    return data

def calculate_tukey_dispersion(five):
    _five = {k: v for k, v in zip(five["Stats"], five["Values"])}
    labels = ["Range", "IQR", "QCV"]
    values = [
        _five["Max"] - _five["Min"],
        _five["Q3"] - _five["Q1"],
        (_five["Q3"] - _five["Q1"]) / _five["Median"]
    ]
    return {"Stats": labels, "Values": values}

def tukey(data):
    five = calculate_tukey_five(data)
    dispersion = calculate_tukey_dispersion(five)
    return {"Stats": five["Stats"] + dispersion["Stats"], "Values": five["Values"] + dispersion["Values"]}

def restyle_boxplot(patch):
    ## change color and linewidth of the whiskers
    for whisker in patch['whiskers']:
        whisker.set(color='#000000', linewidth=1)

    ## change color and linewidth of the caps
    for cap in patch['caps']:
        cap.set(color='#000000', linewidth=1)

    ## change color and linewidth of the medians
    for median in patch['medians']:
        median.set(color='#000000', linewidth=2)

    ## change the style of fliers and their fill
    for flier in patch['fliers']:
        flier.set(marker='o', color='#000000', alpha=0.2)

    for box in patch["boxes"]:
        box.set( facecolor='#FFFFFF', alpha=0.5)
