from dnc_arrivals.arrival_curve import ArrivalCurve
from dnc_service.service_curve import ServiceCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve


def convolution(arrival_curve: ArrivalCurve, service_curve: ServiceCurve, t: float):
    convolution(arrival_curve=arrival_curve, service_curve=service_curve, t=t)


def convolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    T = service_curve.latency

    if t <= T:
        return 0
    else:
        return min(arrival_curve.calculate_function_value(t - T), service_curve.calculate_function_value(t))


def convolution(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve, t: float):
    T = service_curve.get_initial_latency()

    if t <= T:
        return 0
    else:
        return min(arrival_curve.calculate_function_value(t - T), service_curve.calculate_function_value(t))
