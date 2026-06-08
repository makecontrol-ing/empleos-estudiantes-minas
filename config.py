CIUDAD = "Medellín"
PAIS = "Colombia"

BUSQUEDAS_ESTUDIANTE = [
    "aprendiz",
    "practicante",
    "pasante",
    "contrato de aprendizaje",
    "prácticas profesionales",
    "medio tiempo",
]

PALABRAS_ESTUDIANTE = [
    "aprendiz", "aprendizaje", "practicante", "práctica", "practica",
    "pasant", "becario", "beca", "medio tiempo", "media jornada",
    "tiempo parcial", "estudiante", "sin experiencia", "auxiliar",
    "junior", "trainee", "primer empleo",
    "intern", "internship", "working student", "entry level", "entry-level",
    "werkstudent", "praktikum", "praktikant",
]

PALABRAS_EXCLUIR = [
    "senior", "sr.", "líder", "lider", "lead", "jefe",
    "gerente", "director", "manager", "head of",
]

FUENTES = {
    "arbeitnow": True,
    "jooble": True,
    "unal_minas": True,
}

UNAL_UNIDADES = ["MINAS"]
UNAL_MAX = 40

FUENTES_SOLO_ESTUDIANTE = {"unal_minas"}

FUENTES_EMBED = ["unal_minas", "jooble"]

JOOBLE_HOST = "https://co.jooble.org"

DB_PATH = "empleos.db"
