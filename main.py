from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound


if __name__ == '__main__':
    #"""
    tb1 = TokenBucketArrivalCurve(rate=1.5, burst=5)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=9)
    tb3 = TokenBucketArrivalCurve(rate=0.25, burst=13)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    sc = RateLatencyServiceCurve(rate=1.0, latency=3)

    q = backlog_bound(arrival_curve=pwl_ac, service_curve=sc, create_plot=True, plot_x_axis_max=25, plot_y_axis_max=25)
    d = delay_bound(arrival_curve=pwl_ac, service_curve=sc, create_plot=True, plot_x_axis_max=25, plot_y_axis_max=25)

    #create_plots.plot_convolution(arrival_curve=pwl, service_curve=sc, x_axis_range=[0, 35], y_axis_max=25)


    t_end = 35
    step = 0.01
    #solution_checker.convolution_solution_checker.convolution_solution_check(arrival_curve=pwl, service_curve=sc, t_end=t_end, step=step)


