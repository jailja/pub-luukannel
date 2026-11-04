"""Build the static Luukannel site from the original chapter exports."""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "chapters"
CHAPTERS = ROOT / "chapters"
TITLE = "Luukannel"
AUTHOR = "Janne K. Jääskeläinen"
DESCRIPTION = "Luukannel on muinaiseen Suomeen sijoittuva fantasiaromaani. Lue kaikki 37 lukua maksutta verkossa."
EXPECTED_CHAPTERS = 37


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def read_chapters() -> list[dict[str, object]]:
    files = sorted(SOURCE.glob("*.md"))
    if len(files) != EXPECTED_CHAPTERS:
        raise ValueError(f"Expected {EXPECTED_CHAPTERS} chapters, found {len(files)}")
    chapters: list[dict[str, object]] = []
    for number, path in enumerate(files, 1):
        if path.name != f"{number:02d}.md":
            raise ValueError(f"Unexpected chapter file: {path.name}")
        raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        front = re.match(r"\A---\n(.*?)\n---\n", raw, re.S)
        if not front or f'title: "Luku {number}"' not in front.group(1):
            raise ValueError(f"Missing title for chapter {number}")
        body = raw[front.end():].strip()
        if not body:
            raise ValueError(f"Empty chapter {number}")
        chapters.append({
            "number": number,
            "title": f"Luku {number}",
            "filename": f"{number:02d}-luku-{number}.html",
            "body": body,
            "minutes": max(1, round(len(body.split()) / 230)),
        })
    return chapters


def head(page_title: str, *, depth: int) -> str:
    prefix = "../" if depth else ""
    full_title = f"{page_title} · {TITLE}" if page_title != TITLE else TITLE
    return f"""<!doctype html>
<html lang="fi" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0d1711">
  <meta name="description" content="{escape(DESCRIPTION)}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="{escape(full_title)}">
  <meta property="og:description" content="{escape(DESCRIPTION)}">
  <meta property="og:image" content="https://luukannel.net/assets/cover.png">
  <title>{escape(full_title)}</title>
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script defer src="{prefix}assets/site.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Siirry sisältöön</a>
"""


def header(*, depth: int, reader: bool = False) -> str:
    prefix = "../" if depth else ""
    toc = ('<button class="nav-button" id="toc-toggle" type="button" '
           'aria-controls="chapter-nav" aria-expanded="false">Sisällys</button>') if reader else ""
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="Luukannel, etusivu">
      <span class="brand-mark" aria-hidden="true">✧</span><span>Luukannel</span>
    </a>
    <div class="header-actions">{toc}
      <button class="theme-button" id="theme-toggle" type="button" aria-label="Vaihda vaaleaan teemaan" title="Vaihda teemaa"><span aria-hidden="true">☼</span></button>
    </div>
  </div>
</header>"""


def footer(*, depth: int) -> str:
    prefix = "../" if depth else ""
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <span>© {AUTHOR}</span>
    <span><a href="{prefix}index.html">Takaisin sisällykseen</a></span>
  </div>
</footer>"""


def chapter_link(chapter: dict[str, object], *, active: bool = False) -> str:
    number = int(chapter["number"])
    current = ' aria-current="page"' if active else ""
    return (f'<a class="sidebar-link{" is-active" if active else ""}" '
            f'href="{escape(str(chapter["filename"]))}"{current}>'
            f'<span class="sidebar-number">{number:02d}</span>'
            f'<span>{escape(str(chapter["title"]))}</span></a>')


