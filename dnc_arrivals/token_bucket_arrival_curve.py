from dnc_arrivals.arrival_curve import ArrivalCurve


class TokenBucketArrivalCurve(ArrivalCurve):
    def __init__(self, rate: float, burst: float, shift=0):
        self.rate = rate
        self.burst = burst
        self.shift = shift

    def calculate_function_value(self, t: float) -> float:
        """
        Calculates f(t) for the arrival curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        if t <= self.shift:
            return 0
        else:
            return self.rate * (t - self.shift) + self.burst

    def get_initial_burst(self) -> float:
        return self.burst

    def get_used_gamma(self, t: float):
        return self

    def get_shift(self) -> float:
        return self.shift

    def get_gammas(self):
        return self

    def print_all_information(self):
        print("TokenBucketArrivalCurve Information (Object ID: " + str(id(self)) + "):")
        print("rate = " + str(self.rate) + " ; burst = " + str(self.burst))

