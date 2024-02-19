from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve


def max_length_backlogged_period(arrival_curve: PiecewiseLinearArrivalCurve,
                                 service_curve: RateLatencyServiceCurve):
    A = []
    for i in arrival_curve.intersections:
        alpha = arrival_curve.calculate_function_value(i)
        beta = service_curve.calculate_function_value(i)

        if alpha >= beta:
            A.append(i)

    ta = max(A)

    gamma = arrival_curve.get_used_gamma(ta)

    rx = gamma.rate
    bx = gamma.burst
    R = service_curve.rate
    T = service_curve.latency

    return (bx + R * T) / (R - rx)


def max_length_backlogged_period(arrival_curve: PiecewiseLinearArrivalCurve,
                                 service_curve: PiecewiseLinearServiceCurve):
    A = []
    C = []
    for i in arrival_curve.intersections:
        alpha = arrival_curve.calculate_function_value(i)
        beta = service_curve.calculate_function_value(i)

        if alpha >= beta:
            A.append(i)

    for j in service_curve.intersections:
        alpha = arrival_curve.calculate_function_value(j)
        beta = service_curve.calculate_function_value(j)

        if alpha >= beta:
            C.append(j)

    ta = max(A)
    uc = max(C)

    gamma = arrival_curve.get_used_gamma(ta)
    rho = service_curve.get_used_rho(uc)

    rx = gamma.rate
    bx = gamma.burst
    Ry = rho.rate
    Ty = rho.latency

    return (bx + Ry * Ty) / (Ry - rx)
