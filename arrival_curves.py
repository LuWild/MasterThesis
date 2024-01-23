from typing import List


class TokenBucketArrivalCurve:
    def __init__(self, rate: float, burst: float):
        self.rate = rate
        self.burst = burst


class PiecewiseLinearArrivalCurve:
    def __init__(self, gammas: List[TokenBucketArrivalCurve]):
        """
        It is necessary to provide the TokenBucketArrivalCurves in normal form.

        :param gammas: list of TokenBucketArrivalCurves (in normal form)
        """
        self.gammas = gammas
        self.intersections = self.__get_list_of_all_intersections()

    def __get_list_of_all_intersections(self):
        intersections = []
        for x in range(0, len(self.gammas) - 1):
            tb1 = self.gammas[x]
            tb2 = self.gammas[x+1]
            intersections.append((tb2.burst - tb1.burst) / (tb1.rate - tb2.rate))

        return intersections
