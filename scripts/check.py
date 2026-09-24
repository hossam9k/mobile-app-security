#!/usr/bin/env python3
"""Structural checks for the book. Exit status is non-zero if anything fails.

    python3 scripts/check.py           # structure + code syntax
    python3 scripts/check.py --mermaid # also render every Mermaid diagram

Checks:
  * every code fence is closed and carries a language tag
  * every "§x.y" and "Chapter N" reference resolves to a heading
  * section numbers under each chapter match the chapter number
  * every Mermaid diagram has a "*Figure N: title*" caption, numbered in order
  * the repository's own workflows pass actionlint
  * Swift blocks parse (swiftc -parse), XML blocks are well formed (xmllint),
    GitHub workflow YAML passes actionlint; each only if the tool is installed
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = sorted((ROOT / "book").glob("*.md")) + sorted(ROOT.glob("*.md"))
FENCE = re.compile(r"^(\s*)(```+|~~~+)(.*)$")
CHAPTER_H = re.compile(r"^## Chapter (\d+(?:\.\d+)?)\b")
SECTION_H = re.compile(r"^### (\d+)\.(\d+)\b")
SECTION_REF = re.compile(r"§\s?(\d+)\.(\d+)(?!\d|\.\d)")  # three-level numbers are external (CDD, BR)
CHAPTER_REF = re.compile(r"\bChapters? (\d+(?:\.\d+)?(?:(?:,\s*|\s*(?:–|-|to|and|or)\s*)\d+(?:\.\d+)?)*)")
REF_NUMBER = re.compile(r"\d+(?:\.\d+)?")
CAPTION = re.compile(r"^\*Figure (\d+): \S.*\*$")
ORDER = ["start-here.md"] + [f"{i:02d}-" for i in range(13)]

problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


def blocks(path: Path):
    """Yield (language, first_line_no, code) for every fenced block."""
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        marker, lang, start = m.group(2), m.group(3).strip(), i + 1
        j = i + 1
        while j < len(lines) and not re.match(rf"^\s*{re.escape(marker)}\s*$", lines[j]):
            j += 1
        if j == len(lines):
            fail(f"{path.name}:{start}: unclosed code fence")
            return
        yield lang, start, "\n".join(lines[i + 1:j])
        i = j + 1


def prose_lines(path: Path):
    in_fence = False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            yield n, line


def resolves(ref: str, chapters: set[str], sections: set[tuple[int, int]]) -> bool:
    """"12", "0.5" (a Part 0 chapter) and "8.6" (a section) are all valid targets."""
    if ref in chapters:
        return True
    if "." in ref:
        major, minor = map(int, ref.split("."))
        return (major, minor) in sections
    return False


def check_structure() -> None:
    chapters: set[str] = set()
    sections: set[tuple[int, int]] = set()
    for path in FILES:
        if path.parent.name != "book":
            continue
        current = None
        for n, line in prose_lines(path):
            if m := CHAPTER_H.match(line):
                current = m.group(1)
                chapters.add(current)
            elif m := SECTION_H.match(line):
                chap, sec = int(m.group(1)), int(m.group(2))
                sections.add((chap, sec))
                if current is not None and str(chap) != current:
                    fail(f"{path.name}:{n}: section {chap}.{sec} sits under Chapter {current}")
    for path in FILES:
        for n, line in prose_lines(path):
            for m in SECTION_REF.finditer(line):
                if not resolves(f"{m.group(1)}.{m.group(2)}", chapters, sections):
                    fail(f"{path.name}:{n}: §{m.group(1)}.{m.group(2)} has no matching heading")
            for m in CHAPTER_REF.finditer(line):
                for ref in REF_NUMBER.findall(m.group(1)):
                    if not resolves(ref, chapters, sections):
                        fail(f"{path.name}:{n}: Chapter {ref} has no matching heading")


def check_figures() -> None:
    """Every diagram carries a caption line, and figures are numbered 1..N in reading order."""
    expected = 1
    book = [p for p in FILES if p.parent.name == "book"]
    book.sort(key=lambda p: (p.name != "start-here.md", p.name))
    for path in book:
        lines = path.read_text(encoding="utf-8").splitlines()
        for lang, start, code in blocks(path):
            if lang != "mermaid":
                continue
            end = start + code.count("\n") + 1          # line index of the closing fence
            after = next((l.strip() for l in lines[end + 1:end + 3] if l.strip()), "")
            m = CAPTION.match(after)
            if not m:
                fail(f"{path.name}:{start}: diagram has no '*Figure N: title*' caption under it")
            elif int(m.group(1)) != expected:
                fail(f"{path.name}:{start}: caption says Figure {m.group(1)}, expected Figure {expected}")
            expected += 1


def check_workflows() -> None:
    if shutil.which("actionlint"):
        for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
            run(["actionlint", str(wf)], wf.name)


def check_fences() -> None:
    for path in FILES:
        for lang, start, _ in blocks(path):
            if not lang:
                fail(f"{path.name}:{start}: code fence has no language tag")


def run(cmd: list[str], label: str) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        fail(f"{label}: " + " | ".join(detail[:4]))


def check_code(render_mermaid: bool) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="book-check-"))
    have = {tool: shutil.which(tool) for tool in ("swiftc", "xmllint", "actionlint", "npx")}
    for path in FILES:
        for lang, start, code in blocks(path):
            label = f"{path.name}:{start} ({lang})"
            stem = tmp / f"{path.stem}-{start}"
            if lang == "swift" and have["swiftc"]:
                src = stem.with_suffix(".swift")
                src.write_text(code)
                run(["swiftc", "-parse", str(src)], label)
            elif lang == "xml" and have["xmllint"]:
                src = stem.with_suffix(".xml")
                # "..." marks elided attributes or children in the prose.
                body = re.sub(r"<\?xml[^>]*\?>", "", code).replace("...", "")
                # Fragments may have several roots and use the android: prefix undeclared.
                src.write_text(
                    '<fragment xmlns:android="http://schemas.android.com/apk/res/android" '
                    'xmlns:tools="http://schemas.android.com/tools" '
                    'xmlns:app="http://schemas.android.com/apk/res-auto">'
                    f"{body}</fragment>"
                )
                run(["xmllint", "--noout", str(src)], label)
            elif lang in ("yaml", "yml") and have["actionlint"] and re.search(r"^jobs:", code, re.M) and re.search(r"^on:", code, re.M):
                src = stem.with_suffix(".yml")
                src.write_text(code)
                run(["actionlint", "-shellcheck=", "-pyflakes=", str(src)], label)
            elif lang == "mermaid" and render_mermaid and have["npx"]:
                src = stem.with_suffix(".mmd")
                src.write_text(code)
                run(["npx", "-y", "@mermaid-js/mermaid-cli@11", "-q", "-i", str(src),
                     "-o", str(stem.with_suffix(".svg"))], label)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mermaid", action="store_true", help="render every Mermaid block")
    args = parser.parse_args()
    check_fences()
    check_figures()
    check_structure()
    check_workflows()
    check_code(args.mermaid)
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
