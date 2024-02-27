from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.delay_bound import delay_bound_brute_force
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period
from solution_checker.deconvolution_solution_checker import deconvolution_solution_check
from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift

from plotter import create_plots

if __name__ == '__main__':
    # """
    tb1 = TokenBucketArrivalCurve(rate=2.0, burst=2)
    tb2 = TokenBucketArrivalCurve(rate=1.0, burst=6)
    tb3 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=3)
    rl2 = RateLatencyServiceCurve(rate=2.5, latency=7)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])
    print("pwl_ac intersections: " + str(pwl_ac.intersections))
    print("pwl_sc intersections: " + str(pwl_sc.intersections))

    # create_plots.plot_arrival_and_service_curve(arrival_curve=pwl_ac, service_curve=pwl_sc, x_axis_max=25, y_axis_max=25)

    create_plots.plot_arrival_and_service_curve(arrival_curve=piecewise_linear_arrival_curve_shift(pwl_ac, 5),
                                                service_curve=pwl_sc,
                                                x_axis_max=25, y_axis_max=25)

    q = backlog_bound(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=False, plot_x_axis_max=40,
                      plot_y_axis_max=50)
    d = delay_bound_brute_force(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=False, plot_x_axis_max=40,
                                plot_y_axis_max=50)
    # d = delay_bound(arrival_curve=pwl_ac, service_curve=sc, create_plot=True, plot_x_axis_max=25, plot_y_axis_max=25)

    max_bp = max_length_backlogged_period(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print("Maximum length of a backlogged period: " + str(max_bp))

    # create_plots.plot_convolution(arrival_curve=pwl, service_curve=sc, x_axis_range=[0, 35], y_axis_max=25)

    t = [-15, 25, 0.1]
    s = [0, 100, 0.1]
    print("Starting Solution Check")
    print("...")
    deconvolution_solution_check(arrival_curve=pwl_ac, service_curve=pwl_sc,
                                 t_start=t[0], t_end=t[1], t_step=t[2],
                                 s_start=s[0], s_end=s[1], s_step=s[2])
    print("Solution Check Completed")

    create_plots.plot_deconvolution(arrival_curve=pwl_ac, service_curve=pwl_sc, x_axis_range=[-15, 25], y_axis_max=25)
