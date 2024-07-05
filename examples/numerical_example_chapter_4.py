from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period
from plotter import custom_plots

import numpy as np

if __name__ == '__main__':
    print("Arrival Curve:")
    tb1 = TokenBucketArrivalCurve(rate=2.0, burst=3)
    tb2 = TokenBucketArrivalCurve(rate=1.0, burst=5)
    tb3 = TokenBucketArrivalCurve(rate=0.50, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    pwl_ac.print_all_information()

    print("")
    print("Service Curve:")
    rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
    rl2 = RateLatencyServiceCurve(rate=1.25, latency=4)
    rl3 = RateLatencyServiceCurve(rate=2.0, latency=7)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    pwl_sc.print_all_information()

    print("----------")

    q = backlog_bound(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print("Backlog Bound: " + str(q))

    d = delay_bound(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print("Delay Bound: " + str(np.round(d[0], 3)))

    bp = max_length_backlogged_period(arrival_curve=pwl_ac, service_curve=pwl_sc)
    print("Max. length of backlogged period: " + str(np.round(bp, 3)))

    custom_plots.plot_example(arrival_curve=pwl_ac, service_curve=pwl_sc, chapter=4)
