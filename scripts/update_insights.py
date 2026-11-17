#!/usr/bin/env python3
"""Refresh the Insights section of index.html from the Sequire Substack feed.

Run by .github/workflows/update-insights.yml once a day (and on demand).
Uses only the Python standard library.

- Takes the newest posts from https://sequireconsulting.substack.com/feed
- Uses a hand-written summary from data/insight-summaries.json when one exists
  for that post's URL, otherwise the post's Substack subtitle.
- Rewrites only the block between <!-- INSIGHTS:START --> and <!-- INSIGHTS:END -->.

Usage:
  python3 scripts/update_insights.py                 # fetch the live feed
  python3 scripts/update_insights.py --feed file.xml # use a saved feed (testing)
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://sequireconsulting.substack.com/feed"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
SUMMARIES = os.path.join(ROOT, "data", "insight-summaries.json")
COUNT = 3
START, END = "<!-- INSIGHTS:START -->", "<!-- INSIGHTS:END -->"


def esc(text):
    return html.escape(text, quote=True)


def card(title, url, summary, date_iso="", date_label=""):
    """HTML for one article card. Also imported by the site build so both match."""
    ext = 'target="_blank" rel="noopener"'
    date_html = (f'\n            <p class="article__date"><time datetime="{esc(date_iso)}">{esc(date_label)}</time></p>'
                 if date_iso else "")
    return f'''          <article class="article">
            <a class="article__thumb" href="{esc(url)}" {ext} tabindex="-1" aria-hidden="true">
              <span class="article__thumb-label">Sequire Insights</span>
              <span class="article__thumb-rule"></span>
              <span class="article__thumb-title">{esc(title)}</span>
            </a>{date_html}
            <h3><a href="{esc(url)}" {ext}>{esc(title)}</a></h3>
            <p>{esc(summary)}</p>
          </article>
'''


def block(cards_html):
    return f'{START}\n        <div class="insights__grid">\n{cards_html}        </div>\n        {END}'


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def read_feed(source):
    if source:
        with open(source, "rb") as f:
            return f.read()
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "SequireSiteBot/1.0 (+https://www.sequireconsulting.com)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def posts(xml_bytes):
    channel = ET.fromstring(xml_bytes).find("channel")
    items = []
    for item in channel.findall("item"):
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip().split("?")[0]
        if not title or not link:
            continue
        summary = clean(item.findtext("description"))
        try:
            dt = parsedate_to_datetime(item.findtext("pubDate"))
            iso, label = dt.date().isoformat(), dt.strftime("%B %Y")
        except Exception:
            iso, label, dt = "", "", None
        items.append({"title": title, "url": link, "summary": summary, "iso": iso, "label": label, "dt": dt})
    items.sort(key=lambda p: p["dt"].timestamp() if p["dt"] else 0, reverse=True)
    return items[:COUNT]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", help="read the feed from a local file instead of Substack")
    args = ap.parse_args()

    overrides = {}
    if os.path.exists(SUMMARIES):
        with open(SUMMARIES, encoding="utf-8") as f:
            overrides = json.load(f)

    latest = posts(read_feed(args.feed))
    if not latest:
        print("No posts found in the feed; leaving the page unchanged.")
        return 0

    cards = "".join(
        card(p["title"], p["url"], overrides.get(p["url"]) or p["summary"] or "Read the article on Substack.", p["iso"], p["label"])
        for p in latest)

    with open(INDEX, encoding="utf-8") as f:
        page = f.read()
    if START not in page or END not in page:
        print("Insights markers not found in index.html", file=sys.stderr)
        return 1
    updated = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block(cards), page, count=1, flags=re.S)
    if updated == page:
        print("Insights already up to date.")
        return 0
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(updated)
    print("Insights updated:", ", ".join(p["title"] for p in latest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
