from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve


def deconvolution_n2(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    """
    Calculates the deconvolution of a PiecewiseLinearArrivalCurve (n=2) and a RateLatencyServiceCurve for
    the given value t.

    :param arrival_curve: PiecewiseLinearArrivalCurve
    :param service_curve: RateLatencyServiceCurve
    :param t: value t
    :return: deconvolution of PiecewiseLinearArrivalCurve and RateLatencyServiceCurve of t
    """

    R = service_curve.rate
    T = service_curve.latency

    r1 = arrival_curve.gammas[0].rate
    b1 = arrival_curve.gammas[0].burst

    r2 = arrival_curve.gammas[1].rate
    b2 = arrival_curve.gammas[1].burst

    t1 = arrival_curve.intersections[0]

    if t <= (t1 - T):
        if r1 <= R:
            if t <= -T:
                # print("Used Case: Iaa")
                return R * (t + T) + b1
            else:
                # print("Used Case: Iab")
                return r1 * (t + T) + b1
        else:
            # print("Used Case: Ib")
            return R * (t + T - t1) + b2 + r2 * t1
    else:
        # print("Used Case: II")
        return r2 * (t + T) + b2


def deconvolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    R = service_curve.rate
    T = service_curve.latency

    ta_and_gamma = arrival_curve.calculate_intersection_t_a_and_gamma_a(R=R)
    ta = ta_and_gamma[0]
    ra = ta_and_gamma[1].rate
    ba = ta_and_gamma[1].burst

    if t <= ta - T:
        return R * (t + T - ta) + ba + ra * ta
    else:
        return arrival_curve.calculate_function_value(t=t + T)


def deconvolution_test(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                       t: float):
    gammas = arrival_curve.gammas
    rhos = service_curve.rhos

    ac_intersections = arrival_curve.intersections
    sc_intersections = service_curve.intersections


