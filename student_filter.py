import config
from models import Job


def es_para_estudiante(job: Job) -> bool:
    if job.source in config.FUENTES_SOLO_ESTUDIANTE:
        return True

    titulo = job.title.lower()
    texto = f"{job.title} {job.description}".lower()

    if any(neg in titulo for neg in config.PALABRAS_EXCLUIR):
        return False

    return any(pos in texto for pos in config.PALABRAS_ESTUDIANTE)
