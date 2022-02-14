import math
import statistics
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from functools import reduce


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


def scatter_plot(x, y, show_best_fit, rank, colours, label, polar):
    x = reduce(lambda a, b: a + b, x)
    if polar:
        x = list(map(math.radians, x))
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
        line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text, alpha=.15)
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

        if polar:
            points = np.linspace(min_val, max_val, 2000)
        else:
            points = np.array([min_val, max_val])
        best_fit, = plt.plot(points, m * points + c, label=f"y = {m:.5}x + {c:.5}", color=colours[1])
        handles.append(best_fit)

    return handles


def line_plot(x, y, show_best_fit, rank, colours, label, polar):
    handles = []
    x2 = np.array(reduce(lambda a, b: a + b, x))
    y2 = np.array(reduce(lambda a, b: a + b, y))

    if rank:
        r, p = scipy.stats.pearsonr(x2, y2)
        rank_text = f"\nr = {r:.4}, p = {p:.4}"
    else:
        rank_text = ""

    for x_sec, y_sec in zip(x, y):
        if polar:
            x_sec = list(map(math.radians, x_sec))
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

        if polar:
            points = np.linspace(min_val, max_val, 2000)
        else:
            points = np.array([min_val, max_val])
        best_fit, = plt.plot(list(map(math.radians, points)), m * points + c, label=f"y = {m:.5}x + {c:.5}", color=colours[1])
        handles.append(best_fit)
    return handles


def smoothed_plot(x, y, show_best_fit, show_rank, colours, label, polar):
    x2 = np.array(reduce(lambda a, b: a + b, x))
    y2 = np.array(reduce(lambda a, b: a + b, y))
    vals = list(zip(x2, y2))
    vals.sort(key=lambda a: a[0])

    x3 = np.linspace(min(x2), max(x2), round((len(x2) ** (2/3)) / 1.6))

    x4 = [[]]
    y4 = [[]]
    current = 1
    y_values = []
    for x_val, y_val in vals:
        if x_val <= x3[current]:
            y_values.append(y_val)
        else:
            if y_values:
                x4[-1].append(statistics.mean((x3[current - 1], x3[current])))
                y4[-1].append(statistics.mean(y_values))
            elif x4[-1]:
                x4.append([])
                y4.append([])
            current += 1
            y_values = []

    if not x4[-1]:
        x4.pop()
        y4.pop()

    handles = line_plot(x4, y4, show_best_fit, show_rank, colours, label, polar)

    return handles


plotting_dict = {
    "Scatter": scatter_plot,
    "Line": line_plot,
    "Smoothed Line": smoothed_plot
}
