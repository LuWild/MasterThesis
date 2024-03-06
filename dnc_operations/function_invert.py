from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve


def invert_token_bucket_arrival_curve(arrival_curve: TokenBucketArrivalCurve) -> RateLatencyServiceCurve:
    r = arrival_curve.rate
    b = arrival_curve.burst

    R = 1 / r
    T = b

    return RateLatencyServiceCurve(rate=R, latency=T)


def invert_piecewise_linear_arrival_curve(arrival_curve: PiecewiseLinearArrivalCurve) -> PiecewiseLinearServiceCurve:

    betas = []
    for gamma in arrival_curve.gammas:
        betas.append(invert_token_bucket_arrival_curve(gamma))

    return PiecewiseLinearServiceCurve(rhos=betas)


def invert_rate_latency_service_curve(service_curve: RateLatencyServiceCurve) -> TokenBucketArrivalCurve:
    R = service_curve.rate
    T = service_curve.latency

    r = 1 / R
    b = T

    return TokenBucketArrivalCurve(rate=r, burst=b)


def invert_piecewise_linear_service_curve(service_curve: PiecewiseLinearServiceCurve) -> PiecewiseLinearArrivalCurve:

    gammas = []
    for beta in service_curve.rhos:
        gammas.append(invert_rate_latency_service_curve(beta))

    return PiecewiseLinearArrivalCurve(gammas=gammas)
