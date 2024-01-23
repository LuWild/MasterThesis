from arrival_curves import *
from services_curves import *
from calculator import *

from typing import List


def linear_function(r, a, b, values):
    """
    Calculates function values for a given array of values. The function has the following form:
    r(t+a)+b

    :param r: rate
    :param a: x-axis shift
    :param b: y-axis shift
    :param values: values for which the function values are calculated for
    :return: array of function values
    """
    function_values = []
    for t in values:
        f_t = r * (t + a) + b
        function_values.append(f_t)

    return function_values


def piecewise_linear_function(pwl: PiecewiseLinearArrivalCurve, values):
    """
    :param pwl: PiecewiseLinearArrivalCurve
    :param values: values for which the function values are calculated for
    :return: array of function values
    """

    function_values = []
    function_value_candidate = []
    for t in values:
        for gamma in pwl.gammas:
            r = gamma.rate
            b = gamma.burst
            f_t = r * t + b
            function_value_candidate.append(f_t)
        function_values.append(min(function_value_candidate))
        function_value_candidate = []

    return function_values


def rate_latency_function(R, T, values):
    """
    :param R: rate
    :param T: latency
    :param values: values for which the function values are calculated for
    :return: array of function values
    """

    function_values = []
    for t in values:
        if t <= T:
            f_t = 0
        else:
            f_t = R * (t - T)
        function_values.append(f_t)

    return function_values
