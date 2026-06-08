import requests

from models import Job
from sources.base import Connector

API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowConnector(Connector):
    name = "arbeitnow"

    def fetch(self) -> list[Job]:
        resp = requests.get(API_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", [])

        jobs: list[Job] = []
        for item in data:
            tipos = ", ".join(item.get("job_types", []) or [])
            ubicacion = item.get("location") or ("Remoto" if item.get("remote") else "")
            jobs.append(
                Job(
                    source=self.name,
                    title=(item.get("title") or "").strip(),
                    company=(item.get("company_name") or "").strip(),
                    location=ubicacion,
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    employment_type=tipos,
                    posted_at=str(item.get("created_at", "")),
                )
            )
        return jobs
