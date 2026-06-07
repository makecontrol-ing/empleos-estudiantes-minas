"""Modelo normalizado de una oferta de empleo.

Cada fuente devuelve los datos en su propio formato; aquí los unificamos
en un solo objeto `Job` para que el resto del sistema no dependa de la fuente.
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class Job:
    source: str                 # fuente: "jooble", "arbeitnow", ...
    title: str
    company: str
    location: str
    url: str
    description: str = ""
    salary: str = ""
    employment_type: str = ""
    posted_at: str = ""         # fecha original tal cual la da la fuente (texto)
    is_student: bool = False
    fetched_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    id: str = ""                # se calcula solo (sirve para evitar duplicados)

    def __post_init__(self) -> None:
        if not self.id:
            # Un id estable por (fuente + url) evita duplicados si luego
            # cambia el título. Si no hay url, caemos al título.
            base = f"{self.source}|{self.url or self.title}".lower()
            self.id = hashlib.sha1(base.encode("utf-8")).hexdigest()

    def to_row(self) -> dict:
        return asdict(self)
