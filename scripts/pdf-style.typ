// Typst rules injected by scripts/build.py (pandoc --include-in-header).
#show heading.where(level: 1): it => { pagebreak(weak: true); it }
#show link: set text(fill: rgb("#1a5fb4"))
#show raw.where(block: true): set text(size: 8pt)
#show raw.where(block: true): block.with(fill: rgb("#f6f8fa"), inset: 8pt, radius: 3pt, width: 100%)
#show quote: set block(fill: rgb("#fff8e6"), inset: 8pt, radius: 3pt)
#set table(stroke: 0.5pt + rgb("#c0c0c0"))
#show table: set text(size: 8.5pt)
#show table.cell: set align(left + top)
#show table: set par(justify: false)
#show image: it => align(center, it)
// Long identifiers in table cells: allow a line break after any character.
#show table.cell: it => {
  show raw.where(block: false): r => text(font: "DejaVu Sans Mono", size: 0.9em, r.text.clusters().join(sym.zws))
  it
}
#show figure.caption: set text(size: 9pt, style: "italic", fill: rgb("#4A5568"))
#show figure: set block(above: 1.2em, below: 1.4em)
