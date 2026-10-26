#!/usr/bin/env python3
"""死链扫描：从 sitemap 提取 URL，并发检查状态码。

只依赖 Python 标准库。支持 sitemapindex 递归一层。

用法：
    python link_check.py --sitemap https://example.com/sitemap.xml
    python link_check.py --sitemap https://example.com/sitemap.xml --limit 200
    python link_check.py --urls urls.txt

退出码：
    0  无死链
    1  存在死链
"""

import argparse
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

UA = "net-dept-link-check/1.0 (+https://github.com)"
LOC_RE = re.compile(r"<loc>\s*(.+?)\s*</loc>", re.S)


def get_text(url, timeout):
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "ignore"), None
    except Exception as exc:
        return None, str(exc)


def collect(url, timeout, depth=1):
    text, err = get_text(url, timeout)
    if err:
        return [], err
    locs = LOC_RE.findall(text)
    if "<sitemapindex" in text:
        if depth <= 0:
            return [], None
        urls = []
        for sub in locs:
            more, _ = collect(sub, timeout, depth - 1)
            urls.extend(more)
        return urls, None
    return locs, None


def probe(url, timeout):
    req = Request(url, headers={"User-Agent": UA})
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as resp:
            resp.read(1024)
            return {"url": url, "code": resp.status, "ms": (time.perf_counter() - start) * 1000}
    except HTTPError as exc:
        return {"url": url, "code": exc.code, "ms": (time.perf_counter() - start) * 1000}
    except (socket.timeout, TimeoutError):
        return {"url": url, "code": None, "err": "超时"}
    except URLError as exc:
        return {"url": url, "code": None, "err": str(exc.reason)}
    except Exception as exc:
        return {"url": url, "code": None, "err": str(exc)}


def main():
    ap = argparse.ArgumentParser(description="死链扫描")
    ap.add_argument("--sitemap", help="sitemap 地址")
    ap.add_argument("--urls", help="URL 列表文件，每行一个")
    ap.add_argument("--limit", type=int, default=500, help="最多检查多少个 URL")
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    urls = []
    if args.sitemap:
        urls, err = collect(args.sitemap, args.timeout)
        if err:
            print(f"读取 sitemap 失败：{err}")
            return 1
    if args.urls:
        with open(args.urls, "r", encoding="utf-8") as fh:
            urls.extend(
                line.strip()
                for line in fh
                if line.strip() and not line.startswith("#")
            )
    urls = list(dict.fromkeys(urls))[: args.limit]

    if not urls:
        ap.error("没有拿到任何 URL，检查 --sitemap 或 --urls")

    print(f"检查 {len(urls)} 个 URL …\n")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda u: probe(u, args.timeout), urls))

    bad = [r for r in results if r["code"] is None or r["code"] >= 400]
    slow = [r for r in results if r["code"] and r["ms"] > 3000]

    if bad:
        print(f"### 死链 {len(bad)} 个\n")
        print("| URL | 状态码 | 错误 |")
        print("|---|---|---|")
        for r in bad:
            print(f"| {r['url']} | {r['code'] or '-'} | {r.get('err', '')} |")
    else:
        print("无死链。")

    if slow:
        print(f"\n### 响应偏慢 {len(slow)} 个（>3s）\n")
        for r in slow:
            print(f"- {r['url']} → {r['ms']:.0f}ms")

    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
