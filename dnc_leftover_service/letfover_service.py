from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from dnc_operations.arrival_curve_shift import token_bucket_arrival_curve_shift
from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift

from dnc_operations.max_length_backlogged_period import max_length_backlogged_period

from typing import List


def FIFO_leftover_service_basic(cross_flow: TokenBucketArrivalCurve, service_curve: RateLatencyServiceCurve, theta=0.0):
    R = service_curve.rate
    T = service_curve.latency

    r = cross_flow.rate
    b = cross_flow.burst

    new_R = R - r
    new_T = (b + R * T - r * theta) / (R - r)

    return RateLatencyServiceCurve(rate=new_R, latency=new_T)


def FIFO_leftover_service_pwl(cross_flow: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                              theta=0.0):
    print("Starting FIFO Leftover Service calculation (PWL)...")
    # alpha(t-theta) -> shifted_alpha(t)
    cross_flow_shifted_by_theta = piecewise_linear_arrival_curve_shift(arrival_curve=cross_flow, t_shift=-theta)

    # []^+: beta(t) >= shifted_alpha(t) at t = max_backlogged_period
    # --> check sections of beta and the respective sections of shifted_alpha and use FIFO_leftover_service_basic for
    # each section pair (beta_{R,T} and gamma)

    max_bp = max_length_backlogged_period(arrival_curve=cross_flow_shifted_by_theta, service_curve=service_curve)
    print("Max length of backlogged period: " + str(max_bp))

    print("Min Latency Theta: " +
          str(get_optimal_theta_for_min_latency(service_curve=service_curve, cross_flow=cross_flow)))

    relevant_sections_sc = get_relevant_sections_greater_t(input_curve=service_curve, t=max_bp)

    relevant_sections_ac = get_relevant_sections_greater_t(input_curve=cross_flow_shifted_by_theta, t=max_bp)

    # match relevant sections sc with relevant sections ac to use FIFO_leftover_service_basic for each section pair
    leftover_service_pwl = []

    if len(relevant_sections_sc) >= 1 and len(relevant_sections_ac) == 1:
        # get initial pair at max_bp:
        leftover_service_pwl = [
            FIFO_leftover_service_basic(cross_flow=relevant_sections_ac[0], service_curve=relevant_sections_sc[0])]

        print("First relevant sections:")
        relevant_sections_ac[0].print_all_information()
        relevant_sections_sc[0].print_all_information()

        # check if it is 0 till max_bp: so T >= max_bp
        if leftover_service_pwl[0].latency < max_bp:
            leftover_service_pwl[0].latency = max_bp

    if len(relevant_sections_sc) >= 1 and len(relevant_sections_ac) > 1:
        first_section = True
        for sc_section in relevant_sections_sc:
            # get interval for the sc_section
            sc_interval_bounds = get_sc_section_interval_bounds(service_curve=service_curve, section=sc_section)
            # get sections and bounds for the ac_sections inside the interval bounds of the sc_section
            ac_sections_with_interval_bounds = \
                get_ac_sections_inside_sc_section_interval_bounds(sc_interval_bounds=sc_interval_bounds,
                                                                  arrival_curve=cross_flow_shifted_by_theta,
                                                                  ac_sections=relevant_sections_ac)

            for ac_section_with_interval_bounds in ac_sections_with_interval_bounds:
                ac_section = ac_section_with_interval_bounds[0]
                ac_interval_bounds = ac_section_with_interval_bounds[1]
                leftover_service_pwl.append(
                    FIFO_leftover_service_basic(cross_flow=ac_section, service_curve=sc_section))
                if first_section:

                    if leftover_service_pwl[0].latency < max_bp:
                        leftover_service_pwl[0].latency = max_bp

                    first_section = False

    return PiecewiseLinearServiceCurve(rhos=leftover_service_pwl)

    # 1_{t>theta}: t<=theta = 0: jump only at this position possible


def get_optimal_theta_for_min_backlog_bound(service_curve: PiecewiseLinearServiceCurve,
                                            cross_flow: PiecewiseLinearArrivalCurve):
    min_theta = float('inf')
    for rho in service_curve.rhos:
        for gamma in cross_flow.gammas:
            theta = (gamma.burst / rho.rate) + rho.latency
            if min_theta > theta:
                min_theta = theta

    return min_theta


