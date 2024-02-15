from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from plotter.create_plots import plot_backlog_bound


def backlog_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                  create_plot=False, plot_x_axis_max=-1, plot_y_axis_max=-1):
    R = service_curve.rate
    T = service_curve.latency
    ta = arrival_curve.calculate_intersection_t_a_and_gamma_a(R)[0]

    if ta <= T:
        q = arrival_curve.calculate_function_value(T)
        t = T
    else:
        q = arrival_curve.calculate_function_value(ta) - service_curve.calculate_function_value(ta)
        t = ta

    print("Backlog Bound: " + str(q))

    if create_plot:
        plot_backlog_bound(arrival_curve=arrival_curve, service_curve=service_curve, backlog_bound_t=t,
                           x_axis_max=plot_x_axis_max, y_axis_max=plot_y_axis_max)
    else:
        return q
