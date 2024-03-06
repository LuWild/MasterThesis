from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.delay_bound import delay_bound_brute_force
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period
from solution_checker.deconvolution_solution_checker import deconvolution_solution_check
from solution_checker.convolution_solution_checker import convolution_solution_check
from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift
import dnc_operations.function_invert

from plotter import create_plots
from plotter import custum_plots
from plotter import interactive_plots

import os
import time


def show_arrival_and_service_curve():
    create_plots.plot_arrival_and_service_curve(arrival_curve=pwl_ac,
                                                service_curve=pwl_sc,
                                                x_axis_max=25, y_axis_max=25)


def show_backlog_bound():
    q = backlog_bound(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=True, plot_x_axis_max=25,
                      plot_y_axis_max=25)


def show_delay_bound():
    d = delay_bound(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=True, plot_x_axis_max=25,
                    plot_y_axis_max=25)
    d = delay_bound_brute_force(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=True, plot_x_axis_max=25,
                                plot_y_axis_max=25)


def show_max_bp():
    max_bp = max_length_backlogged_period(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print("Maximum length of a backlogged period: " + str(max_bp))


def show_convolution():
    t_end = 35
    step = 0.01
    print("Starting Solution Check")
    print("...")
    convolution_solution_check(arrival_curve=pwl_ac, service_curve=pwl_sc, t_end=t_end, step=step)
    print("Solution Check Completed")

    create_plots.plot_convolution(arrival_curve=pwl_ac, service_curve=pwl_sc, x_axis_range=[0, 35], y_axis_max=25)


def show_deconvolution():
    t = [-25, 25, 0.1]
    s = [0, 100, 0.1]
    deconvolution_solution_check(arrival_curve=pwl_ac, service_curve=pwl_sc,
                                 t_start=t[0], t_end=t[1], t_step=t[2],
                                 s_start=s[0], s_end=s[1], s_step=s[2])

    file_name = "output/csv_files/a_of_t_deconvolution.csv"
    os.remove(file_name)
    create_plots.plot_deconvolution(arrival_curve=pwl_ac, service_curve=pwl_sc, x_axis_range=[-25, 25], y_axis_max=25)
    custum_plots.custom_plot_a_of_t(x_axis_range=[-25, 25], y_axis_max=25)


def show_interactive_plot():
    interactive_plots.plot_interactive_backlog_bound(arrival_curve=pwl_ac, service_curve=pwl_sc,
                                                     x_axis_max=25, y_axis_max=25)


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2.5, burst=2)
    tb2 = TokenBucketArrivalCurve(rate=1.1, burst=6)
    tb3 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    pwl_ac.print_all_information()

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=3)
    rl2 = RateLatencyServiceCurve(rate=1.5, latency=7)
    rl3 = RateLatencyServiceCurve(rate=2.5, latency=12)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    pwl_sc.print_all_information()

    # show_arrival_and_service_curve()

    # show_backlog_bound()

    show_delay_bound()

    # show_arrival_and_service_curve()

    # show_convolution()

    # show_deconvolution()

    # show_interactive_plot()
