from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period
from solution_checker.deconvolution_solution_checker import deconvolution_solution_check
from dnc_leftover_service.fifo_leftover_service import FIFO_leftover_service_pwl
from plotter import create_plots
from plotter import interactive_plots
import numpy as np


def show_arrival_and_service_curve(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    create_plots.plot_arrival_and_service_curve(arrival_curve=ac,
                                                service_curve=sc,
                                                x_axis_max=25, y_axis_max=25)


def show_leftover_service_curve(ac, sc, theta: float):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :param theta: the theta used for the fifo leftover service curve calculation
    :return: bokeh plot will be opened in your browser
    """
    FIFO_leftover_service_pwl(cross_flow=ac, service_curve=sc, theta=theta)


def show_backlog_bound(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    q = backlog_bound(arrival_curve=ac, service_curve=sc, create_plot=True, plot_x_axis_max=25,
                      plot_y_axis_max=25)
    print("Backlog Bound: " + str(np.round(q, 3)))


def show_delay_bound(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    d = delay_bound(arrival_curve=ac, service_curve=sc, create_plot=True, plot_x_axis_max=25,
                    plot_y_axis_max=25)[0]
    print("Delay Bound: " + str(np.round(d, 3)))


def show_max_bp(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    max_bp = max_length_backlogged_period(arrival_curve=ac, service_curve=sc)
    print("Maximum length of a backlogged period: " + str(np.round(max_bp, 3)))


def show_convolution(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    create_plots.plot_convolution(arrival_curve=ac, service_curve=sc, x_axis_range=[0, 35], y_axis_max=25)


def show_deconvolution(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    t = [-25, 25, 0.1]
    s = [0, 50, 0.1]
    deconvolution_solution_check(arrival_curve=ac, service_curve=sc,
                                 t_start=t[0], t_end=t[1], t_step=t[2],
                                 s_start=s[0], s_end=s[1], s_step=s[2])


def show_interactive_plot(ac, sc):
    """
    :param ac: input arrival curve
    :param sc: input service curve
    :return: bokeh plot will be opened in your browser
    """
    interactive_plots.plot_interactive_backlog_bound(arrival_curve=ac, service_curve=sc,
                                                     x_axis_max=25, y_axis_max=25)


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2.0, burst=3)
    tb2 = TokenBucketArrivalCurve(rate=1.0, burst=5)
    tb3 = TokenBucketArrivalCurve(rate=0.50, burst=10)
    arrival_curve = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    arrival_curve.print_all_information()

    rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
    rl2 = RateLatencyServiceCurve(rate=1.25, latency=4)
    rl3 = RateLatencyServiceCurve(rate=2.0, latency=7)
    service_curve = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    service_curve.print_all_information()

    print("------------------------")

    show_arrival_and_service_curve(ac=arrival_curve, sc=service_curve)

    show_interactive_plot(ac=arrival_curve, sc=service_curve)

    show_leftover_service_curve(ac=arrival_curve, sc=service_curve, theta=10)

    show_backlog_bound(ac=arrival_curve, sc=service_curve)

    show_delay_bound(ac=arrival_curve, sc=service_curve)

    show_max_bp(ac=arrival_curve, sc=service_curve)

    show_convolution(ac=arrival_curve, sc=service_curve)

    show_deconvolution(ac=arrival_curve, sc=service_curve)

