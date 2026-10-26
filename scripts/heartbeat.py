#!/usr/bin/env python3
"""Cron heartbeat: stamp a "last successful run" time for each scheduled job and
alert when it goes stale.

Solves silent failure: a cron job that stops producing output without erroring
can go unnoticed for weeks. Add a beat on success, check the beats separately.

Standard library only.

Usage:
    # 1. At the successful end of every scheduled job
    python heartbeat.py beat --dir /var/hb --name daily-push

    # 2. A separate daily job checks all heartbeats
    python heartbeat.py check --dir /var/hb --max-age 26

    # 3. Per-job thresholds (hours)
    python heartbeat.py check --dir /var/hb --expect daily-push=26 --expect backup=50

Exit codes:
    beat   always 0
    check  0 when all fresh, 1 when anything is overdue
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_utc():
    return datetime.now(timezone.utc)


def do_beat(args):
    d = Path(args.dir).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    stamp = now_utc().isoformat(timespec="seconds")
    (d / f"{args.name}.ts").write_text(stamp + "\n", encoding="utf-8")
    print(f"heartbeat: {args.name} @ {stamp}")
    return 0


def load_beats(directory):
    d = Path(directory).expanduser()
    items = []
    if not d.is_dir():
        return items
    for path in sorted(d.glob("*.ts")):
        raw = path.read_text(encoding="utf-8").strip()
        try:
            ts = datetime.fromisoformat(raw)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except ValueError:
            items.append({"name": path.stem, "ts": None, "hours": None, "raw": raw})
            continue
        delta = now_utc() - ts
        items.append({"name": path.stem, "ts": ts, "hours": delta.total_seconds() / 3600})
    return items


def do_check(args):
    expects = {}
    for item in args.expect or []:
        if "=" not in item:
            continue
        name, hours = item.split("=", 1)
        try:
            expects[name] = float(hours)
        except ValueError:
            continue

    items = load_beats(args.dir)
    if not items:
        print(f"No heartbeat records found (dir: {args.dir})")
        print("Check whether the job actually runs, or whether `beat` is being called at all.")
        return 1

    rows = []
    overdue = []
    for it in items:
        limit = expects.get(it["name"], args.max_age)
        if it["hours"] is None:
            status = "corrupt record"
            overdue.append((it["name"], status))
        elif it["hours"] > limit:
            status = f"overdue (limit {limit:g}h)"
            overdue.append((it["name"], status))
        else:
            status = "ok"
        rows.append({**it, "limit": limit, "status": status})

    if args.json:
        print(json.dumps(
            [
                {
                    "name": r["name"],
                    "last": r["ts"].isoformat() if r["ts"] else None,
                    "hours_ago": round(r["hours"], 1) if r["hours"] is not None else None,
                    "limit_hours": r["limit"],
                    "status": r["status"],
                }
                for r in rows
            ],
            ensure_ascii=False,
            indent=2,
        ))
        return 1 if overdue else 0

    print(f"## Cron heartbeat · {now_utc().strftime('%Y-%m-%d %H:%M')} UTC\n")
    print("| Job | Last beat (UTC) | Age | Limit | Status |")
    print("|---|---|---|---|---|")
    for r in rows:
        last = r["ts"].strftime("%Y-%m-%d %H:%M") if r["ts"] else str(r.get("raw"))[:16]
        ago = f"{r['hours']:.1f}h" if r["hours"] is not None else "-"
        print(f"| {r['name']} | {last} | {ago} | {r['limit']:g}h | {r['status']} |")

    if overdue:
        print(f"\n**{len(overdue)} job(s) overdue** — check in this order:")
        print("1. Did the job run at all (check crontab)")
        print("2. Did it run and error (check logs)")
        print("3. Did it run but never reach the beat call (code path)")
        print("4. Is the host timezone or system clock wrong")
        return 1
    print("\nAll good.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Cron heartbeat")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("beat", help="record a successful run")
    b.add_argument("--dir", required=True)
    b.add_argument("--name", required=True)
    b.set_defaults(func=do_beat)

    c = sub.add_parser("check", help="check for stale heartbeats")
    c.add_argument("--dir", required=True)
    c.add_argument("--max-age", type=float, default=26, help="default threshold in hours")
    c.add_argument("--expect", action="append", help="per-job threshold as name=hours, repeatable")
    c.add_argument("--json", action="store_true", help="JSON output")
    c.set_defaults(func=do_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
