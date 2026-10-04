#!/usr/bin/env python3

"""Collecte hebdomadaire des sources de veille AI-Frontier-Watcher.

La collecte ne modifie pas le README. Elle produit un rapport destiné à une
validation humaine avant publication.

Une source inaccessible ne fait pas échouer la collecte : son statut est
conservé explicitement dans les rapports Markdown et JSON. En revanche, les
erreurs internes du collecteur restent fatales.
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

USER_AGENT = (
    "AI-Frontier-Watcher/0.1 "
    "(+https://github.com/valorisa/AI-Frontier-Watcher)"
)

TIMEOUT = 30


class TitleParser(HTMLParser):
    """Extrait le contenu du premier élément HTML <title>."""

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
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
        """Retourne le titre HTML normalisé."""
        return " ".join("".join(self.parts).split())


def classify_http_status(status: int) -> str:
    """Classe un statut HTTP sans confondre échec de collecte et indisponibilité."""
    if status == 200:
        return "accessible"
    if status == 404:
        return "not_found"
    if status in {403, 429}:
        return "inconclusive"
    return "inconclusive"


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

            encoding_match = re.search(
                r"charset=([\w-]+)",
                content_type,
                re.I,
            )
            encoding = (
                encoding_match.group(1)
                if encoding_match
                else "utf-8"
            )

            text = body.decode(encoding, errors="replace")

            parser = TitleParser()
            parser.feed(text)

            result.update(
                {
                    "status": response.status,
                    "status_class": classify_http_status(response.status),
                    "content_type": content_type,
                    "title": parser.title,
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "bytes": len(body),
                }
            )

    except HTTPError as exc:
        result.update(
            {
                "status": exc.code,
                "status_class": classify_http_status(exc.code),
                "error": f"HTTP {exc.code}",
            }
        )

    except (URLError, TimeoutError) as exc:
        result.update(
            {
                "status": None,
                "status_class": "inconclusive",
                "error": str(exc),
            }
        )

    except UnicodeError as exc:
        result.update(
            {
                "status": None,
                "status_class": "inconclusive",
                "error": f"Encoding error: {exc}",
            }
        )

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

    accessible = [
        item for item in results if item.get("status_class") == "accessible"
    ]
    inconclusive = [
        item for item in results
        if item.get("status_class") == "inconclusive"
    ]
    not_found = [
        item for item in results if item.get("status_class") == "not_found"
    ]

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
        f"- Sources contrôlées : **{len(results)}**",
        f"- Sources accessibles : **{len(accessible)}**",
        f"- Collectes non concluantes : **{len(inconclusive)}**",
        f"- Sources retournant HTTP 404 : **{len(not_found)}**",
        "",
        "| Source | Niveau | Statut | HTTP | Titre | Empreinte |",
        "| --- | ---: | --- | ---: | --- | --- |",
    ]

    for item in results:
        status = item.get("status")
        status_text = str(item.get("status_class", "inconclusive"))
        title = str(
            item.get(
                "title",
                item.get("error", "non disponible"),
            )
        )
        digest = str(item.get("sha256", ""))[:12] or "—"
        http_status = str(status) if status is not None else "—"

        lines.append(
            f"| {item['provider']} / `{item['id']}` | {item['level']} | "
            f"**{status_text}** | {http_status} | {title} | "
            f"`{digest}` |"
        )

    lines.extend(
        [
            "",
            "## Interprétation",
            "",
            "Une source **accessible** a répondu avec HTTP 200 et son "
            "contenu a été analysé.",
            "",
            "Une collecte **non concluante** n'a pas permis de déterminer "
            "l'état réel de la source. Cela ne constitue pas une preuve "
            "d'indisponibilité de la source elle-même.",
            "",
            "Un statut HTTP 403 ou 429, ou une erreur réseau ou d'encodage, "
            "est conservé comme information de collecte sans contournement "
            "des protections de la source.",
            "",
            "Un statut HTTP 404 indique que l'URL contrôlée n'a pas été "
            "trouvée au moment de la collecte. Il nécessite une validation "
            "humaine avant toute modification de l'état accepté.",
            "",
            "Une modification d'empreinte indique que le contenu récupéré "
            "a changé. Elle ne constitue pas, à elle seule, la preuve "
            "d'un changement de modèle ou de disponibilité.",
            "",
            "La validation humaine doit comparer le contenu source et "
            "déterminer si une mise à jour du README est justifiée.",
            "",
            "## Données brutes",
            "",
            "Les métadonnées complètes sont conservées dans le rapport "
            "JSON produit avec cette exécution.",
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

    report_path.write_text(
        build_report(results),
        encoding="utf-8",
    )

    json_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    accessible = [
        item
        for item in results
        if item.get("status_class") == "accessible"
    ]
    inconclusive = [
        item
        for item in results
        if item.get("status_class") == "inconclusive"
    ]
    not_found = [
        item
        for item in results
        if item.get("status_class") == "not_found"
    ]

    print(f"Sources contrôlées : {len(results)}")
    print(f"Sources accessibles : {len(accessible)}")
    print(f"Collectes non concluantes : {len(inconclusive)}")
    print(f"Sources HTTP 404 : {len(not_found)}")
    print(f"Rapport : {report_path}")
    print(f"Données JSON : {json_path}")

    for item in inconclusive + not_found:
        status = item.get("status")
        status_text = (
            f"HTTP {status}"
            if status is not None
            else str(item.get("error", "erreur inconnue"))
        )
        message = (
            f"{item['provider']} / {item['id']} : "
            f"collecte non concluante ({status_text})"
        )
        print(f"::warning::{message}")

    # Une collecte non concluante est un résultat de collecte, pas une
    # défaillance du collecteur. Les erreurs internes restent fatales.
    return 0


if __name__ == "__main__":
    sys.exit(main())
