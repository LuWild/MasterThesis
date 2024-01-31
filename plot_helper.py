from arrival_curves import *
from services_curves import *
import deconvolution_calculator

from bokeh.plotting import figure
import numpy as np
from typing import List


def plot_arrival_curve_token_bucket(p: figure, arrival_curve: TokenBucketArrivalCurve, x_max: int):
    """
    Adds the line to figure p for the arrival curve.

    :param p: figure
    :param arrival_curve: TokenBucketArrivalCurve
    :param x_max: for which value the line is plotted
    :return: -
    """
    t_data = [0]
    value_data = [arrival_curve.burst]
    for t in list(np.arange(0.01, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(arrival_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="blue", line_width=2)


def plot_arrival_curve_piecewise_linear(p: figure, arrival_curve: PiecewiseLinearArrivalCurve, x_max: int):
    """
    Adds the line to figure p for the arrival curve.

    :param p: figure
    :param arrival_curve: PiecewiseLinearArrivalCurve
    :param x_max: for which value the line is plotted
    :return: -
    """
    t_data = [0]
    value_data = [arrival_curve.gammas[0].burst]
    for t in list(np.arange(0.01, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(arrival_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="blue", line_width=2)


def plot_service_curve_rate_latency(p: figure, service_curve: RateLatencyServiceCurve, x_max: int):
    """
    Adds the line to figure p for the service curve.

    :param p: figure
    :param service_curve: RateLatencyServiceCurve
    :param x_max: for which value the line is plotted
    :return: -
    """
    t_data = []
    value_data = []
    for t in list(np.arange(0, x_max + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(service_curve.calculate_function_value(t))

    p.line(t_data, value_data, color="red", line_width=2)


def plot_deconvolution_n2(p: figure, arrival_curve: PiecewiseLinearArrivalCurve,
                          service_curve: RateLatencyServiceCurve, x_axis_range: List[int]):
    """
    Adds the line to figure p for the deconvolution (n=2).

    :param p: figure
    :param arrival_curve: PiecewiseLinearArrivalCurve
    :param service_curve: RateLatencyServiceCurve
    :param x_axis_range: for which value range the line is plotted
    :return: -
    """
    t_data = []
    value_data = []
    for t in list(np.arange(x_axis_range[0], x_axis_range[1] + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(deconvolution_calculator.deconvolution_n2(arrival_curve=arrival_curve,
                                                                    service_curve=service_curve, t=t))

    p.line(t_data, value_data, color="green", line_width=2)
