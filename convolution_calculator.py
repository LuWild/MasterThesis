from arrival_curves import *
from services_curves import *


def convolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    T = service_curve.latency

    if t <= T:
        return 0
    else:
        return min(arrival_curve.calculate_function_value(t - T), service_curve.calculate_function_value(t))

