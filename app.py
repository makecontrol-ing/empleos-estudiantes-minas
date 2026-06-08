from flask import Flask, jsonify, redirect, render_template_string, request, url_for

import config
import db
from fetch import recolectar

app = Flask(__name__)

FUENTE_LABEL = {"unal_minas": "UNAL", "jooble": "Jooble", "arbeitnow": "Remoto"}

PLANTILLA = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Empleos para estudiantes · {{ ciudad }}</title>
<style>
  :root { --azul:#1d4ed8; --gris:#6b7280; --bg:#f8fafc; }
  * { box-sizing:border-box; }
  body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
         margin:0; background:var(--bg); color:#111827; }
  header { background:var(--azul); color:#fff; padding:22px 18px; }
  header h1 { margin:0 0 4px; font-size:20px; }
  header p { margin:0; opacity:.9; font-size:14px; }
  .wrap { max-width:880px; margin:0 auto; padding:18px; }
  form.filtros { display:flex; flex-wrap:wrap; gap:8px; margin:16px 0; }
  input[type=text], select { padding:8px 10px; border:1px solid #d1d5db;
         border-radius:8px; font-size:14px; }
  input[type=text] { flex:1; min-width:160px; }
  button { background:var(--azul); color:#fff; border:0; padding:8px 14px;
           border-radius:8px; font-size:14px; cursor:pointer; }
  button.sec { background:#e5e7eb; color:#111827; }
  .meta { color:var(--gris); font-size:13px; margin:6px 0 14px; }
  .meta a { color:var(--azul); }
  .card { background:#fff; border:1px solid #e5e7eb; border-radius:12px;
          padding:14px 16px; margin-bottom:12px; }
  .card h3 { margin:0 0 4px; font-size:16px; }
  .card h3 a { color:var(--azul); text-decoration:none; }
  .card .sub { color:#374151; font-size:14px; margin-bottom:6px; }
  .badge { display:inline-block; background:#eef2ff; color:var(--azul);
           font-size:11px; padding:2px 8px; border-radius:999px; margin-right:6px; }
  .desc { color:#4b5563; font-size:13px; margin:8px 0 0; }
  .vacio { text-align:center; color:var(--gris); padding:40px 0; }
</style>
</head>
<body>
<header>
  <h1>🎓 Empleos para estudiantes — {{ ciudad }}</h1>
  <p>Prácticas, contrato de aprendizaje SENA, medio tiempo y primer empleo.</p>
</header>
<div class="wrap">

  <form class="filtros" method="get" action="/">
    <input type="text" name="q" placeholder="Buscar cargo, empresa o ciudad…" value="{{ buscar }}">
    <select name="fuente">
      <option value="">Todas las fuentes</option>
      <option value="jooble" {% if fuente=='jooble' %}selected{% endif %}>Jooble (Colombia)</option>
      <option value="arbeitnow" {% if fuente=='arbeitnow' %}selected{% endif %}>Arbeitnow (remoto)</option>
    </select>
    {% if not solo_est %}<input type="hidden" name="todos" value="1">{% endif %}
    <button type="submit">Filtrar</button>
  </form>

  <div class="meta">
    {{ empleos|length }} resultados ·
    {% if solo_est %}
      solo aptos para estudiantes · <a href="/?todos=1{% if buscar %}&q={{ buscar }}{% endif %}">ver todos</a>
    {% else %}
      mostrando todos · <a href="/?{% if buscar %}q={{ buscar }}{% endif %}">ver solo estudiantes</a>
    {% endif %}
    · base: {{ stats.estudiantes }} para estudiantes / {{ stats.total }} totales
    <form method="post" action="/actualizar" style="display:inline; margin-left:8px;">
      <button class="sec" type="submit">🔄 Actualizar ahora</button>
    </form>
  </div>

  {% for e in empleos %}
    <div class="card">
      <h3><a href="{{ e.url }}" target="_blank" rel="noopener">{{ e.title or 'Sin título' }}</a></h3>
      <div class="sub">
        {{ e.company or 'Empresa no especificada' }}{% if e.location %} · {{ e.location }}{% endif %}
      </div>
      <div>
        <span class="badge">{{ labels.get(e.source, e.source) }}</span>
        {% if e.employment_type %}<span class="badge">{{ e.employment_type }}</span>{% endif %}
        {% if e.salary %}<span class="badge">💲 {{ e.salary }}</span>{% endif %}
      </div>
      {% if e.description %}<p class="desc">{{ e.description|striptags|truncate(220) }}</p>{% endif %}
    </div>
  {% else %}
    <div class="vacio">
      <p>No hay ofertas todavía.</p>
      <p>Pulsa <b>🔄 Actualizar ahora</b> o corre <code>python fetch.py</code> en la terminal.</p>
    </div>
  {% endfor %}

</div>
</body>
</html>
"""

EMBED_PLANTILLA = """
<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Empleos para estudiantes</title>
<style>
  body { font-family: 'Ancizar sans', Tahoma, Geneva, sans-serif; margin:0;
         background:#fff; color:#3d3d3d; }
  .wrap { max-width:780px; margin:0 auto; padding:14px; }
  h3.head { color:#b07d0a; font-size:18px; font-weight:700; margin:0;
            border-bottom:3px solid #f2a900; padding-bottom:6px; }
  .sub-h { font-size:12px; color:#777; margin:6px 0 14px; }
  .item { padding:12px 0; border-bottom:1px solid #ebebeb; }
  .item a { color:#135cae; text-decoration:none; font-weight:600; font-size:15px; }
  .item .sub { color:#666; font-size:13px; margin-top:3px; }
  .item .tags { margin-top:5px; font-size:11px; color:#b07d0a; font-weight:700;
                text-transform:uppercase; letter-spacing:.4px; }
</style></head>
<body><div class="wrap">
  <h3 class="head">Oportunidades para estudiantes</h3>
  <p class="sub-h">Facultad de Minas · {{ empleos|length }} vigentes</p>
  {% for e in empleos %}
    <div class="item">
      <a href="{{ e.url }}" target="_blank" rel="noopener">{{ e.title or 'Sin título' }}</a>
      <div class="sub">{{ e.company or '' }}{% if e.location %} · {{ e.location }}{% endif %}</div>
      <div class="tags">{{ labels.get(e.source, e.source) }}{% if e.employment_type %} · {{ e.employment_type }}{% endif %}</div>
    </div>
  {% endfor %}
</div></body></html>
"""


def _leer_filtros():
    solo_est = request.args.get("todos") != "1"
    buscar = request.args.get("q", "").strip()
    fuente = request.args.get("fuente", "").strip()
    try:
        limite = min(int(request.args.get("limite", 50)), 200)
    except (TypeError, ValueError):
        limite = 50
    return solo_est, buscar, fuente, limite


@app.after_request
def _cors(resp):
    if request.path.startswith("/api/"):
        resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/")
def index():
    solo_est = request.args.get("todos") != "1"
    buscar = request.args.get("q", "").strip()
    fuente = request.args.get("fuente", "").strip()
    empleos = db.get_jobs(solo_estudiantes=solo_est, buscar=buscar, fuente=fuente)
    return render_template_string(
        PLANTILLA,
        empleos=empleos,
        stats=db.stats(),
        solo_est=solo_est,
        buscar=buscar,
        fuente=fuente,
        ciudad=config.CIUDAD,
        labels=FUENTE_LABEL,
    )


@app.route("/actualizar", methods=["POST"])
def actualizar():
    recolectar()
    return redirect(url_for("index"))


@app.route("/api/empleos")
def api_empleos():
    solo_est, buscar, fuente, limite = _leer_filtros()
    empleos = db.get_jobs(solo_estudiantes=solo_est, buscar=buscar,
                          fuente=fuente, fuentes=config.FUENTES_EMBED, limite=limite)
    return jsonify({"total": len(empleos), "empleos": empleos})


@app.route("/embed")
def embed():
    solo_est, buscar, fuente, limite = _leer_filtros()
    empleos = db.get_jobs(solo_estudiantes=solo_est, buscar=buscar,
                          fuente=fuente, fuentes=config.FUENTES_EMBED, limite=limite)
    return render_template_string(EMBED_PLANTILLA, empleos=empleos,
                                  ciudad=config.CIUDAD, labels=FUENTE_LABEL)


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True, port=5000)
