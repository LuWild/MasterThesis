import copy

from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve


def piecewise_linear_arrival_curve_shift(arrival_curve: PiecewiseLinearArrivalCurve, t_shift: float):
    shifted_arrival_curve = copy.deepcopy(arrival_curve)

    new_gammas = []
    for gamma in arrival_curve.gammas:
        new_gammas.append(token_bucket_arrival_curve_shift(arrival_curve=gamma, t_shift=t_shift))

    gammas_to_delete = []
    for i in range(len(new_gammas)-1):
        if new_gammas[i].burst >= new_gammas[i+1].burst:
            gammas_to_delete.append(new_gammas[i])

    new_gammas = [i for i in new_gammas if i not in gammas_to_delete]

    shifted_arrival_curve.gammas = new_gammas
    shifted_arrival_curve.intersections = shifted_arrival_curve.calculate_list_of_all_intersections()

    return shifted_arrival_curve


def token_bucket_arrival_curve_shift(arrival_curve: TokenBucketArrivalCurve, t_shift: float):
    shifted_arrival_curve = copy.deepcopy(arrival_curve)

    shifted_arrival_curve.burst = arrival_curve.burst + arrival_curve.rate * t_shift

    return shifted_arrival_curve


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2, burst=2)
    tb2 = TokenBucketArrivalCurve(rate=1, burst=6)
    tb3 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    pwl_ac.print_all_information()

    ac_shifted = piecewise_linear_arrival_curve_shift(arrival_curve=pwl_ac, t_shift=10)
    ac_shifted.print_all_information()
