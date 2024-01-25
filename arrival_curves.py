from typing import List


class TokenBucketArrivalCurve:
    def __init__(self, rate: float, burst: float):
        self.rate = rate
        self.burst = burst

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the arrival curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        if t <= 0:
            return 0
        else:
            return self.rate * t + self.burst


class PiecewiseLinearArrivalCurve:
    def __init__(self, gammas: List[TokenBucketArrivalCurve]):
        """
        It is necessary to provide the TokenBucketArrivalCurves in normal form.

        :param gammas: list of TokenBucketArrivalCurves (in normal form)
        """
        self.gammas = gammas
        self.intersections = self.__get_list_of_all_intersections()

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the arrival curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        import calculator
        if t <= 0:
            return 0
        else:
            return calculator.piecewise_linear_function(self, [t])[0]

    def get_used_gamma(self, t: float):
        """
        Returns the TokenBucketArrivalCurve that is used to calculate f(t) in the segment for a given t

        :param t: value t
        :return: TokenBucketArrivalCurve for the segment of the given t
        """
        number_of_intersections = len(self.intersections)
        for i in range(0, number_of_intersections):
            if t <= self.intersections[i]:
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


    def __get_list_of_all_intersections(self):
        intersections = []
        for x in range(0, len(self.gammas) - 1):
            tb1 = self.gammas[x]
            tb2 = self.gammas[x + 1]
            intersections.append((tb2.burst - tb1.burst) / (tb1.rate - tb2.rate))

        return intersections
