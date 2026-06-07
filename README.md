# 🎓 Plataforma de empleos para estudiantes — Medellín / Colombia

Recolecta ofertas de empleo de varias fuentes, **filtra las aptas para estudiantes
universitarios** (prácticas, contrato de aprendizaje SENA, medio tiempo, primer empleo)
y las muestra en una lista web.

## Cómo funciona (de un vistazo)

```
[Fuentes / APIs] → [Normalizador] → [Filtro estudiante] → [SQLite] → [Web Flask]
   arbeitnow          models.py        student_filter.py    db.py      app.py
   jooble
```

- **Arbeitnow** — API gratis y **sin API key**. Funciona de inmediato (empleos remotos).
- **Jooble** — API gratis que **cubre Colombia**. Necesita una key (1 min de registro).

## Puesta en marcha (Windows / PowerShell)

```powershell
# 1. Crear entorno virtual e instalar dependencias
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. (Opcional pero recomendado) activar Jooble para empleos de Colombia
#    - Regístrate gratis en https://jooble.org/api/about y copia tu key
copy .env.example .env
#    - Abre .env y pega:  JOOBLE_API_KEY=tu_key

# 3. Recolectar empleos
python fetch.py

# 4. Ver la web
python app.py
# abre http://127.0.0.1:5000
```

> Sin la key de Jooble igual funciona: usará solo Arbeitnow. Con la key, verás
> ofertas reales de Medellín (aprendiz SENA, practicante, etc.).

## Estructura

| Archivo | Qué hace |
|---|---|
| `config.py` | Ciudad, palabras clave de estudiante y fuentes activas. **Empieza por aquí.** |
| `models.py` | Formato único de una oferta (`Job`). |
| `sources/` | Un archivo por fuente. Para agregar una nueva, copia `arbeitnow.py`. |
| `student_filter.py` | Decide si una oferta sirve para estudiantes. |
| `db.py` | Guarda y consulta en SQLite (evita duplicados). |
| `fetch.py` | Orquesta: recolecta → filtra → guarda. |
| `app.py` | Web para ver la lista. |

## Cómo crecer (siguientes pasos)

1. **Más fuentes**: agregar más APIs/feeds en `sources/`.
2. **Mejor filtro**: clasificar con IA en vez de solo palabras clave.
3. **Automatizar**: correr `fetch.py` cada X horas (Programador de tareas de Windows o GitHub Actions).
4. **Más features**: filtros por carrera/ciudad, guardar favoritos, alertas por correo.
5. **Escalar**: cambiar SQLite por PostgreSQL y desplegar la web.

## ⚖️ Nota legal importante

Este proyecto usa **APIs oficiales** (Arbeitnow, Jooble), que están pensadas para esto.

Los portales grandes de Colombia (El Empleo, Computrabajo, Magneto, Indeed, LinkedIn)
**no tienen API pública** y su scraping directo suele **violar sus Términos de Servicio**
y tiene anti-bots. Si más adelante quieres añadirlos, revisa sus términos y su
`robots.txt`, identifícate y usa límites de velocidad razonables.
