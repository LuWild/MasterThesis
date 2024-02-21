from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from plotter.create_plots import plot_delay_bound

import numpy as np


def delay_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    R = service_curve.rate
    T = service_curve.latency
    ta_and_gamma_a = arrival_curve.calculate_intersection_t_a_and_gamma_a(R)
    ta = ta_and_gamma_a[0]
    ra = ta_and_gamma_a[1].rate
    ba = ta_and_gamma_a[1].burst

    d = T - ta + (ba + ra * ta) / R

    print("Delay Bound: " + str(d))

    if create_plot:
        plot_delay_bound(arrival_curve=arrival_curve, service_curve=service_curve, ta=ta, d=d,
                         x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max)
    else:
        return d


def delay_bound_brute_force(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                            create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    # 0.01

    d_max = -1
    d_max_intersection = -1
    for intersection in arrival_curve.intersections:
        ac_value = arrival_curve.calculate_function_value(t=intersection)
        print("intersection: " + str(intersection) + " ; ac_value: " + str(ac_value))
        for x in list(np.arange(intersection, plot_x_axis_max + 0.01, 0.01)):
            sc_value = service_curve.calculate_function_value(x)
            print("sc_value: " + str(sc_value))
            if sc_value - ac_value < 0.03:
                if (x - intersection) > d_max:
                    d_max = x - intersection
                    d_max_intersection = intersection

    ta = d_max_intersection
    d = d_max

    print("Delay Bound: " + str(d))

    if create_plot:
        plot_delay_bound(arrival_curve=arrival_curve, service_curve=service_curve, ta=ta, d=d,
                         x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max)
    else:
        return d
