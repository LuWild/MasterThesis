from dnc_service.service_curve import ServiceCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve

from typing import List


class PiecewiseLinearServiceCurve(ServiceCurve):
    def __init__(self, rhos: List[RateLatencyServiceCurve], shift=0):
        """
        It is necessary to provide the PiecewiseLinearServiceCurve in normal form.

        :param rhos: list of RateLatencyServiceCurve (in normal form)
        """
        self.rhos = rhos
        self.shift = shift
        self.intersections = self.__get_list_of_all_intersections()

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the service curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        if t <= self.rhos[0].latency:
            return 0
        else:
            f_t_max = float('-inf')
            for piece in self.rhos:
                R = piece.rate
                T = piece.latency
                f_t = R * (t - T)
                if f_t > f_t_max:
                    f_t_max = f_t
            return f_t_max

    def get_initial_latency(self) -> float:
        """
        :return: initial latency
        """
        return self.rhos[0].latency

    def get_used_rho(self, t: float):
        """
        Returns the RateLatencyServiceCurve that is used to calculate f(t) in the segment for a given t

        :param t: value t
        :return: RateLatencyServiceCurve for the segment of the given t
        """
        number_of_intersections = len(self.intersections)
        for i in range(0, number_of_intersections):
            if t < self.intersections[i]:
                return self.rhos[i]
        return self.rhos[number_of_intersections]

    def set_shift(self, shift: float):
        """
        Set the shift of the PiecewiseLinearServiceCurve f(t-shift).

        :param shift: amount that is shifted.
        :return: shifts the PiecewiseLinearServiceCurve.
        """
        self.shift = shift
        self.intersections = self.__get_list_of_all_intersections()
        for rho in self.rhos:
            rho.latency += self.shift

    def print_all_information(self):
        """
        Prints all important information about this PiecewiseLinearServiceCurve.
        """
        print("PiecewiseLinearServiceCurve Information (Object ID: " + str(id(self)) + "):")
        for i in range(len(self.rhos)):
            rho = self.rhos[i]
            print("rho " + str(i + 1) + ": rate = " + str(rho.rate) + " ; latency = " + str(rho.latency))
        print("intersections: " + str(self.intersections))

    def __get_list_of_all_intersections(self):
        """
        Creating a list of all intersections of this PiecewiseLinearServiceCurve.

        :return: List of all intersections.
        """
        intersections = []
        for x in range(0, len(self.rhos) - 1):
            rl1 = self.rhos[x]
            R1 = rl1.rate
            T1 = rl1.latency
            rl2 = self.rhos[x + 1]
            R2 = rl2.rate
            T2 = rl2.latency
            intersections.append((R1 * T1 - R2 * T2) / (R1 - R2) + self.shift)

        return intersections
