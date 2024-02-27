from dnc_arrivals.arrival_curve import ArrivalCurve
from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve

from typing import List


class PiecewiseLinearArrivalCurve(ArrivalCurve):
    def __init__(self, gammas: List[TokenBucketArrivalCurve]):
        """
        It is necessary to provide the TokenBucketArrivalCurves in normal form.

        :param gammas: list of TokenBucketArrivalCurves (in normal form)
        """
        self.gammas = gammas
        self.intersections = self.calculate_list_of_all_intersections()

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the arrival curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        if t <= 0:
            return 0
        else:
            f_t_min = float('inf')
            for gamma in self.gammas:
                r = gamma.rate
                b = gamma.burst
                f_t = r * t + b
                if f_t < f_t_min:
                    f_t_min = f_t
            return f_t_min

    def get_initial_burst(self) -> float:
        return self.gammas[0].burst

    def get_used_gamma(self, t: float):
        """
        Returns the TokenBucketArrivalCurve that is used to calculate f(t) in the segment for a given t

        :param t: value t
        :return: TokenBucketArrivalCurve for the segment of the given t
        """
        number_of_intersections = len(self.intersections)
        for i in range(0, number_of_intersections):
            if t < self.intersections[i]:
                return self.gammas[i]
        return self.gammas[number_of_intersections]

    def get_used_gamma_number(self, t: float):
        """
        Returns the number of the TokenBucketArrivalCurve that is used to calculate f(t) in the segment for a given t

        :param t: value t
        :return: the number of the TokenBucketArrivalCurve for the segment of the given t
        """
        gamma_used = self.get_used_gamma(t)
        for i in range(0, len(self.gammas)):
            if self.gammas[i].rate == gamma_used.rate and self.gammas[i].burst == gamma_used.burst:
                return i + 1

    def calculate_intersection_t_a_and_gamma_a(self, R):
        """
        Get the intersection point ta for which the following holds:
        ra-1 > R and ra <= R

        This "ta" has to exist since the s.c. must hold.

        :param R: Rate R of a Rate-Latency Server
        :return: [ta, TokenBucketArrivalCurve]
        """

        for x in range(0, len(self.gammas) - 1):
            tb1 = self.gammas[x]
            tb2 = self.gammas[x + 1]

            if tb1.rate >= R > tb2.rate:
                return [(tb2.burst - tb1.burst) / (tb1.rate - tb2.rate), tb2]
            else:
                return [0, tb1]

    def print_all_information(self):
        print("PiecewiseLinearArrivalCurve Information (" + str(self) + "):")
        for i in range(len(self.gammas)):
            gamma = self.gammas[i]
            print("gamma " + str(i+1) + ": rate = " + str(gamma.rate) + " ; burst = " + str(gamma.burst))
        print("intersections: " + str(self.intersections))

    def calculate_list_of_all_intersections(self):
        intersections = []
        for x in range(0, len(self.gammas) - 1):
            tb1 = self.gammas[x]
            tb2 = self.gammas[x + 1]
            intersections.append((tb2.burst - tb1.burst) / (tb1.rate - tb2.rate))

        return intersections
