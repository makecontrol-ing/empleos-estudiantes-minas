from abc import ABC, abstractmethod

from models import Job


class Connector(ABC):
    name: str = "base"

    @abstractmethod
    def fetch(self) -> list[Job]:
        raise NotImplementedError
