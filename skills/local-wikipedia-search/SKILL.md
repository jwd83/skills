---
name: local-wikipedia-search
description: Search and read this host's local text-only English Wikipedia Kiwix/ZIM mirror. Use when the user asks to look something up in our wiki install, needs encyclopedia/background facts, asks for Wikipedia/local wiki evidence, or when external web search is unnecessary.
---

# Local Wikipedia Search

Use this skill to search the locally hosted English Wikipedia mirror, not the public internet.

## Local mirror facts

- Public URL: `https://wiki.ayrscott.com/`
- Prefer local agent URL: `http://127.0.0.1:3081/`
- Service: `kiwix-wikipedia.service`
- ZIM: `/srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim`
- Snapshot: English Wikipedia text-only/no-image ZIM, March 2026
- Content URL prefix: `/content/wikipedia_en_all_nopic_2026-03/`

Do not confuse this with project markdown wikis. This skill is for the Kiwix-hosted English Wikipedia mirror.

## Preferred workflow

1. Search locally.
2. Read one or more likely article pages.
3. Answer from the local articles and cite the article title plus local URL.
4. If local search has no good result, say that the local mirror did not have a good hit instead of silently switching to web search.

## Helper scripts

Run these from this skill directory, or resolve the relative paths against this skill directory.

Search full text:

```bash
python3 ./scripts/wiki-search.py "apollo program" --limit 10
```

Search title suggestions/completions:

```bash
python3 ./scripts/wiki-search.py --suggest "Apollo"
```

Read an article as plain text:

```bash
python3 ./scripts/wiki-article.py "Apollo program" --max-chars 12000
```

Read by URL from a search result:

```bash
python3 ./scripts/wiki-article.py "http://127.0.0.1:3081/content/wikipedia_en_all_nopic_2026-03/Apollo_program"
```

## Manual fallback

If the helper scripts are unavailable:

```bash
ZIM=/srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim
kiwix-search "$ZIM" "search terms" | head -25
kiwix-search -s "$ZIM" "partial title" | head -25
```

To fetch an article, convert the title to the Wikipedia path form by replacing spaces with underscores and URL-encoding special characters, then fetch it from the local server:

```bash
python3 - <<'PY'
from urllib.parse import quote
base = 'http://127.0.0.1:3081/content/wikipedia_en_all_nopic_2026-03/'
title = 'Full moon'
print(base + quote(title.replace(' ', '_'), safe='()_,-.'))
PY
```

## Health checks

If search or article fetches fail, check the local service:

```bash
systemctl is-active kiwix-wikipedia.service
curl -fsSI http://127.0.0.1:3081/
```

If the service is down and sudo is available:

```bash
sudo systemctl restart kiwix-wikipedia.service
```
