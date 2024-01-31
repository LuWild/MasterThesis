from arrival_curves import *
from services_curves import *

import create_plots
import solution_checker.deconvolution_n2_solution_checker

if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.0, burst=4)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=5)

    create_plots.create_plot_deconvolution_n2(arrival_curve=pwl, service_curve=sc,
                                              x_axis_range=[-15, 20], y_axis_max=25)

    t = [-15, 20, 0.1]
    s = [0, 100, 0.1]
    solution_checker.deconvolution_n2_solution_checker.deconvolution_n2_solution_check(arrival_curve=pwl,
                                                                                       service_curve=sc,
                                                                                       t_start=t[0],
                                                                                       t_end=t[1],
                                                                                       t_step=t[2],
                                                                                       s_start=s[0],
                                                                                       s_end=s[1],
                                                                                       s_step=s[2])
