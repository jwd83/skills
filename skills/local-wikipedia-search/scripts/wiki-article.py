#!/usr/bin/env python3
"""Fetch a local Kiwix Wikipedia article and print readable plain text."""

from __future__ import annotations

import argparse
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser
from urllib.parse import quote
from urllib.request import Request, urlopen

ZIM_SLUG = "wikipedia_en_all_nopic_2026-03"
BASE_URL = os.environ.get("LOCAL_WIKI_URL", "http://127.0.0.1:3081").rstrip("/")
CONTENT_PREFIX = f"/content/{ZIM_SLUG}/"

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "ol",
    "p",
    "pre",
    "section",
    "tr",
    "ul",
}
SKIP_TAGS = {"script", "style", "noscript", "svg", "math", "sup", "table"}
BOILERPLATE_LINES = {
    "Jump to content",
    "Main menu",
    "Personal tools",
    "Toggle the table of contents",
    "Tools",
    "Appearance",
    "hide",
}


class MainTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.main_depth = 0
        self.skip_depth = 0
        self.parts: list[str] = []
        self.saw_main = False

    def _newline(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "main" and attr_map.get("id") == "content" and not self.in_main:
            self.in_main = True
            self.saw_main = True
            self.main_depth = 1
        elif self.in_main:
            self.main_depth += 1

        if not self.in_main:
            return
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if self.skip_depth == 0 and tag in BLOCK_TAGS:
            self._newline()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.in_main and self.skip_depth == 0 and tag in BLOCK_TAGS:
            self._newline()

    def handle_endtag(self, tag: str) -> None:
        if not self.in_main:
            return
        if tag in SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
        if self.skip_depth == 0 and tag in BLOCK_TAGS:
            self._newline()
        self.main_depth -= 1
        if self.main_depth <= 0:
            self.in_main = False
            self.main_depth = 0

    def handle_data(self, data: str) -> None:
        if self.in_main and self.skip_depth == 0:
            self.parts.append(data)


def article_url(title_or_url: str) -> str:
    value = title_or_url.strip()
    if value.startswith(("http://", "https://")):
        return value
    if value.startswith(CONTENT_PREFIX):
        return BASE_URL + value
    path_title = value.replace(" ", "_")
    return f"{BASE_URL}{CONTENT_PREFIX}{quote(path_title, safe='()_,-.')}"


def normalize_text(raw: str) -> str:
    lines: list[str] = []
    blank = False
    for raw_line in raw.splitlines():
        line = unescape(re.sub(r"\s+", " ", raw_line)).strip()
        if not line:
            if lines and not blank:
                lines.append("")
                blank = True
            continue
        if line in BOILERPLATE_LINES:
            continue
        lines.append(line)
        blank = False
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "local-wikipedia-search-skill/1.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", "replace")

    parser = MainTextExtractor()
    parser.feed(html)
    text = normalize_text("".join(parser.parts))
    if not parser.saw_main or not text:
        raise RuntimeError("Could not find readable article text in the fetched page")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a local Kiwix Wikipedia article as text.")
    parser.add_argument("title_or_url", nargs="+", help="article title, /content path, or full local URL")
    parser.add_argument("--max-chars", type=int, default=12000, help="maximum characters to print")
    args = parser.parse_args()

    title_or_url = " ".join(args.title_or_url).strip()
    url = article_url(title_or_url)

    try:
        text = fetch_text(url)
    except Exception as exc:  # noqa: BLE001 - command-line helper should report any fetch/parse failure.
        print(f"Failed to read article: {exc}", file=sys.stderr)
        print(f"URL: {url}", file=sys.stderr)
        return 1

    max_chars = max(args.max_chars, 0)
    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars].rstrip()

    print(f"URL: {url}\n")
    print(text)
    if truncated:
        print(f"\n[truncated at {max_chars} characters]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
