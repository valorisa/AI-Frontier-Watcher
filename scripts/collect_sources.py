#!/usr/bin/env python3
"""Collecte hebdomadaire des sources de veille AI-Frontier-Watcher.

La collecte ne modifie pas le README. Elle produit un rapport destiné à une
validation humaine avant publication.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "config" / "sources.json"
REPORT_DIR = ROOT / "reports"
USER_AGENT = "AI-Frontier-Watcher/0.1 (+https://github.com/valorisa/AI-Frontier-Watcher)"
TIMEOUT = 30


class TitleParser(HTMLParser):
    """Extrait le contenu du premier élément HTML <title>."""

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.parts).split())


def fetch_source(source: dict[str, object]) -> dict[str, object]:
    """Télécharge une source et retourne des métadonnées minimales."""

    url = str(source["url"])
    request = Request(url, headers={"User-Agent": USER_AGENT})

    result: dict[str, object] = {
        "id": source["id"],
        "provider": source["provider"],
        "level": source["level"],
        "url": url,
        "priority": source["priority"],
        "checked_at": datetime.now(UTC).isoformat(),
    }

    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            encoding_match = re.search(r"charset=([\w-]+)", content_type, re.I)
            encoding = encoding_match.group(1) if encoding_match else "utf-8"

            text = body.decode(encoding, errors="replace")
            parser = TitleParser()
            parser.feed(text)

            result.update(
                {
                    "status": response.status,
                    "content_type": content_type,
                    "title": parser.title,
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "bytes": len(body),
                }
            )
    except HTTPError as exc:
        result.update({"status": exc.code, "error": f"HTTP {exc.code}"})
    except (URLError, TimeoutError) as exc:
        result.update({"status": None, "error": str(exc)})
    except UnicodeError as exc:
        result.update({"status": None, "error": f"Encoding error: {exc}"})

    return result


def load_sources() -> list[dict[str, object]]:
    """Charge la liste de sources contrôlées."""

    with SOURCES_FILE.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError("config/sources.json doit contenir une liste.")

    return data


def build_report(results: list[dict[str, object]]) -> str:
    """Construit le rapport Markdown destiné à la revue humaine."""

    now = datetime.now(UTC)
    lines = [
        "# Rapport hebdomadaire de veille",
        "",
        f"Collecte UTC : **{now:%Y-%m-%d %H:%M:%S}**",
        "",
        "> Ce rapport est un artefact de collecte. Il ne modifie pas "
        "automatiquement `README.md`.",
        "",
        "## Résumé de collecte",
        "",
        "| Source | Niveau | HTTP | Titre | Empreinte |",
        "| --- | ---: | ---: | --- | --- |",
    ]

    for item in results:
        status = item.get("status", "erreur")
        title = str(item.get("title", item.get("error", "non disponible")))
        digest = str(item.get("sha256", ""))[:12] or "—"
        lines.append(
            f"| {item['provider']} / `{item['id']}` | {item['level']} | "
            f"{status} | {title} | `{digest}` |"
        )

    lines.extend(
        [
            "",
            "## Interprétation",
            "",
            "Une modification d'empreinte indique que le contenu récupéré a "
            "changé. Elle ne constitue pas, à elle seule, la preuve d'un "
            "changement de modèle ou de disponibilité.",
            "",
            "La validation humaine doit comparer le contenu source et "
            "déterminer si une mise à jour du README est justifiée.",
            "",
            "## Données brutes",
            "",
            "Les métadonnées complètes sont conservées dans le rapport JSON "
            "produit avec cette exécution.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    """Point d'entrée principal."""

    sources = load_sources()
    results = [fetch_source(source) for source in sources]

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now(UTC).date().isoformat()

    report_path = REPORT_DIR / f"weekly-{date}.md"
    json_path = REPORT_DIR / f"weekly-{date}.json"

    report_path.write_text(build_report(results), encoding="utf-8")
    json_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = [item for item in results if item.get("status") != 200]
    print(f"Sources contrôlées : {len(results)}")
    print(f"Erreurs HTTP/réseau : {len(failures)}")
    print(f"Rapport : {report_path}")
    print(f"Données JSON : {json_path}")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
