import copy
from typing import List

from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve

from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift


def deconvolution_n2(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    """
    Calculates the deconvolution of a PiecewiseLinearArrivalCurve (n=2) and a RateLatencyServiceCurve for
    the given value t.

    :param arrival_curve: PiecewiseLinearArrivalCurve
    :param service_curve: RateLatencyServiceCurve
    :param t: value t
    :return: deconvolution of PiecewiseLinearArrivalCurve and RateLatencyServiceCurve of t
    """

    R = service_curve.rate
    T = service_curve.latency

    r1 = arrival_curve.gammas[0].rate
    b1 = arrival_curve.gammas[0].burst

    r2 = arrival_curve.gammas[1].rate
    b2 = arrival_curve.gammas[1].burst

    t1 = arrival_curve.intersections[0]

    if t <= (t1 - T):
        if r1 <= R:
            if t <= -T:
                # print("Used Case: Iaa")
                return R * (t + T) + b1
            else:
                # print("Used Case: Iab")
                return r1 * (t + T) + b1
        else:
            # print("Used Case: Ib")
            return R * (t + T - t1) + b2 + r2 * t1
    else:
        # print("Used Case: II")
        return r2 * (t + T) + b2


def deconvolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    R = service_curve.rate
    T = service_curve.latency

    ta_and_gamma = arrival_curve.calculate_intersection_t_a_and_gamma_a(R=R)
    ta = ta_and_gamma[0]
    ra = ta_and_gamma[1].rate
    ba = ta_and_gamma[1].burst

    if t <= ta - T:
        return R * (t + T - ta) + ba + ra * ta
    else:
        return arrival_curve.calculate_function_value(t=t + T)


def deconvolution_test(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                       t: float):
    from dnc_operations.backlog_bound import backlog_bound
    shifted_arrival_curve = piecewise_linear_arrival_curve_shift(arrival_curve=arrival_curve, t_shift=t)
    return backlog_bound(arrival_curve=shifted_arrival_curve,service_curve=service_curve)


def create_plot_deconvolution_test(arrival_curve: PiecewiseLinearArrivalCurve,
                                   service_curve: PiecewiseLinearServiceCurve,
                                   x_axis_range: List[int], y_axis_max: int):
    from bokeh.plotting import figure, show
    import numpy as np
    from plotter.plot_helper import add_service_curve, add_arrival_curve

    p = figure(title="Deconvolution NEW test", x_axis_label="x", y_axis_label="y")

    add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_range[1] - 1)
    add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_range[1] - 1)

    t_data = []
    value_data = []
    for t in list(np.arange(x_axis_range[0], x_axis_range[1] + 0.01, 0.01)):
        t_data.append(t)
        value_data.append(deconvolution_test(arrival_curve=arrival_curve, service_curve=service_curve, t=t))

    p.line(t_data, value_data, color="green", line_width=2)

    # plot settings
    p.x_range.start = x_axis_range[0]
    p.x_range.end = x_axis_range[1]
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    show(p)
