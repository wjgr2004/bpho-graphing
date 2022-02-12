import numpy as np


def convert_to_number(n):
    if not n:
        return 0
    try:
        return float(n)
    except ValueError:
        return False


def any_number(*_):
    return True


def linear(m, c, min_val, max_val):
    x = np.array([min_val, max_val])
    y = m * x + c
    return x, y


def linear_header(m, c):
    return f"y = {m}x + {c}"


def extended_exponential(a, r, c, min_val, max_val):
    x = np.linspace(min_val, max_val, 1000)
    y = a * (r ** x) + c
    return x, y


def extended_exponential_header(a, r, c):
    return f"y = {a}x{r}^x + {c}"


def check_extended_exponential(a, r, c):
    if r < 0:
        return False
    return True


plotting_dict = {
    "y = mx + c": [linear, linear_header, any_number, ["m", "c"]],
    "y = ar^x + c": [extended_exponential, extended_exponential_header, check_extended_exponential, ["a", "r", "c"]]
}
