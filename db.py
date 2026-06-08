import sqlite3
from contextlib import contextmanager
from typing import Iterable

import config
from models import Job

_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id              TEXT PRIMARY KEY,
    source          TEXT,
    title           TEXT,
    company         TEXT,
    location        TEXT,
    url             TEXT,
    description     TEXT,
    salary          TEXT,
    employment_type TEXT,
    posted_at       TEXT,
    is_student      INTEGER,
    fetched_at      TEXT
);
"""


@contextmanager
def _connect():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(_SCHEMA)


def upsert_jobs(jobs: Iterable[Job]) -> int:
    nuevas = 0
    with _connect() as conn:
        for job in jobs:
            cur = conn.execute(
                """
                INSERT INTO jobs (id, source, title, company, location, url,
                                  description, salary, employment_type, posted_at,
                                  is_student, fetched_at)
                VALUES (:id, :source, :title, :company, :location, :url,
                        :description, :salary, :employment_type, :posted_at,
                        :is_student, :fetched_at)
                ON CONFLICT(id) DO NOTHING
                """,
                {**job.to_row(), "is_student": int(job.is_student)},
            )
            if cur.rowcount:
                nuevas += 1
    return nuevas


def get_jobs(
    solo_estudiantes: bool = True,
    buscar: str = "",
    fuente: str = "",
    fuentes: list | None = None,
    limite: int = 200,
) -> list[dict]:
    sql = "SELECT * FROM jobs WHERE 1=1"
    params: list = []
    if solo_estudiantes:
        sql += " AND is_student = 1"
    if fuente:
        sql += " AND source = ?"
        params.append(fuente)
    if fuentes:
        sql += " AND source IN (%s)" % ",".join("?" for _ in fuentes)
        params.extend(fuentes)
    if buscar:
        sql += " AND (lower(title) LIKE ? OR lower(company) LIKE ? OR lower(location) LIKE ?)"
        like = f"%{buscar.lower()}%"
        params += [like, like, like]
    sql += " ORDER BY fetched_at DESC LIMIT ?"
    params.append(limite)
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def stats() -> dict:
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        est = conn.execute("SELECT COUNT(*) FROM jobs WHERE is_student=1").fetchone()[0]
    return {"total": total, "estudiantes": est}
