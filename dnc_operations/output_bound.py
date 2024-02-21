from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from deconvolution import deconvolution


def output_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    if t > 0:
        return deconvolution(arrival_curve=arrival_curve, service_curve=service_curve, t=t)
    else:
        return 0


def output_bound(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, t: float):
    pass
