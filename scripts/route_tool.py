#!/usr/bin/env python3
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Deterministic Firecrawl-first routing helper")
    parser.add_argument("--intent", required=True, choices=["discover", "fetch", "domain-scope", "site-wide", "fallback-check"])
    parser.add_argument("--url")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--reason")
    args = parser.parse_args()

    if args.intent == "discover":
        result = {
            "primary_tool": "firecrawl:/v1/search",
            "why": "Best first move for topic discovery and auto-extraction",
            "fallback_allowed_when": [
                "technical failure",
                "blocked or empty content",
                "insufficient useful coverage"
            ]
        }
    elif args.intent == "fetch":
        result = {
            "primary_tool": "firecrawl:/v1/scrape",
            "why": "Known URL fetch should use Firecrawl scrape first",
            "url": args.url,
            "fallback_allowed_when": [
                "technical failure",
                "blocked or empty content",
                "insufficient useful coverage"
            ]
        }
    elif args.intent == "domain-scope":
        result = {
            "primary_tool": "firecrawl:/v1/map",
            "why": "Use map when you need domain URL inventory before page selection",
            "url": args.url,
            "fallback_allowed_when": [
                "technical failure",
                "unsupported mapping need"
            ]
        }
    elif args.intent == "site-wide":
        result = {
            "primary_tool": "firecrawl:/v1/crawl",
            "why": "Use crawl only for site-wide escalation after narrower options are insufficient",
            "depth": args.depth,
            "fallback_allowed_when": [
                "technical failure",
                "crawl not available in current environment"
            ]
        }
    else:
        reason = (args.reason or "").strip().lower()
        allowed = any(token in reason for token in [
            "timeout", "4xx", "5xx", "blocked", "empty", "coverage", "unsupported"
        ])
        result = {
            "fallback_allowed": allowed,
            "why": "Fallback is valid only for technical failure, blocked/empty content, insufficient coverage, or unsupported need",
            "reason": args.reason,
        }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
