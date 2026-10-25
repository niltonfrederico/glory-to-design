# glory-to-design

СТАНДАРТ · the design system of the Mashinograd / NIRVYTEKH bureau suite
(`glory-to-*`, "g2"). Four surfaces, one voice: a **GUI** system (web, desktop and
mobile), a **TUI** system (terminal), a **WATCH** system (Wear OS, the wrist) and an
**OBSIDIAN** system (the vaults).
Everything else in the suite consumes this repo; nothing here depends on any other repo.

## What lives here

| Path | What it is | Who reads it |
|---|---|---|
| `tokens/tokens.css` | GUI tokens, generated. Dark-first `:root`, `[data-theme="paper"]` variant. | web projects, Super Productivity / Obsidian themes |
| `tokens/tokens.toml` | TUI tokens, generated. Master trio + overrides, gensek `themes.toml` shape, plus the resolved table. | `glory-to-gensek`, `glory-to-protocol`, tuicr |
| `tokens/tokens.kt` | Watch / Compose tokens, generated. One Kotlin `object` per theme; Material 3 fold in the header. | the future Wear OS app; any Compose consumer |
| `tokens/tokens.obsidian.css` | Obsidian tokens, generated. g2 tokens on `.theme-dark` / `.theme-light`, Obsidian's CSS variable contract mapped onto them. | `glory-to-kartoteka` (the theme repo), which vendors it and bundles its component layer on top |
| `tokens/contrast-report.md` | Generated WCAG report for every load-bearing pair. | humans, before changing a seed |
| `tools/derive_tokens.py` | The only source of truth for colors. Edit seeds here, never in the generated files. | whoever changes the palette |
| `tools/align_term.py` | Normalizes the `<pre class="term">` mockups in `showcase/tui.html`: column-exact frames, fixed-width glyph cells. `--check` is the gate. | whoever edits a terminal mockup |
| `showcase/gui.html` | GUI system: spec and living showcase in one page. | published as a claude.ai artifact |
| `showcase/tui.html` | TUI system: spec and living showcase in one page. | published as a claude.ai artifact |
| `showcase/watch.html` | WATCH system (Wear OS, Galaxy Watch6 Classic 47 mm): spec and living showcase, 240 dp discs at 1 px = 1 dp. | published as a claude.ai artifact |
| `showcase/obsidian.html` | OBSIDIAN system: spec and living showcase. Mock windows use Obsidian's real class names with the real theme loaded on top (`showcase/obsidian.css`, written by `glory-to-kartoteka/tools/build.py --showcase`: theme + snippets). | published as a claude.ai artifact |
| `DESIGN.md` | Principles, decisions and their dates, what was rejected and why. | before proposing a change |
| `docs/canon.md` | The bureau's vocabulary, titles, documents, stamps, salutes, language rules. | before writing any public copy in the suite |
| `docs/references.md` | Eastern-bloc computing and print references, with sources. | when a new component needs a precedent |

## Rules of the house

- **Generated files are generated.** `tokens/*.css`, `tokens/*.toml`, `tokens/*.kt`, the
  report and `showcase/tokens.css` come from `python3 tools/derive_tokens.py`;
  `showcase/obsidian.css` comes from `glory-to-kartoteka/tools/build.py --showcase`. A hand
  edit in any of them is overwritten on the next run and is a bug. The Obsidian theme itself
  (component layer, snippets, installer) lives in `glory-to-kartoteka`, not here.
- **A color is a token or it does not exist.** Showcase pages and downstream repos
  speak only in semantic tokens (`bg`, `fg`, `accent`, `signal`, `ok`, `warn`…), never
  in hex. The one exception is the seed table inside the derivation script.
- **The derivation is the gensek one.** Master trio (`bg`, `fg`, `accent`) plus
  fixed overrides, every other token mixed in OKLab, contrast lifted to WCAG AA at
  load. The script mirrors `glory-to-gensek/src/theme/derive.rs` and the blog's
  `tokens.css`. If one changes, change the other.
- **Gate before done.** `python3 tools/derive_tokens.py` exits 1 when a load-bearing
  pair falls under its target. Do not lower a target to make it pass; change the seed.
- **Terminal mockups are column-exact.** After editing any `<pre class="term">` block,
  run `python3 tools/align_term.py` (rewrites) and `--check` (gate). Glyphs outside
  JetBrains Mono (`✓ ✗ ★ ▸ ● ■ ⏎`) must sit in `<i class="g">`; the script does it.
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

GUI, TUI, WATCH and OBSIDIAN share **seeds, semantics and voice**, not pixels. Same master trio,
same token names, same stamp vocabulary, same label grammar (`КИРИЛЛИЦА · English`).
The GUI renders frames as CSS borders and stamps as SVG; the TUI renders frames as
box-drawing glyphs and stamps as text blocks; the WATCH renders square frames inside a
round case, one decision per disc, and keeps always-on under 15 % lit pixels; the OBSIDIAN surface sets everything it can
through Obsidian's own CSS variable contract and touches plugin DOM only in snippets. When a
component exists on one surface and not the others, the spec says so instead of
forcing a bad translation.

## Open items

- The Obsidian theme moved to `glory-to-kartoteka` on 2026-10-25, the day it was written.
  Install and deploy state live in that repo's `CLAUDE.md`. When a seed changes here, run
  `derive_tokens.py`, then `glory-to-kartoteka/tools/build.py --showcase` so the spec page's
  `showcase/obsidian.css` and the theme stay on the same tokens.
- Legacy palettes still live in `glory-to-protocol` (slate `#16181d`) and
  `glory-to-gensek` (teal `#0b1f2a`). The canonical theme is the warm one from this
  repo; migration is per repo, on its own schedule. See `DESIGN.md` → Decisions.
- `docs/canon.md` records only what the suite's repos already state. The Tragedy and
  Norman's border-crossing origin are referenced in `glory-to-protocol/CLAUDE.md` but
  written nowhere. Ask Nilton; do not invent.
