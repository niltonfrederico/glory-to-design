# glory-to-design

СТАНДАРТ · the design system of the Mashinograd / NIRVYTEKH bureau suite
(`glory-to-*`, "g2"). Two surfaces, one voice: a **GUI** system (web, desktop and
mobile) and a **TUI** system (terminal). Everything else in the suite consumes
this repo; nothing here depends on any other repo.

## What lives here

| Path | What it is | Who reads it |
|---|---|---|
| `tokens/tokens.css` | GUI tokens, generated. Dark-first `:root`, `[data-theme="paper"]` variant. | web projects, Super Productivity / Obsidian themes |
| `tokens/tokens.toml` | TUI tokens, generated. Master trio + overrides, gensek `themes.toml` shape, plus the resolved table. | `glory-to-gensek`, `glory-to-protocol`, tuicr |
| `tokens/contrast-report.md` | Generated WCAG report for every load-bearing pair. | humans, before changing a seed |
| `tools/derive_tokens.py` | The only source of truth for colors. Edit seeds here, never in the generated files. | whoever changes the palette |
| `showcase/gui.html` | GUI system: spec and living showcase in one page. | published as a claude.ai artifact |
| `showcase/tui.html` | TUI system: spec and living showcase in one page. | published as a claude.ai artifact |
| `DESIGN.md` | Principles, decisions and their dates, what was rejected and why. | before proposing a change |
| `docs/canon.md` | The bureau's vocabulary, titles, documents, stamps, salutes, language rules. | before writing any public copy in the suite |
| `docs/references.md` | Eastern-bloc computing and print references, with sources. | when a new component needs a precedent |

## Rules of the house

- **Generated files are generated.** `tokens/*.css`, `tokens/*.toml` and the report
  come from `python3 tools/derive_tokens.py`. A hand edit there is overwritten on the
  next run and is a bug.
- **A color is a token or it does not exist.** Showcase pages and downstream repos
  speak only in semantic tokens (`bg`, `fg`, `accent`, `signal`, `ok`, `warn`…), never
  in hex. The one exception is the seed table inside the derivation script.
- **The derivation is the gensek one.** Master trio (`bg`, `fg`, `accent`) plus
  fixed overrides, every other token mixed in OKLab, contrast lifted to WCAG AA at
  load. The script mirrors `glory-to-gensek/src/theme/derive.rs` and the blog's
  `tokens.css`. If one changes, change the other.
- **Gate before done.** `python3 tools/derive_tokens.py` exits 1 when a load-bearing
  pair falls under its target. Do not lower a target to make it pass; change the seed.
- **Tone is the only sacred thing.** Palette, glyphs, components and layout are all
  negotiable; the deadpan state-bureau voice is not. `docs/canon.md` is the reference.
  Fake Cyrillic (Я for R) and hammer-and-sickle kitsch are out of canon.
- **Bureau voice in artifacts is project convention here.** This is a `glory-to-*`
  repo: public docs, SVGs and showcase copy may use the bureau register (Cyrillic
  labels, document numbers, stamps). Code identifiers, commit messages and file names
  stay plain technical English.
- **Bilingual public artifacts.** Anything meant for readers ships `*.md` (en-us) and
  `*.pt-br.md`, as in `glory-to-protocol`. Showcase pages are English with the
  bureau's Cyrillic labels; a pt-br toggle is a later layer.
- **Commits:** conventional, English. Branch + PR is not required in this repo yet;
  it is a documentation repo with no CI.

## How the surfaces relate

GUI and TUI share **seeds, semantics and voice**, not pixels. Same master trio, same
token names, same stamp vocabulary, same label grammar (`КИРИЛЛИЦА · English`). The
GUI renders frames as CSS borders and stamps as SVG; the TUI renders frames as
box-drawing glyphs and stamps as text blocks. When a component exists on one surface
and not the other, the spec says so instead of forcing a bad translation.

## Open items

- Legacy palettes still live in `glory-to-protocol` (slate `#16181d`) and
  `glory-to-gensek` (teal `#0b1f2a`). The canonical theme is the warm one from this
  repo; migration is per repo, on its own schedule. See `DESIGN.md` → Decisions.
- `docs/canon.md` records only what the suite's repos already state. The Tragedy and
  Norman's border-crossing origin are referenced in `glory-to-protocol/CLAUDE.md` but
  written nowhere. Ask Nilton; do not invent.
