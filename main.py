"""SkyGuard command-line entry point.

Examples:
    python main.py --event EVT001        # assess one simulated event
    python main.py --all                 # assess all events, write reports
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skyguard.data_loader import Dataset
from skyguard.assistant import Assistant
from skyguard.report import render_markdown

OUTPUT_DIR = Path(__file__).parent / "outputs"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SkyGuard flight-disruption AI assistant")
    parser.add_argument("--event", help="event id, e.g. EVT001")
    parser.add_argument("--all", action="store_true", help="assess every simulated event")
    parser.add_argument("--json", action="store_true", help="also dump JSON")
    args = parser.parse_args(argv)

    ds = Dataset()
    assistant = Assistant(ds)
    events = ds.events

    targets = []
    if args.all:
        targets = events
    elif args.event:
        targets = [e for e in events if str(e.get("事件编号")) == args.event]
        if not targets:
            print(f"event {args.event} not found", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 0

    OUTPUT_DIR.mkdir(exist_ok=True)
    import json
    for ev in targets:
        a = assistant.assess(ev)
        md = render_markdown(a)
        eid = a.event_id
        print(md)
        print()
        (OUTPUT_DIR / f"{eid}.md").write_text(md, encoding="utf-8")
        if args.json:
            (OUTPUT_DIR / f"{eid}.json").write_text(
                json.dumps(a.__dict__, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
