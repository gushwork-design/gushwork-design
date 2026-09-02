#!/usr/bin/env python3
"""
Builds search-index.json for the hosted site.

    python3 scripts/_search_index.py <stage-dir> > <stage-dir>/search-index.json

GENERATED FROM THE STAGED COPIES, NEVER FROM THE REPO. publish-sheets.sh assembles the deploy
in a temp directory — sheets renamed to their routes, the shell injected — and this reads THAT.
Indexing the repo instead would index files whose URLs do not exist and miss the renames, and
the index would drift from the deploy the first time a route changed. Same reason the changelog
is derived from git rather than hand-written: a second source of truth is a source of drift.

An entry is one anchor a reader can land on:

    p  page title        "Style Guide"
    u  page url          "/style-guide"
    t  heading           "Colors"
    a  anchor            "#colors"       (empty when the heading has no id)
    s  snippet           the text under that heading, trimmed

Keys are one letter because this ships to every visitor on first search.
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

# route -> human page name, in sidebar order so results read in a familiar order
PAGES = [
    ("index.html",                 "/",                       "Overview"),
    ("style-guide.html",           "/style-guide",            "Style Guide"),
    ("downloads.html",             "/downloads",              "Downloads"),
    ("internal/claude-plugin.html", "/internal/claude-plugin", "Claude Plugin"),
    ("internal/mini-tools.html",   "/internal/mini-tools",    "Mini Tools"),
    ("internal/changelog.html",    "/internal/changelog",     "Change Log"),
]

HEADINGS = ("h1", "h2", "h3")
SKIP = ("script", "style", "svg", "nav")


class Reader(HTMLParser):
    """Flattens a page into (kind, id, text) so a heading can own the text that follows it."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self._skip = 0
        self._tag = None
        self._id = None
        self._buf = []
        self._depth = 0
        # The id a heading should link to is usually NOT on the heading. The styleguide puts it
        # on <section id="concept">, the changelog on the release block. So remember the last
        # container id seen and let a heading without its own id inherit it.
        self._container_id = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        cls = a.get("class", "")
        if tag in ("section", "article", "div") and a.get("id"):
            self._container_id = a["id"]
        if tag in HEADINGS or "body__sum" in cls:
            self._flush()
            self._tag = "h" if tag in HEADINGS else "rel"
            self._id = a.get("id") or self._container_id
        elif tag in ("p", "li", "pre", "div"):
            self._flush_text()

    def handle_endtag(self, tag):
        if tag in SKIP and self._skip:
            self._skip -= 1
            return
        if tag in HEADINGS or tag in ("p", "li", "pre"):
            self._flush()

    def handle_data(self, d):
        if not self._skip:
            self._buf.append(d)

    def _text(self):
        return re.sub(r"\s+", " ", "".join(self._buf)).strip()

    def _flush(self):
        t = self._text()
        if t:
            self.out.append((self._tag or "t", self._id, t))
        self._buf = []
        self._tag = None
        self._id = None

    def _flush_text(self):
        t = self._text()
        if t:
            self.out.append(("t", None, t))
        self._buf = []


def sections(path):
    r = Reader()
    r.feed(open(path, encoding="utf-8").read())
    r._flush()
    out, cur = [], None
    for kind, ident, text in r.out:
        if kind in ("h", "rel"):
            if cur:
                out.append(cur)
            cur = {"t": text, "a": ("#" + ident) if ident else "", "s": []}
        elif cur is not None:
            cur["s"].append(text)
    if cur:
        out.append(cur)
    for s in out:
        # one snippet, capped — enough to match on and to show, not enough to bloat the file
        s["s"] = re.sub(r"\s+", " ", " ".join(s["s"]))[:400].strip()
    return out


def main():
    stage = sys.argv[1]
    index = []
    for rel, url, name in PAGES:
        p = os.path.join(stage, rel)
        if not os.path.exists(p):
            print("  search: no %s, skipped" % rel, file=sys.stderr)
            continue
        n = 0
        for s in sections(p):
            if not s["t"]:
                continue
            index.append({"p": name, "u": url, "t": s["t"], "a": s["a"], "s": s["s"]})
            n += 1
        print("  search: %-24s %3d entries" % (name, n), file=sys.stderr)
    json.dump(index, sys.stdout, separators=(",", ":"), ensure_ascii=False)


if __name__ == "__main__":
    main()
