import statistics
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from functools import reduce
import math


"""
This is the file for writing new types of graph.

The functions need to accept the arguments:
   x_data, y_data, show_best_fit, show_rank, colours, label
   
The functions should plot the data using plt.plot.

The functions must label the graphs with the supplied label.

The functions must show pearson's rand if it is selected.

The functions must use the supplied colours but can use a gradient between them if appropriate.

The functions must return the labels in a list so they can be added to the key.

After writing a function that fits these requirements add it to plotting_dict in the form:
   name: function
"""


def scatter_plot(x, y, show_best_fit, rank, colours, label):
    x = reduce(lambda a, b: a + b, x)
    y = reduce(lambda a, b: a + b, y)
    x2 = np.array(x)
    y2 = np.array(y)

    handles = []

    if rank:
        r, p = scipy.stats.pearsonr(x2, y2)
        rank_text = f"\nr = {r:.4}, p = {p:.4}"
    else:
        rank_text = ""

    if len(x) > 300:
        line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text, alpha=.1)
    elif len(x2) > 50:
        line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text, alpha=.7)
    else:
        line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text)
    handles.append(line)

    if show_best_fit:
        min_val = None
        max_val = None
        for x_val in x2:
            if min_val is None:
                min_val = x_val
            else:
                min_val = min(min_val, x_val)
            if max_val is None:
                max_val = x_val
            else:
                max_val = max(max_val, x_val)

        # noinspection PyTupleAssignmentBalance
        m, c = np.polyfit(x2, y2, 1)

        points = np.array([min_val, max_val])
        best_fit, = plt.plot(points, m * points + c, label=f"y = {m:.5}x + {c:.5}", color=colours[1])
        handles.append(best_fit)

    return handles


def line_plot(x, y, show_best_fit, rank, colours, label):
    handles = []
    x2 = np.array(reduce(lambda a, b: a + b, x))
    y2 = np.array(reduce(lambda a, b: a + b, y))

    if rank:
        r, p = scipy.stats.pearsonr(x2, y2)
        rank_text = f"\nr = {r:.4}, p = {p:.4}"
    else:
        rank_text = ""

    for x_sec, y_sec in zip(x, y):
        line, = plt.plot(x_sec, y_sec, color=colours[0], label=label + rank_text)
    handles.append(line)

    if show_best_fit:
        min_val = None
        max_val = None
        for x_val in x2:
            if min_val is None:
                min_val = x_val
            else:
                min_val = min(min_val, x_val)
            if max_val is None:
                max_val = x_val
            else:
                max_val = max(max_val, x_val)

        # noinspection PyTupleAssignmentBalance
        m, c = np.polyfit(x2, y2, 1)

        points = np.array([min_val, max_val])
        best_fit, = plt.plot(points, m * points + c, label=f"y = {m:.5}x + {c:.5}", color=colours[1])
        handles.append(best_fit)

    return handles


def smoothed_plot(x, y, show_best_fit, show_rank, colours, label):
    x2 = np.array(reduce(lambda a, b: a + b, x))

    x3 = np.linspace(min(x2), max(x2), round(len(x2) ** (7/8)))

    x4 = [[]]
    y4 = [[]]
    current_sec, current = 0, 0
    for i in range(len(x3) - 1):
        values = []
        if current_sec >= len(x):
            break
        while x[current_sec][current] <= x3[i+1]:
            values.append(y[current_sec][current])
            current += 1
            if current >= len(x[current_sec]):
                current = 0
                current_sec += 1
                if x4[-1]:
                    x4.append([])
                    y4.append([])
                break
        if values:
            x4[-1].append(statistics.mean((x3[i], x3[i+1])))
            y4[-1].append(statistics.mean(values))

    if not x4[-1]:
        x4.pop()
        y4.pop()

    handles = line_plot(x4, y4, show_best_fit, show_rank, colours, label)

    return handles


plotting_dict = {
    "Scatter": scatter_plot,
    "Line": line_plot,
    "Smoothed Line": smoothed_plot
}