def get_optimal_theta_for_min_latency(service_curve: PiecewiseLinearServiceCurve,
                                      cross_flow: PiecewiseLinearArrivalCurve):
    min_theta = float('inf')
    used_rho = None
    for rho in service_curve.rhos:
        gamma = cross_flow.gammas[0]
        theta = (gamma.burst / rho.rate) + rho.latency
        if min_theta > theta:
            used_rho = rho
            min_theta = theta

    print("Used Rho:")
    used_rho.print_all_information()
    return min_theta


def get_ac_sections_inside_sc_section_interval_bounds(sc_interval_bounds: List[float],
                                                      arrival_curve: PiecewiseLinearArrivalCurve,
                                                      ac_sections: List[TokenBucketArrivalCurve]):
    result = []
    for ac_section in ac_sections:
        ac_interval_bounds = get_ac_section_interval_bounds(arrival_curve=arrival_curve, section=ac_section)
        if ac_interval_bounds[0] < sc_interval_bounds[0] and ac_interval_bounds[1] <= sc_interval_bounds[1]:
            result.append([ac_section, [sc_interval_bounds[0], ac_interval_bounds[1]]])
        if ac_interval_bounds[0] >= sc_interval_bounds[0] and ac_interval_bounds[1] <= sc_interval_bounds[1]:
            result.append([ac_section, [ac_interval_bounds[0], ac_interval_bounds[1]]])
        if ac_interval_bounds[0] >= sc_interval_bounds[0] and ac_interval_bounds[1] > sc_interval_bounds[1]:
            result.append([ac_section, [ac_interval_bounds[0], sc_interval_bounds[1]]])

    return result


def get_ac_section_interval_bounds(arrival_curve: PiecewiseLinearArrivalCurve, section: TokenBucketArrivalCurve):
    if arrival_curve.gammas[0] == section:
        return [0, arrival_curve.intersections[0]]
    # last:
    if arrival_curve.gammas[-1] == section:
        return [arrival_curve.intersections[-1], float('inf')]
    # in between:
    for i in range(1, len(arrival_curve.gammas) - 1):
        if arrival_curve.gammas[i] == section:
            return [arrival_curve.intersections[i - 1], arrival_curve.intersections[i]]


def get_sc_section_interval_bounds(service_curve: PiecewiseLinearServiceCurve, section: RateLatencyServiceCurve):
    if len(service_curve.rhos) == 1:
        service_curve.intersections = [service_curve.get_initial_latency()]
    # first:
    if service_curve.rhos[0] == section:
        return [0, service_curve.intersections[0]]
    # last:
    if service_curve.rhos[-1] == section:
        return [service_curve.intersections[-1], float('inf')]
    # in between:
    for i in range(1, len(service_curve.rhos) - 1):
        if service_curve.rhos[i] == section:
            return [service_curve.intersections[i - 1], service_curve.intersections[i]]


def get_relevant_sections_greater_t(input_curve, t: float):
    # Relevant sections are sections for t > max_bp

    relevant_intersections = input_curve.intersections

    relevant_intersections = \
        remove_intersections_before_time_t(intersections=relevant_intersections, t=t)

    if isinstance(input_curve, PiecewiseLinearServiceCurve):
        number_of_sections = len(input_curve.rhos)
    else:
        number_of_sections = len(input_curve.gammas)

    number_of_relevant_intersections = len(relevant_intersections)

    relevant_sections = []
    for i in range(number_of_sections - 1, number_of_sections - number_of_relevant_intersections - 2, -1):
        if isinstance(input_curve, PiecewiseLinearServiceCurve):
            relevant_sections.append(input_curve.rhos[i])
        else:
            relevant_sections.append(input_curve.gammas[i])
    relevant_sections.reverse()

    return relevant_sections


def remove_intersections_before_time_t(intersections: List[float], t: float):
    intersections_to_remove = []
    for intersection in intersections:
        if intersection < t:
            intersections_to_remove.append(intersection)

    return [intersection for intersection in intersections if intersection not in intersections_to_remove]


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=2.5, burst=2)
    tb2 = TokenBucketArrivalCurve(rate=1.1, burst=6)
    tb3 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    pwl_ac.print_all_information()

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=3)
    rl2 = RateLatencyServiceCurve(rate=1.5, latency=7)
    rl3 = RateLatencyServiceCurve(rate=2.5, latency=12)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
    pwl_sc.print_all_information()

    print("--------------")

    FIFO_leftover_service_pwl(cross_flow=pwl_ac, service_curve=pwl_sc)
