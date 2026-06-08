#  Empleos para Estudiantes — Facultad de Minas (UNAL)

Plataforma que reúne en un solo lugar las oportunidades laborales para estudiantes de la
Facultad de Minas (Universidad Nacional de Colombia, sede Medellín): convocatorias de
**Estudiante Auxiliar / monitorías** de la Universidad y **prácticas, contrato de aprendizaje
y empleos de medio tiempo** en Medellín. Se actualiza sola y se muestra dentro de la página
de Bienestar.

**🔗 En vivo:** https://makecontrol-ing.github.io/empleos-estudiantes-minas/

---

## ¿Qué hace?

1. **Recolecta** ofertas de varias fuentes.
2. **Filtra** y deja solo lo apto para estudiantes.
3. **Guarda** las ofertas sin duplicados.
4. **Publica** un tablero (con buscador y filtros) que se incrusta en la página de Bienestar.
5. Un robot lo **actualiza solo** cada pocas horas.

## ¿Cómo funciona? (arquitectura)

```
Fuentes   →   Normalización   →   Filtro estudiante   →   Base de datos   →   Publicación
(APIs +       (un formato          (palabras clave)        (SQLite)            (JSON + widget)
 scraping)     común: Job)
```

| Pieza | Archivo | Qué hace |
|---|---|---|
| Configuración | `config.py` | Ciudad, palabras clave, fuentes activas, host de Jooble. |
| Modelo | `models.py` | Formato único de una oferta (`Job`). |
| Fuentes | `sources/` | Un conector por fuente. |
| Filtro | `student_filter.py` | Decide si una oferta es para estudiantes. |
| Base de datos | `db.py` | Guarda y consulta en SQLite (evita duplicados). |
| Recolector | `fetch.py` | Orquesta: recolecta → filtra → guarda. |
| Web local | `app.py` | Tablero Flask + API JSON (`/api/empleos`). |
| Publicación | `build_site.py` | Genera `docs/` (datos + widget) para GitHub Pages. |
| Widget | `static/widget.js` | El tablero embebible (buscador y filtros, en el navegador). |
| Bloque estático | `export_embed.py` | Genera un HTML sin scripts como respaldo. |

### Fuentes de datos

- **UNAL — Facultad de Minas** (`sources/unal_minas.py`): lee la página pública de convocatorias
  estudiantiles de la sede Medellín (permitido por su `robots.txt`, con User-Agent identificado
  y baja frecuencia) y extrae las convocatorias de **MINAS** con BeautifulSoup.
- **Jooble** (`sources/jooble.py`): API oficial de empleos. Para Colombia usa el host
  `co.jooble.org` (configurable en `config.JOOBLE_HOST`). Requiere una API key gratuita.
- **Arbeitnow** (`sources/arbeitnow.py`): API gratuita de empleos remotos; se usa solo en el
  tablero interno, no en el apartado público.

### Filtro para estudiantes

`student_filter.py` acepta una oferta si su título/descripción contienen señales como *aprendiz,
practicante, monitoría, medio tiempo, sin experiencia, junior*… y descarta títulos
*senior/gerente/director*. Las convocatorias de la UNAL se aceptan siempre (son, por definición,
para estudiantes).

### Buscador y filtros (en el apartado)

El widget incluye un **buscador** (ignora tildes) y **filtros por tipo**: *Prácticas, Aprendiz,
Medio tiempo, UNAL*. Todo ocurre en el navegador, al instante.

### Diseño

Usa la tipografía **Ancízar** (la oficial de la UNAL, heredada de la página) y los colores del
sitio de Bienestar (dorado `#f2a900`, enlaces azul `#135cae`).

## ¿Cómo se hizo?

- **Lenguaje:** Python para recolección, filtrado y web; un widget en JavaScript puro para el apartado.
- **Scraping responsable** de la página de convocatorias de la UNAL (respetando `robots.txt`).
- **API de Jooble** para los empleos de Medellín.
- **Automatización:** un flujo de **GitHub Actions** corre el proceso cada 6 horas y publica los
  datos en **GitHub Pages**.
- **Integración:** un `<script>` embebido en la página de Bienestar (Joomla) lee el JSON publicado;
  así el apartado se actualiza solo.

## Cómo ejecutarlo localmente (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env        # pega tu JOOBLE_API_KEY (https://jooble.org/api/about)

python fetch.py               # recolecta y guarda
python app.py                 # tablero en http://127.0.0.1:5000
```

## Publicar / actualizar (GitHub Pages)

- `python build_site.py` genera la carpeta `docs/` (`empleos.json`, `widget.js`, `index.html`).
- El flujo `.github/workflows/actualizar.yml` lo corre **cada 6 horas** (y a demanda) y publica en
  GitHub Pages.
- Requiere el secreto de Actions **`JOOBLE_API_KEY`**.

## Integración con la página de Bienestar (Joomla)

Pegar en un artículo (modo código) o en un bloque HTML de SP Page Builder:

```html
<div class="empleos-estudiantes"></div>
<script src="https://makecontrol-ing.github.io/empleos-estudiantes-minas/widget.js" defer></script>
```

Si el editor no permite scripts, está el respaldo estático
(`python export_embed.py` → `embed_estatico.html`), que se pega como HTML normal.

## Nota legal

Se usan **APIs oficiales** (Jooble, Arbeitnow) y la **página pública** de convocatorias de la UNAL,
permitida por su `robots.txt`, con User-Agent identificado y baja frecuencia. No se hace scraping
de portales comerciales que lo prohíben en sus términos.

## Estructura del proyecto

```
config.py        models.py        db.py             student_filter.py
fetch.py         app.py           build_site.py     export_embed.py
sources/
  base.py   arbeitnow.py   jooble.py   unal_minas.py
static/widget.js
docs/            (generado: lo publica GitHub Pages)
.github/workflows/actualizar.yml
requirements.txt
```

## Autor

**Andrés David Galeano Quintero** — Estudiante Auxiliar de Bienestar Universitario,
Facultad de Minas (UNAL).

- LinkedIn: https://linkedin.com/in/andres-david-galeano-quintero-9b9177301
- Correo: angaleanoq@unal.edu.co
