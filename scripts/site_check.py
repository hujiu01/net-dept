#!/usr/bin/env python3
"""站点体检：状态码、响应耗时、SSL 剩余天数、robots 与 sitemap 可访问性。

只依赖 Python 标准库，无需安装任何包。

用法：
    python site_check.py https://example.com https://example.org
    python site_check.py --file sites.txt
    python site_check.py --timeout 15 --slow 3 https://example.com

退出码：
    0  全部正常
    1  存在异常（便于 cron / CI 判断）
"""

import argparse
import socket
import ssl
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

UA = "net-dept-site-check/1.0 (+https://github.com)"
DEFAULT_TIMEOUT = 10
DEFAULT_SLOW = 3.0
SSL_WARN_DAYS = 14


def fetch(url, timeout):
    """返回 (状态码, 耗时秒, 最终URL, 错误信息)。状态码为 None 表示请求失败。"""
    req = Request(url, headers={"User-Agent": UA})
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as resp:
            resp.read(2048)
            return resp.status, time.perf_counter() - start, resp.geturl(), None
    except HTTPError as exc:
        return exc.code, time.perf_counter() - start, url, None
    except URLError as exc:
        return None, time.perf_counter() - start, url, str(exc.reason)
    except (socket.timeout, TimeoutError):
        return None, time.perf_counter() - start, url, "超时"
    except Exception as exc:
        return None, time.perf_counter() - start, url, str(exc)


def ssl_days_left(host, port, timeout):
    """返回证书剩余天数；取不到返回 None。"""
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                cert = tls.getpeercert()
        expires = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        expires = expires.replace(tzinfo=timezone.utc)
        return (expires - datetime.now(timezone.utc)).days
    except Exception:
        return None


def check_one(url, timeout, slow):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        return {"url": url, "fatal": True, "notes": ["URL 格式不合法"]}

    base = f"{parsed.scheme}://{parsed.netloc}"
    notes = []
    fatal = False

    code, elapsed, final, err = fetch(url, timeout)
    if err:
        fatal = True
        notes.append(err)
    elif code and code >= 400:
        fatal = True
        notes.append(f"状态码 {code}")
    if elapsed and elapsed > slow:
        notes.append(f"慢 {elapsed:.1f}s")

    ssl_left = "-"
    if parsed.scheme == "https":
        days = ssl_days_left(parsed.hostname, parsed.port or 443, timeout)
        if days is None:
            ssl_left = "取不到"
            notes.append("证书异常")
        else:
            ssl_left = f"{days} 天"
            if days < 0:
                fatal = True
                notes.append("证书已过期")
            elif days < SSL_WARN_DAYS:
                notes.append(f"证书 {days} 天内到期")

    robots_code, _, _, _ = fetch(f"{base}/robots.txt", timeout)
    sitemap_code, _, _, _ = fetch(f"{base}/sitemap.xml", timeout)
    if sitemap_code is None or (isinstance(sitemap_code, int) and sitemap_code >= 400):
        notes.append("sitemap 不可访问")

    return {
        "url": url,
        "code": code,
        "elapsed": elapsed,
        "final": final,
        "ssl": ssl_left,
        "robots": robots_code,
        "sitemap": sitemap_code,
        "notes": notes,
        "fatal": fatal,
    }


def render(rows):
    lines = [
        "| 站点 | 状态码 | 耗时 | SSL | robots | sitemap | 备注 |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if "code" not in r:
            lines.append(f"| {r['url']} | - | - | - | - | - | {'; '.join(r['notes'])} |")
            continue
        elapsed = f"{r['elapsed']:.2f}s" if r.get("elapsed") is not None else "-"
        code = r.get("code") if r.get("code") is not None else "失败"
        mark = "异常" if r.get("fatal") else "正常"
        note = "; ".join(r.get("notes") or []) or mark
        lines.append(
            f"| {r['url']} | {code} | {elapsed} | {r['ssl']} | "
            f"{r['robots']} | {r['sitemap']} | {note} |"
        )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="站点体检")
    ap.add_argument("urls", nargs="*", help="要检查的站点 URL")
    ap.add_argument("--file", help="从文件读取 URL，每行一个，# 开头为注释")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--slow", type=float, default=DEFAULT_SLOW, help="超过多少秒算慢")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    if not urls:
        ap.error("至少给一个 URL，或用 --file 指定列表文件")

    with ThreadPoolExecutor(max_workers=min(8, len(urls))) as pool:
        rows = list(pool.map(lambda u: check_one(u, args.timeout, args.slow), urls))

    print(f"## 站点体检 · {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    print(render(rows))

    bad = [r for r in rows if r.get("fatal")]
    warn = [r for r in rows if not r.get("fatal") and r.get("notes")]
    if bad:
        print(f"\n**{len(bad)} 个站点异常**，需要处理：")
        for r in bad:
            print(f"- {r['url']} → {'; '.join(r['notes'])}")
        return 1
    if warn:
        print(f"\n全部可访问，有 {len(warn)} 条提示值得看一眼（不阻塞）。")
        return 0
    print("\n全部正常。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
