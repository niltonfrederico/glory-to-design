# СПРАВКА · References

Eastern-bloc computing and print precedents the design system borrows from. Compiled
2026-10-24 from web research. **(verified)** = read in the fetched page;
**(summary)** = search snippet only; **(unverified)** = lead. No hex values appear
here because no source stated any; the palette is ours.

## What the system takes from each tier

| Tier | Period look | What we borrow | Surface |
|---|---|---|---|
| Terminal (Elektronika 60, DVK, Robotron A7100) | green mono, 80×24, uppercase-only Cyrillic via KOI-7 shift codes | uppercase as *semantic* (focused panel, directory), status line, one accent at a time | TUI |
| Office PC (CP866 DOS, Norton Commander, Lexicon) | 16-colour text mode, full single/double box drawing, F-key footer | frame hierarchy (`═` active, `─` rest), 10-slot function bar, `[......]` inputs, dialog as a distinct surface | TUI and GUI |
| Paper (GOST forms, ДСП marks, stamps) | fixed-coordinate field grid, classification corner, red ink seals | ledger component, document header block, classification corner, stamp family | GUI (paper theme especially) |

Mixing the terminal and office tiers on one screen is the anachronism to avoid.

## 1. Hardware and terminals

- **Elektronika 60** ran the original Tetris on a 15IE-00-013 text terminal. Blocks
  were pairs of DEL characters that rendered as rectangles on Soviet clones; later
  `[]`. Playfield 10×20, three-digit score. (verified) https://tetris.wiki/Tetris_(Electronika_60)
- **KOI-7** (GOST 13052-67): 7-bit, SO switches to Cyrillic, SI back. The N2 table
  has Cyrillic only in uppercase slots, so uppercase-only Cyrillic is the authentic
  look of that tier. (verified) https://en.wikipedia.org/wiki/KOI-7
- **CP866** (1986) deliberately kept all of CP437's pseudographics (B0–DF: shades,
  single and double lines, blocks). That is why Russian DOS software kept the full
  `╔═╗ ┌─┐` vocabulary. (verified) https://en.wikipedia.org/wiki/Code_page_866
- **BK-0010/0011**: no hardware text mode; 512×256 mono or 256×256 in 4 colours
  from 16 hardwired sets users disliked. (verified) https://en.wikipedia.org/wiki/Electronika_BK
- **Robotron A 7100** (DDR): green monochrome with two brightness levels, 80×25,
  KOI-7 character ROM with a loadable second set. (verified) https://www.robotrontechnik.de/html/computer/a7100.htm
- **ZX Spectrum clones** (Pentagon, Scorpion) dominated Soviet homes 1991–96; 8×8
  attribute cells, two colours per cell, FLASH every 0.64 s. (verified for the
  display model) https://en.wikipedia.org/wiki/ZX_Spectrum_graphic_modes
- Agat, Pravetz 82, Elwro 800 Junior: (summary) only.

## 2. Software UI grammar

- **Norton Commander** became a synonym for DOS in Russian schools and institutes
  («синий экран Norton Commander стал синонимом DOS»). (verified) https://habr.com/ru/post/466839
