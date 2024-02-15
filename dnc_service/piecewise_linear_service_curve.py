from dnc_service.service_curve import ServiceCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve

from typing import List


class PiecewiseLinearServiceCurve(ServiceCurve):
    def __init__(self, pieces: List[RateLatencyServiceCurve]):
        """
        It is necessary to provide the RateLatencyServiceCurve in normal form.

        :param pieces: list of RateLatencyServiceCurve (in normal form)
        """
        self.pieces = pieces
        self.intersections = self.__get_list_of_all_intersections()

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the service curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        if t <= self.pieces[0].latency:
            return 0
        else:
            f_t_max = float('-inf')
            for piece in self.pieces:
                R = piece.rate
                T = piece.latency
                f_t = R * (t - T)
                if f_t > f_t_max:
                    f_t_max = f_t
            return f_t_max

    def __get_list_of_all_intersections(self):
        intersections = []
        for x in range(0, len(self.pieces) - 1):
            rl1 = self.pieces[x]
            R1 = rl1.rate
            T1 = rl1.latency
            rl2 = self.pieces[x + 1]
            R2 = rl2.rate
            T2 = rl2.latency
            intersections.append((R1 * T1 - R2 * T2) / (R1 - R2))

        return intersections
