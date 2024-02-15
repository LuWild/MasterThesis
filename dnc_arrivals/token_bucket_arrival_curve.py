from dnc_arrivals.arrival_curve import ArrivalCurve


class TokenBucketArrivalCurve(ArrivalCurve):
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