- **NC 5.0 layout** (Ilya Birman's UI Museum): panels blue, menus cyan, dialogs grey,
  nested dialogs cyan again; selected files yellow; shadows faked grey-on-black;
  inputs drawn `[.........]`; footer F1 Help · F2 User Menu · F3 View · F4 Edit ·
  F5 Copy · F6 RenMov · F7 Mkdir · F8 Delete · F9 Menu · F10 Quit; filenames
  lowercase, directories UPPERCASE. (verified) https://ilyabirman.net/meanwhile/all/ui-museum-norton-commander-5-0/
  The "double line = active panel" rule is widely assumed but had no primary source
  in this pass. (unverified)
- **Volkov Commander**, **DOS Navigator** (Chișinău, 1991): local clones; DN had a
  grey default. (summary) https://en.wikipedia.org/wiki/DOS_Navigator
- **Lexicon** (Лексикон, Mikroinform): on almost every Soviet PC by the late 1980s,
  F1 help, hints always on screen. (verified for F1) https://author.today/post/51304
- **RT-11 family** and its Soviet clones RAFOS, FOBOS, FODOS, RUDOS, OS DVK: KMON
  commands DIR, COPY, TYPE, DELETE, HELP. (verified) https://en.wikipedia.org/wiki/RT-11

## 3. Print and physical design

- **Forms were standardised**: GOST 6.38-72 and 6.39-72 (формуляр-образец fixes
  position and bounds of 26 реквизиты on the sheet), merged into GOST 6.38-90.
  A бланк is a fixed-coordinate grid of fields. (summary) https://meganorm.ru/mega_doc/norm/gost_gosudarstvennyj-standart/11/gost_6_38-90_unifitsirovannye_sistemy_dokumentatsii_sistema.html
- **Classification hierarchy**: ДСП < Секретно < Совершенно секретно < Особой
  важности. The mark and «Экз. №» copy number sit top-right on page one. (summary)
- **Literaturnaya** set most Soviet books 1950–1990; digital version by ParaGraph,
  1996, commercial. (verified) https://en.wikipedia.org/wiki/Literaturnaya
- **VEB Typoart** (DDR state foundry): Super-Grotesk, Maxima, Minima, Timeless.
  Revivals are commercial. (verified) https://typeoff.de/2019/07/veb-typoart-fonts
- Typewriters: Yatran (Olympia clone), Lyubava (Robotron Erika licence). (summary)
- Colour conventions of grey-blue paper, red stamp ink, gold-on-red: no primary
  source found. (unverified) Treated as working assumption, not fact.

## 4. Typefaces (licence)

| Face | Licence | Why it matters | On Google Fonts |
|---|---|---|---|
| **JetBrains Mono** | OFL 1.1 | existing suite convention (protocol SVGs); full Cyrillic | yes |
| **PT Sans / PT Serif / PT Mono** | OFL 1.1 | ParaType's public faces for Russia; Cyrillic-first design | yes |
| **Terminus** | OFL 1.1 | bitmap; KOI8 coverage; closest free match to a Soviet PC console (verified) https://terminus-font.sourceforge.net/ | no |
| **Ultimate Oldschool PC Font Pack** | CC BY-SA 4.0 | IBM VGA 8×16, EGA 8×14, localised Cyrillic ROMs (verified) https://int10h.org/oldschool-pc-fonts/fontlist/ | no |
| **Fixedsys Excelsior** | CC0 | 8×16 bitmap look with cp1251 Cyrillic (verified) https://github.com/kika/fixedsys | no |
| **OpenGOST** | OFL 1.1 | GOST 2.304-81 drafting lettering; engineering nameplates (summary) | no |
| Iosevka | OFL 1.1 | only partial Cyrillic; check before using for labels (verified) | no |
| Rodchenko, Izhitsa, Typoart revivals | commercial | cited for reference only | no |

Choice for the showcase pages: **JetBrains Mono** for chrome and TUI, **PT Sans** for
GUI body text, **PT Serif** for the paper theme's body. All three are on Google Fonts
with Cyrillic subsets.

## 5. Pitfalls and good homages

- **Faux Cyrillic** (Я→R, И→N) reads as "yaussiai" to Russian readers and is seen as
  ignorant. Cyrillic labels are real words or nothing. (verified) https://en.wikipedia.org/wiki/Faux_Cyrillic
- **Papers, Please**: Pope "chose muted colors and stripped back a lot of the
  details" to carry the mood; the palette is greys and grey-blues with pops of red,
  green and yellow. (verified) https://gamedeveloper.com/design/road-to-the-igf-lucas-pope-s-i-papers-please-i-
- **Disco Elysium**: dialogue column built for scanning, not reading. (verified) https://80.lv/articles/disco-elysium-working-on-ui-design
- **Teletext**: 40×24, 8 colours, 2×3 block graphics; constraint is the attraction. (summary)

### Five takeaways applied

1. **Field quiet, accent as event.** Gold and stamp red go to stamps, selection and
   state change. The field is the warm near-black (or paper).
2. **Borrow grammar, not symbols.** F-key footer, ДСП corner, GOST field grid read
   "bureau" without a single hammer and sickle.
3. **Cyrillic is content, never texture.** Real words, real case rules.
4. **One hardware tier per surface.** TUI leans terminal, GUI leans office PC and
   paper.
5. **Constraint carries deadpan.** Low detail, few colours, copy written to be
   skimmed.
