import math


"""
This is the file for the transformations you can apply to the data.

To add a function write the function then add it to function_dict in the format:
   "equation": function
"""


def linear(val):
    return val


def logarithmic(val):
    return math.log10(val)


def reciprocal(val):
    return 1 / val


def squared(val):
    return math.pow(val, 2)


def sin(val):
    return math.sin(math.radians(val))


def cos(val):
    return math.cos(math.radians(val))


function_dict = {
    "x: x": linear,
    "x: log(x)": logarithmic,
    "x: 1/x": reciprocal,
    "x: x^2": squared,
    "x: sin(x)": sin,
    "x: cos(x)": cos
}