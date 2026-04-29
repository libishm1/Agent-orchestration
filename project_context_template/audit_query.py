#!/usr/bin/env python3
"""
Query the orchestration audit trail at wiki/audit_trail.jsonl.

Usage:
  python audit_query.py                          # last 10 events (summary)
  python audit_query.py --event checkpoint       # filter by event type
  python audit_query.py --agent codex_cloud      # filter by agent name
  python audit_query.py --task <slug>            # filter by task slug
  python audit_query.py --file <path>            # events that touched a file
  python audit_query.py --since 2026-04-29       # events since date (prefix match)
  python audit_query.py --severity P0            # health_check findings only
  python audit_query.py --last 20                # last N events
  python audit_query.py --json                   # full JSON output instead of summary
  python audit_query.py --count                  # print count only
"""

import argparse
import json
import sys
from pathlib import Path

TRAIL = Path(__file__).parent / "wiki" / "audit_trail.jsonl"

_SUMMARY_WIDTH_EVENT = 22
_SUMMARY_WIDTH_AGENT = 22


def load_events():
    if not TRAIL.exists():
        print(f"Audit trail not found: {TRAIL}", file=sys.stderr)
        return []
    events = []
    with TRAIL.open(encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"Warning: line {lineno} not valid JSON — {exc}", file=sys.stderr)
    return events


def _touches_file(event, target):
    for key in ("files_read", "files_changed", "raw_files", "pages_created", "pages_updated"):
        if target in event.get(key, []):
            return True
    return False


def _has_severity(event, severity):
    return any(f.get("severity") == severity for f in event.get("findings", []))


def apply_filters(events, args):
    if args.event:
        events = [e for e in events if e.get("event") == args.event]
    if args.agent:
        events = [
            e for e in events
            if args.agent in " ".join(filter(None, [
                e.get("agent"), e.get("from_agent"), e.get("to_agent"), e.get("parent_agent")
            ]))
        ]
    if args.task:
        events = [e for e in events if args.task in (e.get("task") or "")]
    if args.file:
        events = [e for e in events if _touches_file(e, args.file)]
    if args.since:
        events = [e for e in events if (e.get("ts") or "") >= args.since]
    if args.severity:
        events = [e for e in events if _has_severity(e, args.severity)]
    if args.last:
        events = events[-args.last:]
    return events


def print_summary(events):
    if not events:
        print("(no matching events)")
        return
    for e in events:
        ts = e.get("ts", "?")
        ev = e.get("event", "?")
        agent = e.get("agent") or e.get("from_agent") or "?"
        task = e.get("task") or ""
        extra_parts = []
        if task:
            extra_parts.append(task)
        # add outcome or checkpoint_n if present
        if "outcome" in e:
            extra_parts.append(e["outcome"])
        if "checkpoint_n" in e:
            extra_parts.append(f"n={e['checkpoint_n']}")
        if e.get("event") == "handoff":
            extra_parts.append(f"-> {e.get('to_agent','?')}")
        if e.get("event") == "health_check":
            p0 = e.get("p0_count", 0)
            if p0:
                extra_parts.append(f"P0:{p0}")
        extra = "  " + "  ".join(extra_parts) if extra_parts else ""
        print(f"{ts}  {ev:<{_SUMMARY_WIDTH_EVENT}}  {agent:<{_SUMMARY_WIDTH_AGENT}}{extra}")


def print_full(events):
    if not events:
        print("(no matching events)")
        return
    for e in events:
        print(json.dumps(e, indent=2, ensure_ascii=False))
        print()


def build_parser():
    p = argparse.ArgumentParser(
        description="Query wiki/audit_trail.jsonl.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--event", help="Filter by event type (e.g. checkpoint, handoff)")
    p.add_argument("--agent", help="Filter by agent name (substring match)")
    p.add_argument("--task", help="Filter by task slug (substring match)")
    p.add_argument("--file", help="Filter events that list this file path")
    p.add_argument("--since", help="Filter events with ts >= this prefix (e.g. 2026-04-29)")
    p.add_argument("--severity", choices=["P0", "P1", "P2"], help="Filter health_check findings by severity")
    p.add_argument("--last", type=int, help="Show last N events (default 10 when no other filter given)")
    p.add_argument("--json", dest="as_json", action="store_true", help="Full JSON output")
    p.add_argument("--count", action="store_true", help="Print count only")
    return p


def main():
    args = build_parser().parse_args()

    # default: show last 10 when no filter is given
    no_filter = not any([args.event, args.agent, args.task, args.file, args.since, args.severity, args.last])
    if no_filter:
        args.last = 10

    events = load_events()
    events = apply_filters(events, args)

    if args.count:
        print(len(events))
    elif args.as_json:
        print_full(events)
    else:
        print_summary(events)


if __name__ == "__main__":
    main()
