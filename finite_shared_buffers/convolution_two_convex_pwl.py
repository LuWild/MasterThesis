from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from typing import List


def create_convolution(service_curve1: PiecewiseLinearServiceCurve, service_curve2: PiecewiseLinearServiceCurve):
    if service_curve1 != service_curve2:
        new_initial_latency = service_curve1.get_initial_latency() + service_curve2.get_initial_latency()

        rate_and_length_of_sections_sc1 = get_rate_and_length_of_linear_sections(service_curve=service_curve1)

        rate_and_length_of_sections_sc2 = get_rate_and_length_of_linear_sections(service_curve=service_curve2)

        rate_and_length_of_sections_sorted = sorted(rate_and_length_of_sections_sc1 + rate_and_length_of_sections_sc2,
                                                    key=lambda x: x[0])
        rate_and_length_of_sections_sorted.pop()

        intervals_for_new_sections = get_intervals_for_new_sections(rate_and_length_of_sections_sorted,
                                                                    initial_latency=new_initial_latency)

        for_pwl_creation = create_rl_service_curves(rate_and_length_of_sections_sorted=rate_and_length_of_sections_sorted,
                                                    intervals_for_new_sections=intervals_for_new_sections)

        convolution = PiecewiseLinearServiceCurve(for_pwl_creation)
    else:
        convolution = get_self_convolution()

    return convolution


def get_self_convolution():
    # TODO
    print("This Case is TODO.")


def get_rate_and_length_of_linear_sections(service_curve: PiecewiseLinearServiceCurve):
    result = []
    intersection_list = service_curve.intersections
    intersection_list.insert(0, service_curve.get_initial_latency())
    intersection_list.append(float('inf'))
    for i in range(0, len(service_curve.rhos)):
        result.append([service_curve.rhos[i].rate, intersection_list[i + 1] - intersection_list[i]])

    return result


def get_intervals_for_new_sections(rate_and_length_of_sections_sorted: List[List[float]], initial_latency: float):
    result = []
    last_max = -1
    first = True
    for rate_and_length in rate_and_length_of_sections_sorted:
        if first:
            result.append([initial_latency, rate_and_length[1] + initial_latency])
            last_max = rate_and_length[1] + initial_latency
            first = False
        else:
            result.append([last_max, rate_and_length[1] + last_max])
            last_max += rate_and_length[1]

    return result


def create_rl_service_curves(rate_and_length_of_sections_sorted: List[List[float]],
                             intervals_for_new_sections: List[List[float]]):
    first = True
    result = []
    y = -1
    for i in range(0, len(rate_and_length_of_sections_sorted)):
        rate = rate_and_length_of_sections_sorted[i][0]
        if first:
            first_section = RateLatencyServiceCurve(rate=rate, latency=intervals_for_new_sections[i][0])
            result.append(first_section)
            y = rate * rate_and_length_of_sections_sorted[i][1]
            first = False
        else:
            if i == len(rate_and_length_of_sections_sorted) - 1:
                section = RateLatencyServiceCurve(rate=rate, latency=(intervals_for_new_sections[i][0] - (y / rate)))
                result.append(section)
            else:
                y = y + rate * rate_and_length_of_sections_sorted[i][1]
                section = RateLatencyServiceCurve(rate=rate, latency=(intervals_for_new_sections[i][1] - (y / rate)))
                result.append(section)

    return result


if __name__ == '__main__':
    rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
    rl2 = RateLatencyServiceCurve(rate=1.25, latency=4)
    pwl_sc1 = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])
    pwl_sc1.print_all_information()

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=1)
    rl2 = RateLatencyServiceCurve(rate=2.5, latency=7)
    pwl_sc2 = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])
    pwl_sc2.print_all_information()

    test = create_convolution(service_curve1=pwl_sc1, service_curve2=pwl_sc2)
    create_convolution(service_curve1=test, service_curve2=test).print_all_information()



