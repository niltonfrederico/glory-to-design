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

**WATCH** (Wear OS, Galaxy Watch6 Classic 47 mm first). Canvas 240 × 240 dp (480 px at
density 2); text and ledgers inside the inscribed square (170 dp), the outer 12 dp for
rules and the rim date only. Components: ledger face and stamp face, duty (always-on)
state, tiles as single sheets, voice-note recording / filed slip / shelf, treasury due
notice / overdue / receipt, notification slip (label + body + meta + two 48 dp
actions), task list / sheet / stamped empty state, system board (five rows, glyph +
word + colour), input ledger (bezel = cursor, swipe right = back, hold = confirm).
No new tokens; two new usage rules (duty state, square frames in a round case).

**OBSIDIAN** (the vaults: `_ideas`, `the.hunt`, `zoloto-durakov`). The one host with a
token contract of its own: `tokens/tokens.obsidian.css` (generated) puts the g2 tokens on
`.theme-dark` (bureau) and `.theme-light` (paper) and maps Obsidian's CSS variables onto
them once, with the accent as HSL, every token as an RGB triple and the extended palette
folded onto the bureau's hues. `obsidian/src/theme.css` is the component layer, bundled
by the generator into the installable `obsidian/theme.css`. Components: the sheet
(headings mono with rules, body in the system face, blockquote as a note, code in the
well), properties as the document header, tables as ledgers, tags as outline chips,
callouts as stamped notices (`[!approved]` `[!rejected]` `[!order]` `[!review]`, plus
the usual types folded onto six colours), window chrome on the well / panel / field ramp,
menus and modals as framed forms, notice as a filed slip, empty pane as a blank form.
Plugin layers are snippets, one per plugin: `g2-kanban` (despatch board, lane colour
through `--g2-lane`), `g2-bases` (filterable ledger, decision words in stamp colours),
`g2-dataview` (inline fields, error as a rejected form). No new tokens.

