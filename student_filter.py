"""Decide si una oferta es apta para estudiantes universitarios.

MVP: reglas por palabras clave (rápido y barato). Más adelante se puede
reemplazar por un clasificador con IA sin tocar el resto del sistema.
"""
import config
from models import Job


def es_para_estudiante(job: Job) -> bool:
    # Algunas fuentes (ej. convocatorias UNAL) son por definición para estudiantes.
    if job.source in config.FUENTES_SOLO_ESTUDIANTE:
        return True

    titulo = job.title.lower()
    texto = f"{job.title} {job.description}".lower()

    # Si el título grita "senior/gerente/director/...", lo descartamos.
    if any(neg in titulo for neg in config.PALABRAS_EXCLUIR):
        return False

    # Si aparece alguna señal de empleo estudiantil, lo aceptamos.
    return any(pos in texto for pos in config.PALABRAS_ESTUDIANTE)
