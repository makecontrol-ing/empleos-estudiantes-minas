import re
from html import unescape
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

import config
from models import Job
from sources.base import Connector

BASE = "https://medellin.unal.edu.co/estudiantes/convocatorias_estudiantes/"
LISTADO = BASE + "Home.php?tipo=Llamado+a+Convocatorias"
UA = {
    "User-Agent": "PlataformaEmpleosEstudiantes/0.1 "
                  "(proyecto academico; contacto: andresdgqceo@gmail.com)"
}


def _limpiar_titulo(nombre: str) -> str:
    t = nombre.strip()
    if t.lower().endswith(".pdf"):
        t = t[:-4]
    t = re.sub(r"\s+", " ", t.replace("_", " ")).strip()
    t = re.sub(r"\bConv\b", "Convocatoria", t)
    t = re.sub(r"\bEst(?:ud(?:iante)?)?\.? Aux(?:iliar)?\b", "Estudiante Auxiliar", t)
    t = re.sub(r"\s+\d+$", "", t)
    return t


class UnalMinasConnector(Connector):
    name = "unal_minas"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(UA)

    def _get(self, url: str) -> str:
        r = self.session.get(url, timeout=25)
        r.raise_for_status()
        return r.text

    def _carpetas(self) -> list[tuple[str, str]]:
        soup = BeautifulSoup(self._get(LISTADO), "html.parser")
        filtro = {u.upper() for u in config.UNAL_UNIDADES} if config.UNAL_UNIDADES else None
        carpetas = []
        for tr in soup.select("tr"):
            a = tr.find("a", href=re.compile("Mostrarcarpeta"))
            tds = tr.find_all("td")
            if not a or len(tds) < 4:
                continue
            unidad = tds[2].get_text(strip=True)
            if filtro and unidad.upper() not in filtro:
                continue
            folder_url = urljoin(BASE, quote(unescape(a["href"]), safe="=&?:/;"))
            carpetas.append((unidad, folder_url))
        return carpetas

    def _convocatorias(self, unidad: str, folder_url: str) -> list[Job]:
        soup = BeautifulSoup(self._get(folder_url), "html.parser")
        jobs: list[Job] = []
        for tr in soup.select("tr"):
            a = tr.find("a", href=True)
            tds = tr.find_all("td")
            if not a or len(tds) < 2:
                continue
            nombre = a.get_text(strip=True)
            if not nombre.lower().endswith(".pdf"):
                continue
            fecha = tds[1].get_text(strip=True)[:10]
            url = urljoin(BASE, quote(unescape(a["href"]), safe="=&?:/;.,"))
            jobs.append(
                Job(
                    source=self.name,
                    title=_limpiar_titulo(nombre),
                    company=f"UNAL · {unidad.title()}",
                    location="Medellín",
                    url=url,
                    description=(
                        f"Convocatoria de Estudiante Auxiliar de la Universidad "
                        f"Nacional ({unidad.title()}). Documento: {nombre}"
                    ),
                    employment_type="Estudiante Auxiliar / Monitoría",
                    posted_at=fecha,
                    is_student=True,
                )
            )
            if len(jobs) >= config.UNAL_MAX:
                break
        return jobs

    def fetch(self) -> list[Job]:
        jobs: list[Job] = []
        try:
            carpetas = self._carpetas()
        except requests.RequestException as e:
            print(f"  [unal_minas] No se pudo leer el listado: {e}")
            return jobs
        for unidad, folder_url in carpetas:
            try:
                jobs.extend(self._convocatorias(unidad, folder_url))
            except requests.RequestException as e:
                print(f"  [unal_minas] Error en carpeta {unidad}: {e}")
        return jobs