Shared: seeds, token names, stamp vocabulary, label grammar, frame weights, the
80-column ledger width (`FORM_WIDTH = 80` in protocol). The watch adds the 48 dp
target, the 32 dp list row, the 18-character top label (the chord 22 dp under the rim)
and the 12 / 10 sp text floors from the Wear OS quality guidelines.

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
| 2026-10-24 | **Third surface: WATCH**, Galaxy Watch6 Classic 47 mm as the reference device, Compose for Wear OS as the app stack. | phone-first mobile spec; a generic "wearable" section inside the GUI page | Owner's call: a design standard for the device on the wrist is the bait for an app. The GUI page already covers mobile web; the wrist has its own geometry, input and power budget. |
| 2026-10-24 | **Frames stay square inside the round canvas.** The circle is the case, not the design. Curved text only for the rim date on a watch face. | round cards and ring progress (Material 3 for Wear); curved labels everywhere | The bureau has no rounded corners on any surface; bending the forms to the glass would make the watch a different system. Ring progress is the bezel's job. |
| 2026-10-24 | **Always-on is a usage rule, not a theme**: text on `well`, regular weight, `accent` + `muted` + `faint`, no fills, no stamps, under 15 % on-pixel ratio. Paper has no duty state. | a derived `aod` theme in the seed table; dimming the bureau theme | Samsung's Watch Face Studio rejects faces over 15 % OPR; a theme would invite fills. The rule keeps positions fixed so nothing jumps when the wrist lifts. |
| 2026-10-24 | **The watch types nothing.** Tasks are checked, deferred or dictated; voice notes are numbered, not titled; text is written on the phone. | an on-watch keyboard; on-watch transcription in the UI | 240 dp cannot carry a keyboard and the bureau's voice; dictation is the inline edit box of the wrist. Transcription may arrive later from the phone. |
| 2026-10-24 | **Two actions per disc, same pair for the same question** (done · defer, play · discard, hand-off · dismiss), primary on the left. | three-button rows; swipe actions as the only path | One screen, one decision. A fixed pair is learnable blind, which is how a watch is used. |
| 2026-10-25 | **Tap confirms; hold (1 s) is reserved for destructive actions.** The ✓ on treasury, tasks and notifications is a tap, also where it asserts a fact the app cannot verify ("paid"). | hold-to-stamp on fact assertions (gold fills the 48 dp square over 1 s, then the ОДОБРЕНО stamp lands); hold on every ✓ | Owner's call for the initial version, with the stated worry that an impulsive tap files something by mistake. Tap is the Wear OS convention and keeps the task list fast. Revisit after real use; the hold-to-stamp design is kept below. |
| 2026-10-25 | **Fourth surface: OBSIDIAN**, replacing the June `Nirvytekh` theme (hand palette, serif body, dark only) that ran in every registered vault. | keep the vault theme as a consumer outside the system; restyle each vault with snippets only | Owner's call. The vault is read more than any other surface; seven hand-copied theme folders had already drifted from the tokens. The theme name stays `Nirvytekh`. |
| 2026-10-25 | **The Obsidian theme lives in its own repo, `glory-to-kartoteka`.** This repo keeps the spec (`showcase/obsidian.html`) and emits the contract (`tokens/tokens.obsidian.css`), as it does for the watch; the theme repo vendors the contract and bundles its component layer on top. | theme, snippets and installer inside this repo (chosen earlier the same day, reverted on the owner's call); the source in `zoloto-durakov/_code` | One theme repo per host app is the suite's pattern (`glory-to-direktiva` for Super Productivity). The design repo stays a standard, not a product. |
| 2026-10-25 | **Body text in Obsidian follows the system**: PT Sans on the bureau, PT Serif on paper. | keep IBM Plex Serif as a surface exception (the June choice, "legible in long sessions") | Principle 5 was written for a dyslexic reader and the vault is where the long sessions happen. Serif remains on paper, which is where the June reasoning holds. |
| 2026-10-25 | **`.theme-light` is paper.** The user picks it in Settings › Appearance; "adapt to system" is left off. | dark only, `.theme-light` repainted dark (the direktiva stance) | Obsidian's switch is the opt-in the system asks for. Repainting light as dark hides a user choice. |
| 2026-10-25 | **Contract first, selectors second; plugin DOM only in snippets.** `--radius-*`, `--shadow-*`, fonts, every colour slot go through Obsidian's variables; Kanban, Bases and Dataview get one defensive snippet each. | component selectors everywhere (the June theme); plugin rules inside the theme | The contract is Obsidian's stable surface; plugin markup is not. A plugin update breaks one snippet, not the vault. |
| 2026-10-25 | **Tags are outline chips; blockquotes are notes.** No gold-filled tags in running text; the quote takes `note`, not `signal`. | the June theme's filled gold tags and red quote rule | Field quiet, accent as event (principle 2); red marks a decision and a quotation decides nothing. |
| 2026-10-25 | **Kanban lane colour is a vault decision** exposed as `--g2-lane`; the system snippet sets structure only. The vault maps its columns to the stamp grammar in its own snippet, tokens only. | colouring lanes 1..n from this repo; a `g2-hunt.css` here | The lane vocabulary belongs to the board. `the.hunt`'s `hunt-style.css` (slate, violet, blue, amber, green in raw hex) is the migration target, not a template. |
| 2026-10-24 | **Red is a rejection, not an overdue amount.** Overdue is К СВЕДЕНИЮ in `warn`. | red figures for late payments (every banking app) | The stamp grammar is the state grammar; the citizen who is late has been reminded, not rejected. |
| 2026-10-24 | **`tokens/tokens.kt` is generated** alongside the CSS and TOML: one Kotlin `object` per theme, Material 3 fold documented in the header. Watch Face Format has no variables and copies hex by hand from `tokens.toml`. | hand-written `Color.kt` in the future app repo | A color is a token or it does not exist; the app must read the same generated table as the web and the terminal. |

## Rejected for now, not forever

- ASCII-frame CSS overlays on third-party apps (Super Productivity): couples to unstable
  selectors. The direktiva DESIGN.md already parked this.
- A `legacy-slate` / `legacy-teal` theme shipped from this repo: the consuming repos
  already ship them; duplicating would create a second source of truth.
- Landing decision stamps on the GUI (after *File request*, say): protocol plans animated
  stamps for `0.5.0`; the GUI has the `.is-landing` keyframes on the masthead seal only.
- A 43 mm variant of the watch page (432 × 432, 216 dp): same rules, smaller square; drawn
  when a 43 mm device exists in the household.
- Curved rim text as a general watch component: allowed on the face's date only, see
  Decisions. Revisit if a real face needs a second arc.
- Hold-to-stamp for fact assertions (treasury "paid"): a 1 s press fills the button from the
  bottom in gold, release early cancels, completion lands the ОДОБРЕНО stamp with the
  masthead's 420 ms drop. It would be the WATCH surface's one motion, turning "one motion
  in the system" into "one per surface". Parked on 2026-10-25 in favour of plain tap; the
  owner's worry about impulsive taps is the reason to bring it back.
- Styling make.md (spaces, stickers, the vault's gold icon set) from this repo: its DOM is
  undocumented and the icon set is the vault's own decision (2026-06-26). Revisit if a
  second vault adopts make.md.
- A `g2-hunt.css` in this repo mapping the.hunt's nine Kanban lanes and Bases verdicts:
  that vocabulary is the vault's; the recipe is in `showcase/obsidian.html` §7 and §8.
- Embedding font files in the theme: the three vaults are on one machine with the fonts
  installed; a `@font-face` block would add weight to every vault for a case that does
  not exist yet.
- Charts on the wrist: the GUI's one-hue bar chart does not survive 240 dp; a figure with
  a trend glyph and ten blocks replace it. Revisit with a real data app.

## Migration notes for consuming repos

- **glory-to-protocol** `tui/theme.py`: replace the six Style constants with reads
  from `tokens.toml [resolved.bureau]`. `BORDER` → `border`, `HEADER` → `accent`,
  `BODY` → `fg`, `MUTED` → `muted`, `CYRILLIC_ACCENT` → `signal`, `SIGNATURE` →
  `faint`. Stamp colours → `ok`, `bad`, `info`, `warn`. SVG headers: `.bg` →
  `bg`, `.border` → `border`.
- **glory-to-gensek** `themes.toml`: add `[themes.bureau]` from this repo's toml as the
  default; keep `gensek` (teal) shipped for anyone who prefers it.
- **Obsidian vaults**: the June `deploy.fish` had put `Nirvytekh` into every registered
  vault (seven of eight on 2026-10-25; `zoloto-durakov` is outside the registry and takes
  `--vault`). `glory-to-kartoteka/tools/install.py --all` replaces `.obsidian/themes/Nirvytekh/`
  in the vaults already on it and drops the `g2-*` snippets into `.obsidian/snippets/`; the
  previous `theme.css` is kept beside it as `theme.css.prev` once. Enable the snippets per vault in Settings › Appearance.
  `zoloto-durakov/_code/nirvytekh/` is superseded and can be retired. `the.hunt`'s
  `hunt-style.css`: keep the header-card and striping rules if wanted, rewrite the lane
  and verdict colours as `--g2-lane` / token rules (recipe in the showcase §7, §8).
- **glory-to-direktiva** `nirvytekh.css`: already on the warm palette. Replace the
  `--nv-*` block with `@import` of `tokens.css` and alias `--nv-* → --g2-*`.
