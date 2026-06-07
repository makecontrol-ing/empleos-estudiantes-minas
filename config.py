"""Configuración central de la plataforma.

Aquí cambias el comportamiento sin tocar el resto del código:
- la ciudad/país,
- los términos con los que se busca en las fuentes,
- las palabras que definen "empleo para estudiante",
- qué fuentes están activas.
"""

# Ciudad / país objetivo (Colombia)
CIUDAD = "Medellín"
PAIS = "Colombia"

# Términos con los que se busca en fuentes que aceptan búsqueda (ej. Jooble).
# Están pensados para empleo estudiantil en Colombia.
BUSQUEDAS_ESTUDIANTE = [
    "aprendiz",
    "practicante",
    "pasante",
    "contrato de aprendizaje",
    "prácticas profesionales",
    "medio tiempo",
]

# Palabras que indican que una oferta SÍ sirve para estudiantes.
PALABRAS_ESTUDIANTE = [
    # Español (Colombia)
    "aprendiz", "aprendizaje", "practicante", "práctica", "practica",
    "pasant", "becario", "beca", "medio tiempo", "media jornada",
    "tiempo parcial", "estudiante", "sin experiencia", "auxiliar",
    "junior", "trainee", "primer empleo",
    # Inglés / alemán (fuentes internacionales como Arbeitnow)
    "intern", "internship", "working student", "entry level", "entry-level",
    "werkstudent", "praktikum", "praktikant",
]

# Palabras en el TÍTULO que indican que NO es para estudiantes (roles senior).
PALABRAS_EXCLUIR = [
    "senior", "sr.", "líder", "lider", "lead", "jefe",
    "gerente", "director", "manager", "head of",
]

# Fuentes activas. Pon en False para desactivar una.
FUENTES = {
    "arbeitnow": True,    # gratis, SIN API key (empleos remotos / Europa)
    "jooble": True,       # ON: key de Colombia (usa el host co.jooble.org)
    "unal_minas": True,   # convocatorias UNAL (estudiante auxiliar / monitorías)
}

# --- Fuente UNAL (Facultad de Minas) ---
# Dependencias a incluir de las convocatorias de la sede. [] = todas.
UNAL_UNIDADES = ["MINAS"]
# Máximo de convocatorias (más recientes) por dependencia.
UNAL_MAX = 40

# Fuentes cuyas ofertas SIEMPRE son para estudiantes
# (no pasan por el filtro de palabras clave).
FUENTES_SOLO_ESTUDIANTE = {"unal_minas"}

# Fuentes que se muestran en el apartado PÚBLICO (widget / bloque / iframe)
# que va en la página de Bienestar. El tablero interno (/) sigue mostrando todo.
FUENTES_EMBED = ["unal_minas", "jooble"]

# Host de Jooble según el país de tu API key.
# Colombia: https://co.jooble.org  ·  Internacional/EE.UU.: https://jooble.org
JOOBLE_HOST = "https://co.jooble.org"

# Archivo de base de datos (SQLite, se crea solo)
DB_PATH = "empleos.db"
