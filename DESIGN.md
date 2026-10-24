# DESIGN — СТАНДАРТ

Principles, decisions and rejections of the g2 design system. `CLAUDE.md` says how the
repo works; this file says why it looks the way it does.

## Principles

1. **Tone is the only sacred thing.** Deadpan state-bureau voice (see `docs/canon.md`).
   Every other rule below can be overturned by a dated decision.
2. **Field quiet, accent as event.** The surface is warm near-black (or form paper).
   Gold marks focus, links and the active frame. Stamp red marks a decision or a fault.
   Nothing else is loud.
3. **Flat and straight.** No shadows, no radius, no gradients. Surfaces are stamped
   paper, not floating cards. Depth comes from the panel ramp (`bg → panel → panel_alt`)
   and from frame weight, never from blur.
4. **Frames carry state.** A heavy or double frame means focus or authority; a light
   single frame means rest. This is the one visual grammar both surfaces share
   literally: `┏━┓` and `┌─┐` in the TUI, 2px and 1px borders in the GUI.
5. **Mono is the chrome, not the prose.** Labels, headers, ledgers, keys, numbers and
   the whole TUI are monospace. GUI body text is a humanist sans with Cyrillic, because
   paragraphs in mono cost reading effort, and this suite is read by a dyslexic owner.
6. **Cyrillic is content, never texture.** Real words, the state's voice, always paired
   with English (`КИРИЛЛИЦА · English`). No faux Cyrillic, ever.
7. **Borrow grammar, not symbols.** F-key footer, classification corner, GOST-style
   field grid, numbered documents. No hammer and sickle, no real states or leaders.
8. **Constraint carries the mood.** Few colours, low detail, copy written to be
   skimmed. Restraint is what makes the deadpan land (Papers, Please; Disco Elysium).
9. **Modern to use, period to feel.** Buttons have hover and focus states, inputs have
   validation, layouts reflow to a phone. The era is in the type, the frames and the
   words, not in making the user suffer 1989 ergonomics.
10. **Accessible by construction.** Every token pair that carries text clears WCAG AA;
    body text clears AAA. The gate is `tools/derive_tokens.py`, run before done.

## Token model

Same model as `glory-to-gensek` §10 and the blog's `tokens.css`: a **master trio**
(`bg`, `fg`, `accent`) plus hand-fixed overrides, everything else derived in OKLab.

| Token | Derivation | Role |
|---|---|---|
| `bg_alt` / `panel` / `panel_alt` | mix(fg 4 / 8 / 13 %, bg) | surface ramp |
| `well` | bg, lightness −0.02 (−0.05 on paper) | deepest surface |
| `fg_bright` | fg moved 0.07 away from bg | headings |
| `muted` / `faint` | mix(fg 55 / 38 %, bg), lifted to 4.5 / 3.0 | secondary text |
| `accent_bright` | accent moved 0.12 away from bg | focus ring, hover |
| `accent_ink` | `well` or `fg_bright`, whichever reads better on accent | text on filled gold |
| `border` / `border_faint` | mix(accent 45 / 22 %, bg) | frames |
| `border_focus` | = accent | focused frame |
| `selection` | mix(accent 18 %, bg) | hovered / selected row |
| `signal` | fixed stamp red | graphics, large text (3:1) |
| `signal_text` | signal lifted to 4.5 | red at body size |
| `signal_bg` | mix(signal 14 %, bg) | rejected-row wash |
| `note` | hand-fixed sage, lifted to 4.5 against `note_bg` | the second hue |
| `note_bg` | mix(note 12 %, bg) | note wash |
| `ok` `warn` `bad` `info` | seeds lifted to 4.5 | state |

Why `signal` is split: `#c0392b` on the warm black measures about 3.4:1. That is fine
for a stamp ring or a 20px heading and not fine for a sentence. Rather than brighten
the stamp red everywhere (it would stop looking like ink), the text use gets its own
lifted token.

## Surfaces

**GUI** (web, desktop and mobile). Components: document header block, classification
corner, ledger (field grid), frame panel (rest / focus / authority), stamp (four
decisions + seal), button (filled gold, outline, ghost, danger), input with bracket
affordance, select, checkbox and radio drawn as `[ ]` `( )`, table ledger, navigation
rail with F-key hints, status bar, toast as a filed slip, dialog as a form (static and live), tabs as
folder tabs, badge, progress as a filled bar of blocks, empty state as a blank form, loading as
shade rows, search and filter chips, pager in sheets, figures as ledger rows, one-hue bar chart,
rendered prose (lists, tasks, quotes, code), print rules.

**TUI** (terminal). Components: header band with logo and session line, boxed panel
(three weights), section marker `▌`, ledger rows with dot leaders, stamp block, F-key
footer (10 slots), status line, command line `:`, inline edit box, list with `▸`
cursor, table, progress blocks `█▓▒░`, help-as-directive overlay, confirm as a form, modal over a
dimmed screen, command palette, scroll counts in the frame, narrow mode under 80 columns, boot
ledger, fatal error as a rejected form.

