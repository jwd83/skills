#!/usr/bin/env python3
"""Search the public Kiwix-hosted English Wikipedia mirror."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from html import unescape
from html.parser import HTMLParser
from urllib.parse import quote, urlencode, urljoin
from urllib.request import Request, urlopen

PUBLIC_BASE_URL = "https://wiki.ayrscott.com"
ZIM_PATH = "/srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim"
ZIM_SLUG = "wikipedia_en_all_nopic_2026-03"
CONTENT_PREFIX = f"/content/{ZIM_SLUG}/"
DEFAULT_BASE_URL = os.environ.get("WIKI_BASE_URL") or os.environ.get("LOCAL_WIKI_URL") or PUBLIC_BASE_URL


class SearchResultParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.current_href: str | None = None
        self.current_text: list[str] = []
        self.results: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        absolute = urljoin(self.base_url + "/", href)
        if CONTENT_PREFIX in absolute:
            self.current_href = absolute
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self.current_href is None:
            return
        title = unescape(" ".join("".join(self.current_text).split()))
        if title:
            item = (title, self.current_href)
            if item not in self.results:
                self.results.append(item)
        self.current_href = None
        self.current_text = []


def title_url(title: str, base_url: str) -> str:
    path_title = title.strip().replace(" ", "_")
    return f"{base_url.rstrip('/')}{CONTENT_PREFIX}{quote(path_title, safe='()_,-.')}"


def search_http(query: str, base_url: str) -> list[tuple[str, str]]:
    url = f"{base_url.rstrip('/')}/search?{urlencode({'pattern': query})}"
    request = Request(url, headers={"User-Agent": "local-wikipedia-search-skill/1.0"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    parser = SearchResultParser(base_url.rstrip("/"))
    parser.feed(html)
    return parser.results


def search_local_zim(query: str, zim: str, suggest: bool, base_url: str) -> list[tuple[str, str]]:
    if not os.path.exists(zim):
        raise FileNotFoundError(f"ZIM file not found: {zim}")

    cmd = ["kiwix-search"]
    if suggest:
        cmd.append("--suggestion")
    cmd.extend([zim, query])

    result = subprocess.run(cmd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"kiwix-search exited {result.returncode}")

    titles = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return [(title, title_url(title, base_url)) for title in titles]


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the Kiwix English Wikipedia mirror at wiki.ayrscott.com.")
    parser.add_argument("query", nargs="+", help="search query")
    parser.add_argument("--suggest", "-s", action="store_true", help="suggest matching article titles when using --zim; otherwise performs normal public search")
    parser.add_argument("--limit", "-n", type=int, default=20, help="maximum results to print")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="wiki base URL; defaults to https://wiki.ayrscott.com or WIKI_BASE_URL")
    parser.add_argument("--zim", default=None, help=f"optional local ZIM path for kiwix-search, e.g. {ZIM_PATH}")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        print("empty query", file=sys.stderr)
        return 2

    base_url = args.base_url.rstrip("/")
    try:
        if args.zim:
            results = search_local_zim(query, args.zim, args.suggest, base_url)
        else:
            results = search_http(query, base_url)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - command-line helper should report any fetch/search failure.
        print(f"Search failed: {exc}", file=sys.stderr)
        return 1

    if not results:
        print(f"No wiki results for: {query}")
        return 0

    for index, (title, url) in enumerate(results[: max(args.limit, 0)], start=1):
        print(f"{index}. {title}")
        print(f"   {url}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
