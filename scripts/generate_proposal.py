#!/usr/bin/env python3
"""Génère une proposition de veille à partir du dernier rapport JSON.

Le script sépare explicitement :

- config/source-state.json :
  état de référence accepté et versionné ;
- proposals/source-state-observed.json :
  état observé par la collecte courante ;
- proposals/weekly-YYYY-MM-DD.md :
  proposition destinée à la revue humaine.

Le script ne modifie jamais README.md ni l'état accepté.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
PROPOSAL_DIR = ROOT / "proposals"
STATE_FILE = ROOT / "config" / "source-state.json"
OBSERVED_STATE_FILE = PROPOSAL_DIR / "source-state-observed.json"


def find_latest_report() -> Path:
    """Retourne le rapport JSON hebdomadaire le plus récent."""
    reports = sorted(REPORT_DIR.glob("weekly-*.json"))
    if not reports:
        raise FileNotFoundError(
            "Aucun rapport JSON hebdomadaire trouvé dans reports/."
        )
    return reports[-1]


def load_json(path: Path) -> object:
    """Charge un fichier JSON UTF-8."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_state() -> dict[str, dict[str, object]]:
    """Charge l'état accepté, ou retourne un état vide."""
    if not STATE_FILE.exists():
        return {}

    data = load_json(STATE_FILE)
    if not isinstance(data, dict):
        raise ValueError("config/source-state.json doit contenir un objet JSON.")

    return data


def source_snapshot(item: dict[str, object]) -> dict[str, object]:
    """Extrait les informations pertinentes pour la comparaison."""
    return {
        "provider": item.get("provider"),
        "level": item.get("level"),
        "url": item.get("url"),
        "priority": item.get("priority"),
        "status": item.get("status"),
        "status_class": item.get("status_class"),
        "title": item.get("title"),
        "sha256": item.get("sha256"),
    }


def accessibility_state(snapshot: dict[str, object]) -> str | None:
    """Retourne l'état d'accessibilité connu de la source."""
    status_class = snapshot.get("status_class")
    if status_class in {"accessible", "inaccessible"}:
        return str(status_class)
    return None


