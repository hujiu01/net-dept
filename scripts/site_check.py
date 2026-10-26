#!/usr/bin/env python3
"""Site health check: status code, response time, SSL days remaining, robots and sitemap reachability.

Standard library only — nothing to install.

Usage:
    python site_check.py https://example.com https://example.org
    python site_check.py --file sites.txt
    python site_check.py --timeout 15 --slow 3 https://example.com

Exit codes:
    0  everything fine
    1  at least one site failing (so cron / CI can act on it)
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

UA = "net-dept-site-check/1.0 (+https://github.com/hujiu01/net-dept)"
DEFAULT_TIMEOUT = 10
DEFAULT_SLOW = 3.0
SSL_WARN_DAYS = 14


def fetch(url, timeout):
    """Return (status, seconds, final_url, error). status is None when the request failed."""
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
        return None, time.perf_counter() - start, url, "timeout"
    except Exception as exc:
        return None, time.perf_counter() - start, url, str(exc)


def ssl_days_left(host, port, timeout):
    """Days until certificate expiry; None if it can't be read."""
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
        return {"url": url, "fatal": True, "notes": ["invalid URL"]}

    base = f"{parsed.scheme}://{parsed.netloc}"
    notes = []
    fatal = False

    code, elapsed, final, err = fetch(url, timeout)
    if err:
        fatal = True
        notes.append(err)
    elif code and code >= 400:
        fatal = True
        notes.append(f"HTTP {code}")
    if elapsed and elapsed > slow:
        notes.append(f"slow {elapsed:.1f}s")

    ssl_left = "-"
    if parsed.scheme == "https":
        days = ssl_days_left(parsed.hostname, parsed.port or 443, timeout)
        if days is None:
            ssl_left = "error"
            notes.append("certificate unreadable")
        else:
            ssl_left = f"{days}d"
            if days < 0:
                fatal = True
                notes.append("certificate expired")
            elif days < SSL_WARN_DAYS:
                notes.append(f"certificate expires in {days}d")

    robots_code, _, _, _ = fetch(f"{base}/robots.txt", timeout)
    sitemap_code, _, _, _ = fetch(f"{base}/sitemap.xml", timeout)
    if sitemap_code is None or (isinstance(sitemap_code, int) and sitemap_code >= 400):
        notes.append("sitemap unreachable")

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
        "| Site | Status | Time | SSL | robots | sitemap | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if "code" not in r:
            lines.append(f"| {r['url']} | - | - | - | - | - | {'; '.join(r['notes'])} |")
            continue
        elapsed = f"{r['elapsed']:.2f}s" if r.get("elapsed") is not None else "-"
        code = r.get("code") if r.get("code") is not None else "FAIL"
        note = "; ".join(r.get("notes") or []) or ("FAIL" if r.get("fatal") else "ok")
        lines.append(
            f"| {r['url']} | {code} | {elapsed} | {r['ssl']} | "
            f"{r['robots']} | {r['sitemap']} | {note} |"
        )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Site health check")
    ap.add_argument("urls", nargs="*", help="site URLs to check")
    ap.add_argument("--file", help="read URLs from a file, one per line, # for comments")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--slow", type=float, default=DEFAULT_SLOW, help="seconds before a response counts as slow")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    if not urls:
        ap.error("give at least one URL, or use --file")

    with ThreadPoolExecutor(max_workers=min(8, len(urls))) as pool:
        rows = list(pool.map(lambda u: check_one(u, args.timeout, args.slow), urls))

    print(f"## Site health · {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    print(render(rows))

    bad = [r for r in rows if r.get("fatal")]
    warn = [r for r in rows if not r.get("fatal") and r.get("notes")]
    if bad:
        print(f"\n**{len(bad)} site(s) failing** — needs attention:")
        for r in bad:
            print(f"- {r['url']} → {'; '.join(r['notes'])}")
        return 1
    if warn:
        print(f"\nAll reachable; {len(warn)} note(s) worth a look (non-blocking).")
        return 0
    print("\nAll good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
