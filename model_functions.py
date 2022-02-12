import numpy as np


def convert_to_number(n):
    return float(n)


def linear(m, c, min_val, max_val):
    x = np.array([min_val, max_val])
    y = m * x + c
    return x, y


def linear_header(m, c):
    return f"y = {m}x + {c}"


plotting_dict = {
    "y = mx + c": [linear, linear_header, ["m", "c"]]
}
