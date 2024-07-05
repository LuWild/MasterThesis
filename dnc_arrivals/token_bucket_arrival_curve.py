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
        """
        :return: initial burst
        """
        return self.burst

    def get_used_gamma(self, t: float):
        """
        :return: this TokenBucketArrivalCurve.
        """
        return self

    def set_shift(self, shift: float):
        """
        Set the shift of the TokenBucketArrivalCurve f(t-shift).

        :param shift: amount that is shifted.
        :return: shifts the TokenBucketArrivalCurve.
        """
        self.shift = shift

    def get_shift(self) -> float:
        """
        :return: amount that was shifted.
        """
        return self.shift

    def get_gammas(self):
        """
        :return: this TokenBucketArrivalCurve.
        """
        return self

    def print_all_information(self):
        """
        Prints all important information about this TokenBucketArrivalCurve.
        """
        print("TokenBucketArrivalCurve Information (Object ID: " + str(id(self)) + "):")
        print("rate = " + str(self.rate) + " ; burst = " + str(self.burst))

