"""Collect text posts from a subreddit into a CSV you can label.

Usage:
    python collect_posts.py --subreddit soccer  # 60 from top-of-year, 60 from new
    python collect_posts.py --top 80 --new 80

Uses the subreddit RSS feed (no login needed). Writes collected.csv with columns text,label,note. `label` is left blank for
you to fill in. Image/link-only posts and very short posts are skipped.
"""
import argparse
import csv
import html
import re
import time
import xml.etree.ElementTree as ET

import requests

# Reddit blocks the .json endpoints for anonymous scripts; the RSS feed works.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
NS = {"a": "http://www.w3.org/2005/Atom"}


def clean(fragment):
    """HTML fragment from the feed -> plain text."""
    text = re.sub(r"<(br|/p)\s*/?>", "\n", html.unescape(fragment))
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"submitted by\s+/u/\S+.*$", "", text, flags=re.S)
    text = re.sub(r"\[(link|comments)\]", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def fetch(subreddit, listing, want, **params):
    """Page through a listing until `want` usable posts are found."""
    posts, after = [], None
    while len(posts) < want:
        for wait in (10, 30, 60, None):  # back off if Reddit rate-limits us
            resp = requests.get(
                f"https://www.reddit.com/r/{subreddit}/{listing}.rss",
                headers=HEADERS,
                params={"limit": 100, "after": after, **params},
                timeout=15,
            )
            if resp.status_code != 429 or wait is None:
                break
            print(f"Rate limited; waiting {wait}s...")
            time.sleep(wait)
        resp.raise_for_status()
        entries = ET.fromstring(resp.content).findall("a:entry", NS)
        if not entries:
            break
        for e in entries:
            pid = e.find("a:id", NS).text  # e.g. t3_abc123
            title = e.find("a:title", NS).text.strip()
            body = clean(e.find("a:content", NS).text or "")
            # Image/link posts carry no text of their own
            if "i.redd.it" in body or "v.redd.it" in body:
                continue
            text = f"{title}\n\n{body}" if body else title
            if len(text.split()) < 8:  # too short to carry a take
                continue
            posts.append({"id": pid, "text": text})
        after = entries[-1].find("a:id", NS).text
        time.sleep(2)  # be polite
    return posts[:want]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subreddit", default="sitcoms")
    ap.add_argument("--top", type=int, default=60)
    ap.add_argument("--new", type=int, default=60)
    ap.add_argument("--out", default="collected.csv")
    args = ap.parse_args()

    rows, seen = [], set()
    for listing, n, extra, tag in [
        ("top", args.top, {"t": "year"}, "top-year"),
        ("new", args.new, {}, "new"),
    ]:
        for p in fetch(args.subreddit, listing, n, **extra):
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            rows.append({"text": p["text"], "label": "", "note": tag})

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} posts to {args.out}")


if __name__ == "__main__":
    main()
