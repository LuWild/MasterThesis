from arrival_curves import *
from services_curves import *
from calculator import *

from typing import List
import numpy as np


def deconvolution_n2_case1(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                           x_axis_range: List[int]):
    """
    (n=2, Case I): Prepares the data to create the plot

    :param arrival_curve: arrival curve
    :param service_curve: service curve
    :param x_axis_range: range on x-axis for data preparation, e.g., [-20,20]
    :return: List of Lists of Data for the plot
    """

    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    R = service_curve.rate
    T = service_curve.latency

    r1 = arrival_curve.gammas[0].rate
    b1 = arrival_curve.gammas[0].burst

    r2 = arrival_curve.gammas[1].rate
    b2 = arrival_curve.gammas[1].burst

    t1 = arrival_curve.intersections[0]

    # Service Curve:
    service_curve_x = list(np.arange(0, x_axis_max + 0.01, 0.01))
    service_curve_y = rate_latency_function(R=R, T=T, values=service_curve_x)
    # Arrival Curve:
    arrival_curve_x = list(np.arange(0, x_axis_max + 0.01, 0.01))
    arrival_curve_y = piecewise_linear_function(pwl=arrival_curve, values=arrival_curve_x)

    gamma_2_dotted_x = list(np.arange(0, t1 + 0.01, 0.01))
    gamma_2_dotted_y = linear_function(r=r2, a=0, b=b2, values=gamma_2_dotted_x)

    # Case Ia:
    # Case Iaa:
    case_Iaa_x = list(np.arange(x_axis_min, -T + 0.01, 0.01))
    case_Iaa_y = linear_function(r=R, a=T, b=b2, values=case_Iaa_x)

    # Case Iab:
    case_Iab_x = list(np.arange(-T, -t1 + 0.01, 0.01))
    case_Iab_y = linear_function(r=r2, a=T, b=b2, values=case_Iab_x)

    # Case Ib:
    i = (r2 * T - r1 * t1 + b2 - b1) / (r1 - r2)
    # Case Iba:
    case_Iba_x = list(np.arange(-t1, i + 0.01, 0.01))
    case_Iba_y = linear_function(r=r2, a=T, b=b2, values=case_Iba_x)

    # Case Ibb:
    case_Ibb_x = list(np.arange(i, x_axis_max + 0.01, 0.01))
    case_Ibb_y = linear_function(r=r1, a=t1, b=b1, values=case_Ibb_x)

    return [[service_curve_x, service_curve_y],
            [arrival_curve_x, arrival_curve_y],
            [gamma_2_dotted_x, gamma_2_dotted_y],
            [case_Iaa_x, case_Iaa_y],
            [case_Iab_x, case_Iab_y],
            [case_Iba_x, case_Iba_y],
            [case_Ibb_x, case_Ibb_y]]


def deconvolution_n2_case2(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                           x_axis_range: List[int]):
    """
    (n=2, Case II): Prepares the data to create the plot

    :param arrival_curve: arrival curve
    :param service_curve: service curve
    :param x_axis_range: range on x-axis for data preparation, e.g., [-20,20]
    :return: List of Lists of Data for the plot
    """

    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    R = service_curve.rate
    T = service_curve.latency

    r1 = arrival_curve.gammas[0].rate
    b1 = arrival_curve.gammas[0].burst

    r2 = arrival_curve.gammas[1].rate
    b2 = arrival_curve.gammas[1].burst

    t1 = arrival_curve.intersections[0]

    # Service Curve:
    service_curve_x = list(np.arange(0, x_axis_max + 0.01, 0.01))
    service_curve_y = rate_latency_function(R=R, T=T, values=service_curve_x)
    # Arrival Curve:
    arrival_curve_x = list(np.arange(0, x_axis_max + 0.01, 0.01))
    arrival_curve_y = piecewise_linear_function(pwl=arrival_curve, values=arrival_curve_x)

    gamma_2_dotted_x = list(np.arange(0, t1 + 0.01, 0.01))
    gamma_2_dotted_y = linear_function(r=r2, a=0, b=b2, values=gamma_2_dotted_x)

    # Case IIa:
    case_IIa_x = list(np.arange(x_axis_min, -t1 + 0.01, 0.01))
    case_IIa_y = linear_function(r=r2, a=t1, b=(R * (T - t1) + b2), values=case_IIa_x)

    # Case IIb:
    i = ((r2 - R) * t1 + (R - r1) * T + b2 - b1) / (r1 - r2)
    if r1 <= R:
        # Case IIbba:
        case_IIbba_x = list(np.arange(-t1, i + 0.01, 0.01))
        case_IIbba_y = linear_function(r=r2, a=t1, b=(R * (T - t1) + b2), values=case_IIbba_x)

        # Case IIbab:
        case_IIbab_x = list(np.arange(i, x_axis_max + 0.01, 0.01))
        case_IIbab_y = linear_function(r=r1, a=T, b=b1, values=case_IIbab_x)

        return [[service_curve_x, service_curve_y],
                [arrival_curve_x, arrival_curve_y],
                [gamma_2_dotted_x, gamma_2_dotted_y],
                [case_IIa_x, case_IIa_y],
                [case_IIbba_x, case_IIbba_y],
                [case_IIbab_x, case_IIbab_y]]
    else:
        # Case IIbb:
        case_IIbb_x = list(np.arange(-t1, x_axis_max + 0.01, 0.01))
        case_IIbb_y = linear_function(r=r1, a=t1, b=(R * (T - t1) + b1), values=case_IIbb_x)

        return [[service_curve_x, service_curve_y],
                [arrival_curve_x, arrival_curve_y],
                [gamma_2_dotted_x, gamma_2_dotted_y],
                [case_IIa_x, case_IIa_y],
                [case_IIbb_x, case_IIbb_y]]

