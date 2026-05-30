#!/usr/bin/env python3
"""Search the local English Wikipedia Kiwix/ZIM mirror."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from urllib.parse import quote

ZIM_PATH = "/srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim"
ZIM_SLUG = "wikipedia_en_all_nopic_2026-03"
BASE_URL = os.environ.get("LOCAL_WIKI_URL", "http://127.0.0.1:3081").rstrip("/")


def title_url(title: str) -> str:
    path_title = title.strip().replace(" ", "_")
    return f"{BASE_URL}/content/{ZIM_SLUG}/{quote(path_title, safe='()_,-.')}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the local Kiwix English Wikipedia mirror.")
    parser.add_argument("query", nargs="+", help="search query")
    parser.add_argument("--suggest", "-s", action="store_true", help="suggest matching article titles instead of full-text search")
    parser.add_argument("--limit", "-n", type=int, default=20, help="maximum results to print")
    parser.add_argument("--zim", default=ZIM_PATH, help="path to ZIM file")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        print("empty query", file=sys.stderr)
        return 2
    if not os.path.exists(args.zim):
        print(f"ZIM file not found: {args.zim}", file=sys.stderr)
        return 1

    cmd = ["kiwix-search"]
    if args.suggest:
        cmd.append("--suggestion")
    cmd.extend([args.zim, query])

    try:
        result = subprocess.run(cmd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("kiwix-search not found; install kiwix-tools", file=sys.stderr)
        return 1

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return result.returncode

    titles = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not titles:
        print(f"No local Wikipedia results for: {query}")
        return 0

    for index, title in enumerate(titles[: max(args.limit, 0)], start=1):
        print(f"{index}. {title}")
        print(f"   {title_url(title)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
