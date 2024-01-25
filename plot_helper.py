from arrival_curves import *
from services_curves import *
from bokeh.plotting import figure

import numpy as np


def plot_arrival_curve_token_bucket(p: figure, arrival_curve: TokenBucketArrivalCurve, x_max: int):
    """

    :param p:
    :param arrival_curve:
    :param x_max:
    :return:
    """
    t_data = [0]
    value_data = [arrival_curve.burst]
    for t in list(np.arange(0.01, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(arrival_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="blue", line_width=2)


def plot_arrival_curve_piecewise_linear(p: figure, arrival_curve: PiecewiseLinearArrivalCurve, x_max: int):
    """

    :param p:
    :param arrival_curve:
    :param x_max:
    :return:
    """
    t_data = [0]
    value_data = [arrival_curve.gammas[0].burst]
    for t in list(np.arange(0.01, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(arrival_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="blue", line_width=2)


def plot_service_curve_rate_latency(p: figure, service_curve: RateLatencyServiceCurve, x_max: int):
    """

    :param p:
    :param service_curve:
    :param x_max:
    :return:
    """
    t_data = []
    value_data = []
    for t in list(np.arange(0, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(service_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="red", line_width=2)
