from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.delay_bound import delay_bound
import dnc_operations.function_invert
from typing import List
import numpy as np
import math
from bokeh.plotting import figure, show, output_file


def FIFO_leftover_service_pwl(cross_flow: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                              theta=0.0, x_axis_max=25, y_axis_max=25):

    d_and_calc_info = delay_bound(arrival_curve=cross_flow, service_curve=service_curve)
    d = d_and_calc_info[0]
    # print(d)

    jump = theta > d

    x_delaybound = -1
    if jump:
        # print(d_and_calc_info[1][0])
        if d_and_calc_info[1][0] == 1:
            x_delaybound = d_and_calc_info[1][1] + theta
        else:
            x_delaybound = d_and_calc_info[1][1]

    # print(x_delaybound)

    cross_flow.set_shift(shift=theta)

    t_data = []
    value_data = []
    for t in list(np.arange(0, x_axis_max + 0.01, 0.01)):
        t_data.append(t)

        if t > theta:
            value = service_curve.calculate_function_value(t) - cross_flow.calculate_function_value(t)
            if jump:
                if x_delaybound > d:
                    if t >= x_delaybound:
                        value_data.append(value)
                    else:
                        value_data.append(0)
                else:
                    value_data.append(value)
            else:
                value_data.append(value)

            """
            if value > 0:
                value_data.append(value)
            else:
                value_data.append(0)
            """
        else:
            value_data.append(0)

    intersection_and_rate = create_intersections_and_rates(t_data=t_data, value_data=value_data, theta=theta)

    # print(intersection_and_rate)

    p = figure(title="Leftover Service Curve", x_axis_label="t", y_axis_label="y")

    p.line(t_data, value_data, color="red", line_width=2)

    # plot settings
    p.x_range.start = 0 - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    show(p)

    cross_flow.set_shift(0)


def create_intersections_and_rates(t_data: List[float], value_data: List[float], theta: float):
    time_step = t_data[1]
    slope_old = 0
    intersection_and_rates = []
    for i in np.arange(0, len(value_data)-1):
        if t_data[i] >= theta:
            slope_new = np.round(((value_data[i+1] - value_data[i]) / time_step), 4)
            if slope_new != slope_old:
                intersection_and_rates.append([np.round(t_data[i], 2), slope_old])
            slope_old = slope_new
    intersection_and_rates.append([math.inf, slope_old])

    result = []
    for i in range(0, len(intersection_and_rates)):
        if intersection_and_rates[i][1] != 0:
            result.append([[intersection_and_rates[i-1][0], intersection_and_rates[i][0]],
                           intersection_and_rates[i][1]])
        else:
            result.append([[0, intersection_and_rates[i][0]], 0])

    return result


def build_piecewise_linear_service_curve_by_intersections_and_rates(intersections_and_rates: List):
    for i in range(0, len(intersections_and_rates)):
        if intersections_and_rates[i][1] == 0:
            initial_latency = intersections_and_rates[i][0][2]


def get_optimal_theta_for_min_latency(service_curve: PiecewiseLinearServiceCurve,
                                      cross_flow: PiecewiseLinearArrivalCurve):
    opt_theta = delay_bound(arrival_curve=cross_flow, service_curve=service_curve)[0]

    return opt_theta


def get_optimal_theta_for_min_backlog_bound(service_curve: PiecewiseLinearServiceCurve,
                                            cross_flow: PiecewiseLinearArrivalCurve):
    opt_theta = get_optimal_theta_for_min_latency(service_curve=service_curve, cross_flow=cross_flow)

    return opt_theta


def get_optimal_theta_for_min_delay_bound(service_curve: PiecewiseLinearServiceCurve,
                                          cross_flow: PiecewiseLinearArrivalCurve):
    beta_inverse = dnc_operations.function_invert.invert_piecewise_linear_service_curve(service_curve=service_curve)
    opt_theta = beta_inverse.calculate_function_value(2*cross_flow.get_initial_burst())

    return opt_theta


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2.0, burst=3)
    tb2 = TokenBucketArrivalCurve(rate=1.0, burst=5)
    tb3 = TokenBucketArrivalCurve(rate=0.50, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    pwl_ac.print_all_information()
    # pwl_ac.set_shift(shift=5)

    rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
    rl2 = RateLatencyServiceCurve(rate=1.25, latency=4)
    rl3 = RateLatencyServiceCurve(rate=2.0, latency=7)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    pwl_sc.print_all_information()

    print("----------------------------------------------------------------------------")

    FIFO_leftover_service_pwl(cross_flow=pwl_ac, service_curve=pwl_sc, theta=15)
    print(get_optimal_theta_for_min_latency(service_curve=pwl_sc, cross_flow=pwl_ac))
    print(get_optimal_theta_for_min_backlog_bound(service_curve=pwl_sc, cross_flow=pwl_ac))
    print(get_optimal_theta_for_min_delay_bound(service_curve=pwl_sc, cross_flow=pwl_ac))
