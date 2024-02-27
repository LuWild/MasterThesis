from abc import abstractmethod, ABC


class ServiceCurve(ABC):
    """
    Abstract Service Curve class
    """

    @abstractmethod
    def calculate_function_value(self, t: float) -> float:
        pass

    @abstractmethod
    def print_all_information(self):
        pass
