from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
import dnc_operations.function_invert

from plotter.create_plots import plot_delay_bound

import numpy as np

import time


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


def delay_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    start_time = time.time()
    T = [0]
    T.extend(arrival_curve.intersections)
    U = service_curve.intersections

    d_alpha = float('-inf')
    t_min = float('inf')
    for t in T:
        alpha_x = arrival_curve.get_used_gamma(t)
        alpha_of_t = arrival_curve.calculate_function_value(t)
        beta_inverse = dnc_operations.function_invert.invert_piecewise_linear_service_curve(service_curve)
        b = beta_inverse.calculate_function_value(alpha_of_t)
        beta_y = service_curve.get_used_rho(b)
        if alpha_x.rate <= beta_y.rate:
            t_min = t
            d_alpha = b - t
            break

    d_beta = float('-inf')
    u_min = float('inf')
    for u in U:
        beta_x = service_curve.get_used_rho(u)
        beta_of_u = service_curve.calculate_function_value(u)
        alpha_inverse = dnc_operations.function_invert.invert_piecewise_linear_arrival_curve(arrival_curve)
        a = alpha_inverse.calculate_function_value(beta_of_u)
        alpha_y = arrival_curve.get_used_gamma(a)
        if beta_x.rate >= alpha_y.rate:
            u_min = u
            d_beta = u - a
            break

    if d_alpha >= d_beta:
        d = d_alpha
        intersection_used = t_min
        case = 1
    else:
        d = d_beta
        intersection_used = u_min
        case = 2

    # print("Delay Bound Runtime: " + str(time.time() - start_time))

    # print("Delay Bound: " + str(d))

    if create_plot:
        plot_delay_bound(arrival_curve=arrival_curve, service_curve=service_curve, ta=intersection_used, d=d,
                         x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max, case=case)
    else:
        return d


def delay_bound_brute_force(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                            create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    start_time = time.time()
    d_max = -1
    d_max_intersection = -1
    case = -1
    for intersection in arrival_curve.intersections:
        ac_value = arrival_curve.calculate_function_value(t=intersection)
        for x in list(np.arange(intersection, plot_x_axis_max + 0.01, 0.01)):
            sc_value = service_curve.calculate_function_value(t=x)
            if sc_value - ac_value < 0.03:
                if (x - intersection) > d_max:
                    d_max = x - intersection
                    d_max_intersection = intersection
                    case = 1

    for intersection in service_curve.intersections:
        sc_value = service_curve.calculate_function_value(t=intersection)
        for x in list(np.arange(0, intersection + 0.01, 0.01)):
            ac_value = arrival_curve.calculate_function_value(t=x)
            if sc_value - ac_value < 0.03:
                if (intersection - x) > d_max:
                    d_max = intersection - x
                    d_max_intersection = intersection
                    case = 2

    ta = d_max_intersection
    d = d_max

    print("Delay Bound (Brute Force) Runtime: " + str(time.time() - start_time))

    print("Delay Bound (Brute Force): " + str(d))

    if create_plot:
        plot_delay_bound(arrival_curve=arrival_curve, service_curve=service_curve, ta=ta, d=d,
                         x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max, case=case)
    else:
        return d
