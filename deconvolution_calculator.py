from arrival_curves import *
from services_curves import *


def deconvolution_n2(pwl: PiecewiseLinearArrivalCurve, sc: RateLatencyServiceCurve, t: float):
    """
    Calculates the deconvolution of a PiecewiseLinearArrivalCurve (n=2) and a RateLatencyServiceCurve for
    the given value t.

    :param pwl: PiecewiseLinearArrivalCurve
    :param sc: RateLatencyServiceCurve
    :param t: value t
    :return: deconvolution of pwl and sc of t
    """

    R = sc.rate
    T = sc.latency

    r1 = pwl.gammas[0].rate
    b1 = pwl.gammas[0].burst

    r2 = pwl.gammas[1].rate
    b2 = pwl.gammas[1].burst

    t1 = pwl.intersections[0]

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
