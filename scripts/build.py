#!/usr/bin/env python3
"""Build the single-file Markdown and the PDF from book/*.md.

    python3 scripts/build.py            # single-file MD + PDF
    python3 scripts/build.py --md-only  # single-file MD only

Requires, for the PDF: pandoc >= 3.1, typst, and Node (npx) for
@mermaid-js/mermaid-cli, which renders Mermaid diagrams to PNG.
"""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
DIST = ROOT / "dist"
CACHE = ROOT / "build" / "diagrams"
DIAGRAMS = ROOT / "dist" / "diagrams"

ORDER = [
    "start-here.md",
    "00-foundations.md",
    "01-understanding-the-threat.md",
    "02-data-at-rest.md",
    "03-data-in-transit.md",
    "04-proving-who-is-calling.md",
    "05-resilience.md",
    "06-the-build-and-release-pipeline.md",
    "07-platform-surfaces-and-new-frontiers.md",
    "08-practice.md",
    "09-the-catalogues.md",
    "10-questions-and-answers.md",
    "11-making-the-case-and-running-the-programme.md",
    "12-verification.md",
]

SINGLE_MD = DIST / "Mobile-Application-Security-single-file.md"
PDF = DIST / "Mobile-Application-Security.pdf"
MERMAID_CLI = "@mermaid-js/mermaid-cli@11.17.0"  # pinned: output must not change under you

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n+", re.S)
FENCE = re.compile(r"^(```|~~~)")
# The body may not contain a fence, so an uncaptioned block cannot swallow the text after it.
MERMAID_WITH_CAPTION = re.compile(r"^```mermaid\n((?:(?!^```).)*?)^```\n\n\*Figure (\d+): (.+?)\*\n", re.S | re.M)
SCALE = 3
MAX_FIGURE_PT = 480.0         # A4 text width with 2 cm margins
MAX_FIGURE_HEIGHT_PT = 640.0  # leaves room for the caption on the page
# ](file.md), ](book/file.md#anchor), ](../.github/ISSUE_TEMPLATE/x.md) and similar relative links
LOCAL_LINK = re.compile(r"\]\((?:\.\./)?((?:[\w.-]+/)*[\w.-]+\.md)(#[^)\s]*)?\)")