def compare_sources(
    results: list[dict[str, object]],
    previous: dict[str, dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    """Compare la collecte courante avec l'état accepté.

    Les transitions d'accessibilité sont distinguées des changements
    de contenu. Une source inaccessible ne fournit pas de contenu
    comparable : ``sha256=None`` ne doit donc pas être traité comme
    une nouvelle empreinte.
    """
    changes: list[dict[str, object]] = []
    current: dict[str, dict[str, object]] = {}

    for item in results:
        source_id = str(item["id"])
        snapshot = source_snapshot(item)
        current[source_id] = snapshot

        if source_id not in previous:
            changes.append(
                {
                    "type": "new",
                    "id": source_id,
                    "current": snapshot,
                }
            )
            continue

        old = previous[source_id]
        old_accessibility = accessibility_state(old)
        new_accessibility = accessibility_state(snapshot)

        if old_accessibility != new_accessibility:
            changes.append(
                {
                    "type": "accessibility_changed",
                    "id": source_id,
                    "current": snapshot,
                    "previous": old,
                    "from": old_accessibility,
                    "to": new_accessibility,
                }
            )
            continue

        changed_fields = [
            field
            for field in snapshot
            if old.get(field) != snapshot.get(field)
        ]

        if changed_fields:
            changes.append(
                {
                    "type": "changed",
                    "id": source_id,
                    "current": snapshot,
                    "previous": old,
                    "fields": changed_fields,
                }
            )

    for source_id in sorted(set(previous) - set(current)):
        changes.append(
            {
                "type": "removed",
                "id": source_id,
                "previous": previous[source_id],
            }
        )

    return changes, current


def append_accessibility_change(
    lines: list[str],
    change: dict[str, object],
    provider: object,
    url: object,
) -> None:
    """Ajoute le rendu Markdown d'un changement d'accessibilité."""
    previous = change.get("previous", {})
    current = change.get("current", {})

    old_status = previous.get("status", "—")
    new_status = current.get("status", "—")
    old_class = previous.get("status_class", "—")
    new_class = current.get("status_class", "—")

    if change.get("to") == "accessible":
        heading = (
            f"### Source de nouveau accessible — "
            f"{provider} / `{change['id']}`"
        )
        note = (
            "Le contenu est de nouveau récupérable. La nouvelle "
            "empreinte ne doit pas être interprétée comme une "
            "modification du contenu pendant la période inaccessible."
        )
    else:
        heading = (
            f"### Source devenue inaccessible — "
            f"{provider} / `{change['id']}`"
        )
        note = (
            "Le contenu n'est plus récupérable. L'absence d'empreinte "
            "ne constitue pas une modification du contenu."
        )

    lines.extend(
        [
            heading,
            "",
            f"- URL : {url}",
            f"- Accessibilité : `{old_class}` → `{new_class}`",
            f"- HTTP : `{old_status}` → `{new_status}`",
            "",
            f"**Interprétation :** {note}",
            "",
            "**Action humaine requise :** vérifier la source et "
            "déterminer si cette évolution a une signification "
            "éditoriale.",
            "",
        ]
    )


def append_change(
    lines: list[str],
    change: dict[str, object],
) -> None:
    """Ajoute le rendu Markdown d'un changement."""
    change_type = change["type"]
    source_id = change["id"]
    current = change.get("current", {})
    previous = change.get("previous", {})

    provider = current.get("provider", previous.get("provider", "—"))
    url = current.get("url", previous.get("url", "—"))

    if change_type == "new":
        lines.extend(
            [
                f"### Nouvelle source — {provider} / `{source_id}`",
                "",
                f"- URL : {url}",
                f"- Niveau : {current.get('level', '—')}",
                f"- Statut : {current.get('status_class', '—')}",
                f"- HTTP : {current.get('status', '—')}",
                f"- Titre : {current.get('title', '—')}",
                "",
                "**Action humaine requise :** vérifier la source et déterminer "
                "si elle justifie une modification du README.",
                "",
            ]
        )

    elif change_type == "accessibility_changed":
        append_accessibility_change(
            lines,
            change,
            provider,
            url,
        )

    elif change_type == "changed":
        fields = ", ".join(change["fields"])
        lines.extend(
            [
                f"### Source modifiée — {provider} / `{source_id}`",
                "",
                f"- URL : {url}",
                f"- Champs modifiés : `{fields}`",
                "",
                "| Champ | Avant | Après |",
                "| --- | --- | --- |",
            ]
        )

        for field in change["fields"]:
            lines.append(
                f"| `{field}` | "
                f"{previous.get(field, '—')} | "
                f"{current.get(field, '—')} |"
            )

        lines.extend(
            [
                "",
                "**Attention :** une modification d'empreinte ou de statut "
                "ne constitue pas à elle seule une preuve de changement "
                "de modèle ou de disponibilité.",
                "",
                "**Action humaine requise :** consulter la source et "
                "déterminer si une modification du README est justifiée.",
                "",
            ]
        )

    elif change_type == "removed":
        lines.extend(
            [
                f"### Source absente — {provider} / `{source_id}`",
                "",
                f"- URL précédente : {url}",
                "",
                "**Action humaine requise :** déterminer si la source a "
                "réellement été supprimée ou si son absence est liée à "
                "la collecte.",
                "",
            ]
        )




def build_proposal(
    report_path: Path,
    changes: list[dict[str, object]],
) -> str:
    """Construit la proposition Markdown destinée à la revue humaine."""
    now = datetime.now(UTC)

    lines = [
        "# Proposition de mise à jour",
        "",
        f"Collecte analysée : **{report_path.name}**",
        f"Générée UTC : **{now:%Y-%m-%d %H:%M:%S}**",
        "",
        "> Cette proposition ne modifie pas `README.md`.",
        "> L'état accepté `config/source-state.json` n'est pas modifié.",
        "> Toute publication nécessite une validation humaine.",
        "",
    ]

    if not changes:
        lines.extend(
            [
                "## Résultat",
                "",
                "Aucun changement détecté depuis l'état de référence accepté.",
                "",
            ]
        )
        return chr(10).join(lines)

    lines.extend(
        [
            "## Changements détectés",
            "",
        ]
    )

    for change in changes:
        append_change(lines, change)

    lines.extend(
        [
            "## Règle de publication",
            "",
            "Cette proposition est un support de revue. Elle ne constitue "
            "pas une décision éditoriale.",
            "",
            "Le README et l'état de référence accepté ne doivent être "
            "modifiés qu'après vérification humaine des sources et de leur "
            "signification.",
            "",
        ]
    )

    return chr(10).join(lines)

def save_observed_state(state: dict[str, dict[str, object]]) -> None:
    """Enregistre l'état observé comme candidat, jamais comme état accepté."""
    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    OBSERVED_STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    """Point d'entrée principal."""
    report_path = find_latest_report()
    data = load_json(report_path)

    if not isinstance(data, list):
        raise ValueError(
            f"{report_path.name} doit contenir une liste de sources."
        )

    results = [
        item
        for item in data
        if isinstance(item, dict) and "id" in item
    ]

    previous = load_state()
    changes, current = compare_sources(results, previous)

    date = datetime.now(UTC).date().isoformat()
    proposal_path = PROPOSAL_DIR / f"weekly-{date}.md"

    if changes:
        PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
        proposal_path.write_text(
            build_proposal(report_path, changes),
            encoding="utf-8",
        )
        save_observed_state(current)
        print(f"Proposition : {proposal_path}")
        print(f"État observé : {OBSERVED_STATE_FILE}")
    else:
        if proposal_path.exists():
            proposal_path.unlink()
        if OBSERVED_STATE_FILE.exists():
            OBSERVED_STATE_FILE.unlink()
        print("Aucune proposition générée : aucun changement détecté.")

    print(f"Rapport analysé : {report_path}")
    print(f"Changements détectés : {len(changes)}")
    print(f"État accepté : {STATE_FILE}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
