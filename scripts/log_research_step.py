#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Append research log entries for research-mode")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--mode", required=True, choices=["query", "source", "evidence", "fallback"])
    parser.add_argument("--query")
    parser.add_argument("--intent")
    parser.add_argument("--tool")
    parser.add_argument("--result-summary")
    parser.add_argument("--url")
    parser.add_argument("--title")
    parser.add_argument("--source-class")
    parser.add_argument("--claim")
    parser.add_argument("--confidence")
    parser.add_argument("--note")
    parser.add_argument("--source")
    parser.add_argument("--reason")
    parser.add_argument("--details")
    args = parser.parse_args()

    artifact_dir = Path(args.artifact_dir)
    ts = dt.datetime.now().isoformat(timespec="seconds")

    if args.mode == "query":
        path = artifact_dir / "queries.json"
        data = load_json(path)
        data.append({
            "timestamp": ts,
            "query": args.query,
            "intent": args.intent,
            "tool": args.tool,
            "result_summary": args.result_summary,
        })
        save_json(path, data)

    elif args.mode == "source":
        path = artifact_dir / "sources.json"
        data = load_json(path)
        data.append({
            "timestamp": ts,
            "url": args.url,
            "title": args.title,
            "source_class": args.source_class,
            "note": args.note,
        })
        save_json(path, data)

    elif args.mode == "evidence":
        path = artifact_dir / "evidence.json"
        data = load_json(path)
        data.append({
            "timestamp": ts,
            "claim": args.claim,
            "url": args.url,
            "title": args.title,
            "source_class": args.source_class,
            "confidence": args.confidence,
            "note": args.note,
        })
        save_json(path, data)

    elif args.mode == "fallback":
        path = artifact_dir / "queries.json"
        data = load_json(path)
        data.append({
            "timestamp": ts,
            "event": "fallback",
            "source": args.source,
            "reason": args.reason,
            "details": args.details,
        })
        save_json(path, data)

    print(json.dumps({"ok": True, "mode": args.mode, "artifact_dir": str(artifact_dir.resolve())}, indent=2))


if __name__ == "__main__":
    main()
