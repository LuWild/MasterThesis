from arrival_curves import *
from services_curves import *

import create_plots
import solution_checker.deconvolution_solution_checker
import solution_checker.convolution_solution_checker

if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.5, burst=5)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=8)
    tb3 = TokenBucketArrivalCurve(rate=0.25, burst=13)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.0, latency=3)

    create_plots.create_plot_convolution(arrival_curve=pwl, service_curve=sc,
                                         x_axis_range=[0, 35], y_axis_max=25)

    t_end = 35
    step = 0.01
    solution_checker.convolution_solution_checker.convolution_solution_check(arrival_curve=pwl,
                                                                             service_curve=sc,
                                                                             t_end=t_end,
                                                                             step=step)

    """
    tb1 = TokenBucketArrivalCurve(rate=1.0, burst=8)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=5)
    
    create_plots.create_plot_deconvolution(arrival_curve=pwl, service_curve=sc,
                                           x_axis_range=[-15, 20], y_axis_max=25)

    t = [-15, 20, 0.1]
    s = [0, 100, 0.1]
    solution_checker.deconvolution_solution_checker.deconvolution_solution_check(arrival_curve=pwl,
                                                                                 service_curve=sc,
                                                                                 t_start=t[0],
                                                                                 t_end=t[1],
                                                                                 t_step=t[2],
                                                                                 s_start=s[0],
                                                                                 s_end=s[1],
                                                                                 s_step=s[2])
    """
