"""Fuente Jooble: API REST gratuita que cubre Colombia.

Cómo activarla:
  1. Regístrate gratis en https://jooble.org/api/about
  2. Copia tu key en el archivo  .env  ->  JOOBLE_API_KEY=tu_key_aqui

Hace una búsqueda por cada término de config.BUSQUEDAS_ESTUDIANTE en la ciudad
configurada (config.CIUDAD) y junta los resultados sin duplicados.
"""
import os

import requests

import config
from models import Job
from sources.base import Connector


class JoobleConnector(Connector):
    name = "jooble"

    def __init__(self) -> None:
        self.api_key = os.getenv("JOOBLE_API_KEY", "").strip()

    def fetch(self) -> list[Job]:
        if not self.api_key:
            print("  [jooble] Sin JOOBLE_API_KEY: omitido. "
                  "Consíguela gratis en https://jooble.org/api/about")
            return []

        url = f"{config.JOOBLE_HOST}/api/{self.api_key}"
        vistos: set[str] = set()
        jobs: list[Job] = []

        for termino in config.BUSQUEDAS_ESTUDIANTE:
            try:
                resp = requests.post(
                    url,
                    json={"keywords": termino, "location": config.CIUDAD},
                    timeout=20,
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"  [jooble] Error buscando '{termino}': {e}")
                continue

            for item in resp.json().get("jobs", []):
                link = item.get("link", "")
                if not link or link in vistos:
                    continue
                vistos.add(link)
                jobs.append(
                    Job(
                        source=self.name,
                        title=(item.get("title") or "").strip(),
                        company=(item.get("company") or "").strip(),
                        location=(item.get("location") or "").strip(),
                        url=link,
                        description=item.get("snippet", ""),
                        salary=item.get("salary", ""),
                        employment_type=item.get("type", ""),
                        posted_at=item.get("updated", ""),
                    )
                )
        return jobs
