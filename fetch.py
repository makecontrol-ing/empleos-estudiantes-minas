"""Recolecta ofertas de todas las fuentes activas, marca las aptas para
estudiantes y las guarda en la base de datos.

Uso:
    python fetch.py
"""
import sys

from dotenv import load_dotenv

import config
import db

# La consola de Windows usa cp1252 por defecto y no imprime símbolos como "→".
# Forzamos UTF-8 para que los mensajes salgan bien.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from sources.arbeitnow import ArbeitnowConnector
from sources.jooble import JoobleConnector
from sources.unal_minas import UnalMinasConnector
from student_filter import es_para_estudiante

load_dotenv()  # carga JOOBLE_API_KEY desde el archivo .env si existe

CONECTORES = {
    "arbeitnow": ArbeitnowConnector,
    "jooble": JoobleConnector,
    "unal_minas": UnalMinasConnector,
}


def recolectar() -> None:
    db.init_db()
    activos = [cls() for nombre, cls in CONECTORES.items() if config.FUENTES.get(nombre)]

    total_crudo = 0
    total_estudiante = 0
    nuevas = 0

    for conector in activos:
        print(f"→ Consultando fuente: {conector.name}")
        try:
            ofertas = conector.fetch()
        except Exception as e:  # una fuente caída no debe tumbar el resto
            print(f"  [{conector.name}] Falló: {e}")
            continue

        for job in ofertas:
            job.is_student = es_para_estudiante(job)
        aptas = [j for j in ofertas if j.is_student]

        total_crudo += len(ofertas)
        total_estudiante += len(aptas)
        nuevas += db.upsert_jobs(ofertas)
        print(f"  {len(ofertas)} ofertas revisadas, {len(aptas)} aptas para estudiantes")

    s = db.stats()
    print("\n--- Resumen ---")
    print(f"Ofertas revisadas en esta corrida: {total_crudo}")
    print(f"Aptas para estudiantes (esta corrida): {total_estudiante}")
    print(f"Nuevas guardadas: {nuevas}")
    print(f"Total en base de datos: {s['total']} ({s['estudiantes']} para estudiantes)")


if __name__ == "__main__":
    recolectar()
