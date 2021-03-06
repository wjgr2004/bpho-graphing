import numpy as np


"""
This is the file for editing which models you can plot with their equations.

To add a model you need to write:
 - A function to create the label
 - A function for generating the points to plot
 - A function to validate the users inputs (you can uses any_numbers if there are no requirements)
 
You then need do add the functions to models_dict in the following format:
   "equation": [points_function, label_function, validation_function, [inputs]]
"""


def any_numbers(*_):
    return True


def linear(m, c, min_val, max_val):
    x = np.linspace(min_val, max_val, 2000)
    y = m * x + c
    return x, y


def linear_label(m, c):
    return f"y = {m}x + {c}"


def extended_exponential(a, r, c, min_val, max_val):
    x = np.linspace(min_val, max_val, 2000)
    y = a * (r ** x) + c
    return x, y


def extended_exponential_label(a, r, c):
    return f"y = {a}x{r}^x + {c}"


def check_extended_exponential(a, r, c):
    if r < 0:
        return False
    return True


def quadratic(a, b, c, min_val, max_val):
    x = np.linspace(min_val, max_val, 2000)
    y = a * x ** 2 + b * x + c
    return x, y


def quadratic_label(a, b, c):
    return f"{a}x^2 + {b}x + {c}"


models_dict = {
    "y = mx + c": [linear, linear_label, any_numbers, ["m", "c"]],
    "y = ar^x + c": [extended_exponential, extended_exponential_label, check_extended_exponential, ["a", "r", "c"]],
    "y = ax^2 + bx + c": [quadratic, quadratic_label, any_numbers, ["a", "b", "c"]]
}
