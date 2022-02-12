import math


def linear(val):
    return val


def logarithmic(val):
    return math.log10(val)


def reciprocal(val):
    return 1 / val


def squared(val):
    return math.pow(val, 2)


function_dict = {
    "x: x": linear,
    "x: log(x)": logarithmic,
    "x: 1/x": reciprocal,
    "x: x^2": squared
}