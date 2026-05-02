#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "research-run"


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Initialize research-mode run artifacts")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--research-type", required=True, choices=["market", "competitor", "exploratory", "simple-topic"])
    parser.add_argument("--tier", required=True, choices=["quick", "standard", "deep"])
    parser.add_argument("--output-root", default="runs")
    parser.add_argument("--deliverable", default="answer + evidence + source inventory")
    args = parser.parse_args()

    now = dt.datetime.now()
    run_id = f"{now:%Y-%m-%d}-{slugify(args.topic)}"
    output_root = Path(args.output_root)
    artifact_dir = output_root / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "run_id": run_id,
        "created_at": now.isoformat(timespec="seconds"),
        "topic": args.topic,
        "research_type": args.research_type,
        "tier": args.tier,
        "deliverable": args.deliverable,
        "artifact_dir": str(artifact_dir.resolve()),
    }
    write_json(artifact_dir / "meta.json", meta)
    write_json(artifact_dir / "queries.json", [])
    write_json(artifact_dir / "sources.json", [])
    write_json(artifact_dir / "evidence.json", [])

    brief = f"# {args.topic}\n\n"
    brief += f"- Run ID: {run_id}\n"
    brief += f"- Research type: {args.research_type}\n"
    brief += f"- Tier: {args.tier}\n"
    brief += f"- Deliverable: {args.deliverable}\n\n"
    brief += "## Scope\n- Objective: \n- Must-answer questions: \n- Boundaries: \n\n"
    brief += "## Working notes\n\n"
    brief += "## Final synthesis\n\n"
    (artifact_dir / "brief.md").write_text(brief, encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "artifact_dir": str(artifact_dir.resolve()),
        "files": {
            "meta": str((artifact_dir / 'meta.json').resolve()),
            "queries": str((artifact_dir / 'queries.json').resolve()),
            "sources": str((artifact_dir / 'sources.json').resolve()),
            "evidence": str((artifact_dir / 'evidence.json').resolve()),
            "brief": str((artifact_dir / 'brief.md').resolve()),
        }
    }, indent=2))


if __name__ == "__main__":
    main()
