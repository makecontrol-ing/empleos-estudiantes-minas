import json
import os
import shutil
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv

import config
import db
from fetch import recolectar

load_dotenv()

DOCS = Path("docs")


def pages_url() -> str:
    repo = os.getenv("GITHUB_REPOSITORY", "")
    if "/" in repo:
        owner, name = repo.split("/", 1)
        return f"https://{owner}.github.io/{name}/"
    return "https://USUARIO.github.io/REPO/"


def index_html(total: int, snippet: str) -> str:
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Empleos para estudiantes - Facultad de Minas</title></head>
<body style="background:#fafafa;margin:0;padding:24px;font-family:'Ancizar sans',Tahoma,Geneva,sans-serif;color:#3d3d3d">
  <div style="max-width:820px;margin:0 auto">
    <h2 style="color:#b07d0a">Empleos para estudiantes - Facultad de Minas</h2>
    <p style="color:#777">Vista previa del apartado ({total} oportunidades). Se actualiza solo.</p>

    <h3 style="border-bottom:3px solid #f2a900;padding-bottom:6px">Vista previa</h3>
    <div class="empleos-estudiantes"></div>
    <script src="widget.js" defer></script>

    <h3 style="margin-top:32px;border-bottom:3px solid #f2a900;padding-bottom:6px">Para pegar en Bienestar (Joomla)</h3>
    <p>Copia esto en un artículo (modo código) o en un bloque HTML de SP Page Builder:</p>
    <pre style="background:#f0f0f0;padding:12px;border-radius:6px;overflow:auto">{snippet}</pre>
  </div>
</body></html>
"""


def main() -> None:
    recolectar()
    empleos = db.get_jobs(solo_estudiantes=True, fuentes=config.FUENTES_EMBED, limite=120)
    prioridad = {"unal_minas": 0, "jooble": 1}
    empleos.sort(key=lambda e: prioridad.get(e.get("source"), 9))

    DOCS.mkdir(exist_ok=True)
    (DOCS / "empleos.json").write_text(
        json.dumps(
            {
                "actualizado": datetime.now(timezone.utc).isoformat(),
                "total": len(empleos),
                "empleos": empleos,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    shutil.copy("static/widget.js", DOCS / "widget.js")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    snippet = escape(
        '<div class="empleos-estudiantes"></div>\n'
        f'<script src="{pages_url()}widget.js" defer></script>'
    )
    (DOCS / "index.html").write_text(index_html(len(empleos), snippet), encoding="utf-8")

    print(f"docs/ listo con {len(empleos)} empleos. Pages URL: {pages_url()}")


if __name__ == "__main__":
    main()
