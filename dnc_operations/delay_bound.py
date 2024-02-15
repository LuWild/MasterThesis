from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from plotter.create_plots import plot_delay_bound


def delay_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    R = service_curve.rate
    T = service_curve.latency
    ta_and_gamma_a = arrival_curve.calculate_intersection_t_a_and_gamma_a(R)
    ta = ta_and_gamma_a[0]
    ra = ta_and_gamma_a[1].rate
    ba = ta_and_gamma_a[1].burst

    d = T - ta + (ba + ra * ta) / R

    print("Delay Bound: " + str(d))

    if create_plot:
        plot_delay_bound(arrival_curve=arrival_curve, service_curve=service_curve, ta=ta, d=d,
                         x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max)
    else:
        return d
