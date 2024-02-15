from abc import abstractmethod, ABC


class ArrivalCurve(ABC):
    """
    Abstract Arrival Curve class
    """

    @abstractmethod
    def calculate_function_value(self, t: float) -> float:
        pass