def github_slug(heading: str) -> str:
    """Anchor GitHub generates for a heading (close enough for our headings)."""
    text = re.sub(r"[*_`]", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def first_h1(markdown: str) -> str:
    in_fence = False
    for line in markdown.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and line.startswith("# "):
            return line[2:]
    raise ValueError("part has no top-level heading")


def last_verified() -> date:
    """Newest `last_verified` date across the parts, so rebuilding unchanged sources is reproducible."""
    dates = re.findall(r"^last_verified: (\d{4}-\d{2}-\d{2})$",
                       "\n".join((BOOK / n).read_text(encoding="utf-8") for n in ORDER), re.M)
    return max(date.fromisoformat(d) for d in dates)


def load_parts() -> list[tuple[str, str]]:
    parts = []
    for name in ORDER:
        path = BOOK / name
        if not path.exists():
            sys.exit(f"missing {path}")
        parts.append((name, FRONTMATTER.sub("", path.read_text(encoding="utf-8"), count=1)))
    return parts


def rewrite_links(markdown: str, part_anchor: dict[str, str]) -> str:
    """Turn links between part files into in-document anchors."""

    def repl(m: re.Match[str]) -> str:
        target, anchor = m.group(1).removeprefix("book/"), m.group(2)
        if target in part_anchor:
            return f"]({anchor or '#' + part_anchor[target]})"
        # Root files (README, VERIFICATION, …) are not in the single file: link to GitHub.
        return f"](https://github.com/hossam9k/mobile-app-security/blob/main/{target}{anchor or ''})"

    return LOCAL_LINK.sub(repl, markdown)


def build_single_md() -> str:
    parts = load_parts()
    anchors = {name: github_slug(first_h1(body)) for name, body in parts}
    body = "\n\n---\n\n".join(rewrite_links(md.strip(), anchors) for _, md in parts) + "\n"
    SINGLE_MD.write_text(body, encoding="utf-8")
    print(f"wrote {SINGLE_MD.relative_to(ROOT)} ({len(body.split()):,} words)")
    return body


def figure_width_pt(png: Path) -> float:
    """Print width for a diagram: its natural size, so every diagram shares one text size,
    shrunk only as far as needed to fit the text block."""
    width_px, height_px = struct.unpack(">II", png.read_bytes()[16:24])
    width, height = width_px / SCALE * 0.75, height_px / SCALE * 0.75
    return round(min(width, MAX_FIGURE_PT, width * MAX_FIGURE_HEIGHT_PT / height), 1)


def render_mermaid(markdown: str) -> str:
    """Replace each Mermaid block and its caption line with a numbered PNG figure.

    Every diagram is rendered once (cached by content hash) with the house theme in
    scripts/mermaid-config.json, and a named copy is written to dist/diagrams/.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    for old in DIAGRAMS.glob("figure-*.png"):
        old.unlink()
    config = ROOT / "scripts" / "mermaid-config.json"
    css = ROOT / "scripts" / "mermaid.css"
    salt = config.read_bytes() + css.read_bytes()

    def repl(m: re.Match[str]) -> str:
        source, number, title = m.group(1), m.group(2), m.group(3)
        digest = hashlib.sha256(salt + source.encode()).hexdigest()[:16]
        png = CACHE / f"{digest}.png"
        if not png.exists():
            mmd = CACHE / f"{digest}.mmd"
            mmd.write_text(source, encoding="utf-8")
            subprocess.run(
                ["npx", "-y", MERMAID_CLI, "-q", "-i", str(mmd), "-o", str(png),
                 "-c", str(config), "-C", str(css), "-s", str(SCALE), "-w", "1400", "-b", "white"],
                check=True,
            )
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
        shutil.copyfile(png, DIAGRAMS / f"figure-{int(number):02d}-{slug}.png")
        width = figure_width_pt(png)
        # A lone image with alt text becomes a numbered figure; typst adds "Figure N:".
        return f"![{title}]({png}){{width={width}pt}}\n"

    out = MERMAID_WITH_CAPTION.sub(repl, markdown)
    if "```mermaid" in out:
        sys.exit("a Mermaid block has no '*Figure N: title*' caption line under it")
    return out


def build_pdf(single_md: str) -> None:
    for tool in ("pandoc", "typst", "npx"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found; install it or run with --md-only")
    source = ROOT / "build" / "book-for-pdf.md"
    source.parent.mkdir(exist_ok=True)
    # The PDF gets its title page from pandoc metadata, so drop the Markdown title block.
    body = re.sub(r"\A# .*?\n(?=## )", "", single_md, count=1, flags=re.S)
    source.write_text(render_mermaid(body), encoding="utf-8")
    subprocess.run(
        [
            "pandoc", str(source),
            "--from", "gfm+gfm_auto_identifiers+attributes+implicit_figures",
            "--to", "pdf",
            "--pdf-engine", "typst",
            "--toc", "--toc-depth", "2",
            "--metadata", "title=Mobile Application Security",
            "--metadata", "subtitle=A Study Book for Engineers",
            "--metadata", "author=Hossam Atef",
            "--metadata", f"date=Edition 1 · revised {last_verified():%-d %B %Y}",
            "--variable", "lang=en",
            "--variable", "region=GB",
            "--variable", "papersize=a4",
            "--variable", "fontsize=10pt",
            "--variable", "margin.x=2cm",
            "--variable", "margin.y=2.2cm",
            "--variable", "section-numbering=",
            "--include-in-header", str(ROOT / "scripts" / "pdf-style.typ"),
            "--resource-path", str(ROOT),
            "--output", str(PDF),
        ],
        check=True,
    )
    print(f"wrote {PDF.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--md-only", action="store_true", help="skip the PDF")
    args = parser.parse_args()
    DIST.mkdir(exist_ok=True)
    single_md = build_single_md()
    if not args.md_only:
        build_pdf(single_md)


if __name__ == "__main__":
    main()
