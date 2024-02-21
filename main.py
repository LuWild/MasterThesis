from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.delay_bound import delay_bound_brute_force
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period

from plotter import create_plots

if __name__ == '__main__':
    # """
    tb1 = TokenBucketArrivalCurve(rate=2.5, burst=3.0)
    tb2 = TokenBucketArrivalCurve(rate=1.5, burst=10.0)
    tb3 = TokenBucketArrivalCurve(rate=0.5, burst=26.0)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    rl1 = RateLatencyServiceCurve(rate=0.5, latency=4.0)
    rl2 = RateLatencyServiceCurve(rate=1.25, latency=10.0)
    rl3 = RateLatencyServiceCurve(rate=2.5, latency=16.0)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    print("pwl_ac intersections: " + str(pwl_ac.intersections))
    print("pwl_sc intersections: " + str(pwl_sc.intersections))

    # create_plots.plot_arrival_and_service_curve(arrival_curve=pwl_ac, service_curve=pwl_sc, x_axis_max=25, y_axis_max=25)

    q = backlog_bound(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=True, plot_x_axis_max=40,
                      plot_y_axis_max=50)
    d = delay_bound_brute_force(arrival_curve=pwl_ac, service_curve=pwl_sc, create_plot=True, plot_x_axis_max=40,
                                plot_y_axis_max=50)
    # d = delay_bound(arrival_curve=pwl_ac, service_curve=sc, create_plot=True, plot_x_axis_max=25, plot_y_axis_max=25)

    max_bp = max_length_backlogged_period(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print(max_bp)

    # create_plots.plot_convolution(arrival_curve=pwl, service_curve=sc, x_axis_range=[0, 35], y_axis_max=25)

    t_end = 35
    step = 0.01
    # solution_checker.convolution_solution_checker.convolution_solution_check(arrival_curve=pwl, service_curve=sc, t_end=t_end, step=step)
