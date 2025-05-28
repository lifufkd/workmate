from abc import ABC, abstractmethod


class BaseReport(ABC):

    @abstractmethod
    def process_data(self, employees_data: list[dict]) -> dict:
        pass
