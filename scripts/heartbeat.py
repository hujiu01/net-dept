#!/usr/bin/env python3
"""定时任务心跳：给每个定时任务加一个"上次成功跑完"的时间戳，
超期未更新就报警。

解决的问题：cron 任务静默失败 —— 没报错、没产出，两周后才发现。
脚本跑成功就留一个心跳，另一个任务定期检查心跳，超期立即报警。

只依赖 Python 标准库。

用法：
    # 1. 在每个定时任务成功结束时调用（放在脚本最后一行）
    python heartbeat.py beat --dir /var/hb --name baidu-push

    # 2. 单独一个每日任务检查所有心跳
    python heartbeat.py check --dir /var/hb --max-age 26

    # 3. 只查某几个任务，单独设阈值（小时）
    python heartbeat.py check --dir /var/hb --expect baidu-push=26 --expect backup=50

退出码：
    beat   永远 0
    check  全部正常 0，有超期 1
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
        print(f"没有找到任何心跳记录（目录：{args.dir}）")
        print("检查任务是否真的在跑，或者 beat 命令有没有被调用。")
        return 1

    rows = []
    overdue = []
    for it in items:
        limit = expects.get(it["name"], args.max_age)
        if it["hours"] is None:
            status = "记录损坏"
            overdue.append((it["name"], status))
        elif it["hours"] > limit:
            status = f"超期（阈值 {limit:g}h）"
            overdue.append((it["name"], status))
        else:
            status = "正常"
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

    print(f"## 定时任务心跳 · {now_utc().strftime('%Y-%m-%d %H:%M')} UTC\n")
    print("| 任务 | 上次心跳（UTC） | 距今 | 阈值 | 状态 |")
    print("|---|---|---|---|---|")
    for r in rows:
        last = r["ts"].strftime("%Y-%m-%d %H:%M") if r["ts"] else str(r.get("raw"))[:16]
        ago = f"{r['hours']:.1f}h" if r["hours"] is not None else "-"
        print(f"| {r['name']} | {last} | {ago} | {r['limit']:g}h | {r['status']} |")

    if overdue:
        print(f"\n**{len(overdue)} 个任务超期**，按顺序排查：")
        print("1. 任务本身有没有跑（看 crontab）")
        print("2. 跑了但有报错（看日志）")
        print("3. 跑完但没调用 beat（代码路径问题）")
        print("4. 主机时区或系统时间错误")
        return 1
    print("\n全部正常。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="定时任务心跳")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("beat", help="记录一次成功心跳")
    b.add_argument("--dir", required=True)
    b.add_argument("--name", required=True)
    b.set_defaults(func=do_beat)

    c = sub.add_parser("check", help="检查心跳是否超期")
    c.add_argument("--dir", required=True)
    c.add_argument("--max-age", type=float, default=26, help="默认阈值（小时）")
    c.add_argument("--expect", action="append", help="单独设阈值，格式 name=hours，可重复")
    c.add_argument("--json", action="store_true", help="输出 JSON")
    c.set_defaults(func=do_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
