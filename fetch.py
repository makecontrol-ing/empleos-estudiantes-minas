import sys

from dotenv import load_dotenv

import config
import db
from sources.arbeitnow import ArbeitnowConnector
from sources.jooble import JoobleConnector
from sources.unal_minas import UnalMinasConnector
from student_filter import es_para_estudiante

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

load_dotenv()

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
        print(f"Consultando fuente: {conector.name}")
        try:
            ofertas = conector.fetch()
        except Exception as e:
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
