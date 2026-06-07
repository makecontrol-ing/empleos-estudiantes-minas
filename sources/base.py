"""Interfaz común para todas las fuentes de empleo.

Para agregar una fuente nueva: crea un archivo en `sources/` con una clase
que herede de `Connector` e implemente `fetch()` devolviendo una lista de Job.
"""
from abc import ABC, abstractmethod

from models import Job


class Connector(ABC):
    name: str = "base"

    @abstractmethod
    def fetch(self) -> list[Job]:
        """Devuelve una lista de ofertas normalizadas (objetos Job)."""
        raise NotImplementedError
