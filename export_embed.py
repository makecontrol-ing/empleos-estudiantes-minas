"""Genera 'embed_estatico.html': un bloque HTML autónomo (SOLO estilos en línea,
sin <script> ni <iframe>) para pegar en un artículo de Joomla.

Usa la tipografía Ancízar (la hereda de la página UNAL) y la paleta del sitio
(verde #b07d0a / lima #f2a900, enlaces azul #135cae). No se actualiza solo:
vuelve a correr este script para refrescar.

Uso:  python export_embed.py
"""
import sys
from html import escape

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import config
import db

FUENTE_LABEL = {"unal_minas": "UNAL", "jooble": "Jooble", "arbeitnow": "Remoto"}
FONT = "'Ancizar sans', Tahoma, Geneva, sans-serif"

ITEM = (
    '<div style="padding:12px 0;border-bottom:1px solid #ebebeb">'
    '<a href="{url}" target="_blank" rel="noopener" '
    'style="color:#135cae;text-decoration:none;font-weight:600;font-size:15px;'
    'font-family:{font}">{title}</a>'
    '<div style="color:#666;font-size:13px;margin-top:3px">{sub}</div>'
    '<div style="margin-top:5px;font-size:11px;color:#b07d0a;font-weight:700;'
    'text-transform:uppercase;letter-spacing:.4px">{tags}</div>'
    '</div>'
)


def main() -> None:
    empleos = db.get_jobs(solo_estudiantes=True, fuentes=config.FUENTES_EMBED, limite=60)
    prioridad = {"unal_minas": 0, "jooble": 1}
    empleos.sort(key=lambda e: prioridad.get(e.get("source"), 9))
    out = [
        f'<div style="font-family:{FONT};color:#3d3d3d;max-width:780px">',
        f'<h3 style="font-family:{FONT};color:#b07d0a;font-size:18px;font-weight:700;'
        'margin:0;border-bottom:3px solid #f2a900;padding-bottom:6px">'
        'Oportunidades para estudiantes</h3>',
        '<p style="font-size:12px;color:#777;margin:6px 0 14px">'
        f'Facultad de Minas &middot; {len(empleos)} vigentes</p>',
    ]
    for e in empleos:
        sub = escape(e.get("company") or "")
        if e.get("location"):
            sub += " &middot; " + escape(e["location"])
        src = e.get("source", "")
        tags = escape(FUENTE_LABEL.get(src, src))
        if e.get("employment_type"):
            tags += " &middot; " + escape(e["employment_type"])
        out.append(ITEM.format(
            font=FONT,
            url=escape(e.get("url") or "#"),
            title=escape(e.get("title") or "Sin título"),
            sub=sub,
            tags=tags,
        ))
    out.append("</div>")

    with open("embed_estatico.html", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"Generado 'embed_estatico.html' con {len(empleos)} empleos.")
    print("Copia su contenido y pégalo en el artículo de Joomla (modo código).")


if __name__ == "__main__":
    main()
