from dnc_arrivals.arrival_curve import ArrivalCurve
from dnc_service.service_curve import ServiceCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve

from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift
from dnc_operations import backlog_bound

import csv
import os.path
import time


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


def deconvolution(arrival_curve: ArrivalCurve, service_curve: ServiceCurve, t: float):
    deconvolution(arrival_curve=arrival_curve, service_curve=service_curve, t=t)


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


def deconvolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve, t: float):
    shifted_arrival_curve = piecewise_linear_arrival_curve_shift(arrival_curve=arrival_curve, t_shift=t)
    q_and_a = backlog_bound.backlog_bound(arrival_curve=shifted_arrival_curve, service_curve=service_curve,
                                          deconvolution_case=True)
    a = q_and_a[1]

    row_data = [str(t), str(a)]

    file_name = "output/csv_files/a_of_t_deconvolution.csv"
    if os.path.isfile(file_name):
        with open(file_name, 'a', newline='') as file:
            csv.writer(file).writerow(row_data)
    else:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            column_names = ["t", "a"]
            writer.writerow(column_names)
            writer.writerow(row_data)
        time.sleep(4)

    return q_and_a[0]