def reader_page(chapter: dict[str, object], chapters: list[dict[str, object]]) -> str:
    number = int(chapter["number"])
    title = str(chapter["title"])
    nav = "\n".join(chapter_link(c, active=int(c["number"]) == number) for c in chapters)
    previous = chapters[number - 2] if number > 1 else None
    next_one = chapters[number] if number < len(chapters) else None
    nav_cards = ""
    if previous:
        nav_cards += (f'<a class="chapter-nav-card" href="{escape(str(previous["filename"]))}">'
                      f'<span>← Edellinen</span><strong>{escape(str(previous["title"]))}</strong></a>')
    if next_one:
        nav_cards += (f'<a class="chapter-nav-card is-next" href="{escape(str(next_one["filename"]))}">'
                      f'<span>Seuraava →</span><strong>{escape(str(next_one["title"]))}</strong></a>')
    body_html = markdown.markdown(str(chapter["body"]), extensions=["extra", "sane_lists"])
    page = head(title, depth=1)
    page += '<div class="reading-progress" id="reading-progress" aria-hidden="true"></div>'
    page += header(depth=1, reader=True)
    page += '<div class="reader-layout" id="reader-layout">'
    page += '<div class="sidebar-backdrop" id="sidebar-backdrop"></div>'
    page += (f'<aside class="reader-sidebar" id="chapter-nav" aria-label="Kirjan luvut">'
             f'<div class="sidebar-heading"><span>Fantasiaromaani</span><strong>{TITLE}</strong></div>'
             f'<nav class="sidebar-chapters">{nav}</nav></aside>')
    page += (f'<main id="main" class="reading-main" data-chapter="{number}">'
             f'<div class="reading-topline"><a href="../index.html">← Sisällys</a>'
             f'<span>Luku {number} / {len(chapters)}</span></div>'
             f'<article class="chapter-article"><header class="chapter-heading">'
             f'<p class="eyebrow">Luukannel · {number:02d}</p><h1>{escape(title)}</h1>'
             f'<div class="heading-rule" aria-hidden="true"><span>✧</span></div></header>'
             f'<div class="book-prose">{body_html}</div></article>'
             f'<nav class="chapter-next" aria-label="Lukujen välinen siirtyminen">{nav_cards}</nav>'
             f'</main></div>')
    page += footer(depth=1) + "\n</body>\n</html>\n"
    return page


def index_page(chapters: list[dict[str, object]]) -> str:
    chapter_cards = "\n".join(
        f'<li><a href="chapters/{escape(str(c["filename"]))}">'
        f'<span class="toc-number">{int(c["number"]):02d}</span>'
        f'<span class="toc-name">{escape(str(c["title"]))}</span>'
        f'<span class="toc-time">n. {int(c["minutes"])} min</span>'
        f'<span class="toc-arrow" aria-hidden="true">↗</span></a></li>'
        for c in chapters
    )
    page = head(TITLE, depth=0)
    page += header(depth=0)
    page += f"""<main id="main">
  <section class="hero" aria-labelledby="book-title">
    <div class="hero-stars" aria-hidden="true"></div>
    <div class="hero-inner">
      <div class="cover-wrap"><picture><source srcset="assets/cover.webp" type="image/webp"><img class="book-cover" src="assets/cover.png" alt="Luukannel-kirjan kansi" width="1600" height="2560" fetchpriority="high"></picture></div>
      <div class="hero-copy">
        <p class="eyebrow">Fantasiaromaani · 2009</p>
        <h1 id="book-title">Luukannel</h1>
        <p class="hero-author">{AUTHOR}</p>
        <div class="hero-description"><p>Muinaiseen Suomeen sijoittuva fantasiaromaani, jossa myytit, sota ja kohtalo kietoutuvat yhteen.</p></div>
        <div class="hero-buttons">
          <a class="button button-primary" href="chapters/01-luku-1.html">Aloita lukeminen <span aria-hidden="true">→</span></a>
          <a class="button button-secondary" href="#luvut">Selaa lukuja</a>
        </div>
        <p class="hero-note">Koko kirja luettavissa maksutta · 37 lukua</p>
        <p class="content-note">Sisältöhuomio: kirjassa kuvataan väkivaltaa ja seksuaalista väkivaltaa.</p>
      </div>
    </div>
  </section>
  <section class="toc-section" id="luvut" aria-labelledby="toc-title">
    <div class="section-heading"><p class="eyebrow">Koko tarina</p><h2 id="toc-title">Sisällys</h2>
      <p>Valitse luku tai aloita alusta. Viimeksi avattu luku tallentuu vain omaan selaimeesi.</p></div>
    <ol class="toc-grid">{chapter_cards}</ol>
  </section>
  <section class="end-note"><span aria-hidden="true">✧</span><p>37 lukua. Yksi tarina.</p></section>
</main>"""
    page += footer(depth=0) + "\n</body>\n</html>\n"
    return page


def main() -> None:
    chapters = read_chapters()
    CHAPTERS.mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(index_page(chapters), encoding="utf-8")
    for chapter in chapters:
        (CHAPTERS / str(chapter["filename"])).write_text(
            reader_page(chapter, chapters), encoding="utf-8"
        )
    print(f"Generated 1 landing page and {len(chapters)} chapters")


if __name__ == "__main__":
    main()
