from abc import abstractmethod, ABC


class ArrivalCurve(ABC):
    """
    Abstract Arrival Curve class
    """

    @abstractmethod
    def calculate_function_value(self, t: float) -> float:
        pass

    @abstractmethod
    def get_initial_burst(self) -> float:
        pass

    @abstractmethod
    def get_used_gamma(self, t: float):
        pass
