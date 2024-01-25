import calculator


class RateLatencyServiceCurve:
    def __init__(self, rate: float, latency: float):
        self.rate = rate
        self.latency = latency

    def calculate_function_value(self, t: float):
        """
        Calculates f(t) for the service curve object.

        :param t: value t for which f(t) is calculated
        :return: the calculated value f(t) for the given t
        """
        return calculator.rate_latency_function(R=self.rate, T=self.latency, values=[t])[0]
