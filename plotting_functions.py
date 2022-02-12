import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from functools import reduce


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


plotting_dict = {
    "Scatter": scatter_plot,
    "Line": line_plot
}
