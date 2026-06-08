from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class Job:
    source: str
    title: str
    company: str
    location: str
    url: str
    description: str = ""
    salary: str = ""
    employment_type: str = ""
    posted_at: str = ""
    is_student: bool = False
    fetched_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    id: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            base = f"{self.source}|{self.url or self.title}".lower()
            self.id = hashlib.sha1(base.encode("utf-8")).hexdigest()

    def to_row(self) -> dict:
        return asdict(self)