Shared: seeds, token names, stamp vocabulary, label grammar, frame weights, the
80-column ledger width (`FORM_WIDTH = 80` in protocol).

## Decisions

| Date | Decision | Alternatives rejected | Why |
|---|---|---|---|
| 2026-10-24 | Canonical background is the **warm near-black** `#0e0a05` (direktiva / zoloto-durakov). | gensek teal `#0b1f2a`; protocol slate `#16181d`; two official themes | Gold and cream read naturally on it; stamp red gains contrast; two surfaces (Obsidian vault, Super Productivity) already use it. Legacy palettes migrate per repo. |
| 2026-10-24 | **Dark canonical + `paper` as an opt-in theme.** No automatic light mode. | dark-only (direktiva's stance); automatic prefers-color-scheme | A paper form is in canon; a system-driven light mode is not. The user chooses. |
| 2026-10-24 | **Full bureau dose** on the GUI: frames on containers, stamps on status, screens as forms. | contained (stamps only on decisions); minimal (palette and type only) | Owner's call: err toward excess and trim later. Usability rules (principle 9) still hold. |
| 2026-10-24 | Design system lives in **`glory-to-design`**; its `CLAUDE.md` is the repo's own, not a parent for `_mashinograd`. | parent CLAUDE.md in `_mashinograd`; docs inside protocol | `_mashinograd` is a folder, not a repo. Canon vocabulary goes to `docs/canon.md` here. |
| 2026-10-24 | `note` is **hand-fixed sage** `#6fa86f`, not derived. | derive by rotating gold 140° (gives cyan) | Cyan is a second loud colour; the badge green already exists in protocol and gensek. |
| 2026-10-24 | GUI body in **PT Sans** (PT Serif on paper), chrome in **JetBrains Mono**. | all-mono; Inter / Space Grotesk | Mono paragraphs cost reading effort; PT faces are Cyrillic-first and free; JetBrains Mono is already the SVG stack. |
| 2026-10-24 | **Section headings carry the Cyrillic themselves** (`СВОДКА · One sheet…`), no eyebrow label above. | mono uppercase eyebrow + plain H2 | The protocol README does it this way; the eyebrow was a template reflex (frontend-design review). |
| 2026-10-24 | **Buttons are sentence case.** Uppercase stays on stamps, chips, focused frame titles, classification corners and ledger keys. | uppercase on every button | Our own principle says uppercase is semantic; buttons had no canon asking for it. |
| 2026-10-24 | **Figures use one hue.** A second series is a second chart; no categorical palette exists. | gold + sage + steel as series colours | Measured with the dataviz validator: gold↔sage ΔE 14.4 (normal vision, floor 15), steel below the chroma floor. |
| 2026-10-24 | **Print is paper**: `@media print` in the generated CSS applies the paper tokens. | a separate print stylesheet | The paper theme exists for printouts; one source. |
| 2026-10-24 | **Dose plena stays on the masthead** (logo, star, seal, ДСП corner, ОФИЦИАЛЬНО rule, seal again in the footer). | trim the footer rule and the masthead corner (frontend-design review) | Owner's call, second time asked. The review's "remove one accessory" is noted, not applied. |
| 2026-10-24 | **One motion in the system**: the masthead seal lands once on load (420 ms, transform only), off under `prefers-reduced-motion`. | no motion; also landing decision stamps | The review asked for one orchestrated moment; the stamp is the bureau's most characteristic gesture. Decision stamps stay still for now. |
| 2026-10-24 | GUI leans **office-PC tier** (CP866 box drawing, dialogs), TUI leans **terminal tier** (uppercase as semantic, one accent at a time). | blend both on every screen | One hardware tier per surface avoids anachronism (see `docs/references.md`). |

## Rejected for now, not forever

- ASCII-frame CSS overlays on third-party apps (Super Productivity): couples to unstable
  selectors. The direktiva DESIGN.md already parked this.
- A `legacy-slate` / `legacy-teal` theme shipped from this repo: the consuming repos
  already ship them; duplicating would create a second source of truth.
- Landing decision stamps on the GUI (after *File request*, say): protocol plans animated
  stamps for `0.5.0`; the GUI has the `.is-landing` keyframes on the masthead seal only.

## Migration notes for consuming repos

- **glory-to-protocol** `tui/theme.py`: replace the six Style constants with reads
  from `tokens.toml [resolved.bureau]`. `BORDER` → `border`, `HEADER` → `accent`,
  `BODY` → `fg`, `MUTED` → `muted`, `CYRILLIC_ACCENT` → `signal`, `SIGNATURE` →
  `faint`. Stamp colours → `ok`, `bad`, `info`, `warn`. SVG headers: `.bg` →
  `bg`, `.border` → `border`.
- **glory-to-gensek** `themes.toml`: add `[themes.bureau]` from this repo's toml as the
  default; keep `gensek` (teal) shipped for anyone who prefers it.
- **glory-to-direktiva** `nirvytekh.css`: already on the warm palette. Replace the
  `--nv-*` block with `@import` of `tokens.css` and alias `--nv-* → --g2-*`.
