from create_plots import *

if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2.5, burst=4)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=5)
    create_plot_deconvolution_n2_case1(arrival_curve=pwl, service_curve=sc, x_axis_range=[-20, 20], y_axis_max=25)

    tb1 = TokenBucketArrivalCurve(rate=2, burst=3)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=12)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=4)
    create_plot_deconvolution_n2_case2(arrival_curve=pwl, service_curve=sc, x_axis_range=[-26, 20], y_axis_max=25)


