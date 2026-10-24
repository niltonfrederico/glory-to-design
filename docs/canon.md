# КАНОН · Canon

The bureau's vocabulary, as the suite's repos already use it. Compiled 2026-10-24 from
`glory-to-protocol` (README, TRUE_* docs, SVGs, `stamps.py`, `theme.py`),
`glory-to-gensek` (strings, spec), `glory-to-direktiva` (README, DESIGN.md) and the
`state-titles-in-english` project memory. Nothing here is new; where the repos are
silent, this file says so.

## The institution

| Term | Cyrillic | English | PT-BR |
|---|---|---|---|
| The bureau | НИРВЫТЕХ · Нирская Вычислительная Техника | NIRVYTEKH · Bureau of Computational Technology | NIRVYTEKH · Bureau de Tecnologia Computacional |
| The city / canon | Машиноград | Mashinograd | Mashinograd |
| The suite | — | the `glory-to-*` suite, "g2"; each repo is a bureau or directorate | idem |

Directorates named so far: **Public Works** (Общественные Работы), **Internal
Affairs**. `glory-to-protocol` is the Bureau of Protocol, "the most complete of the
suite's feel". `glory-to-proton` styles itself Bureau of Protocol Engineering in its
own theme example.

## Figures and titles

| Role | In English prose | In PT-BR prose | Notes |
|---|---|---|---|
| Head of state | **Верховный Генсек** (short: Генсек) | Vetor Partidário Supremo / Supremo Gensek | Never translate the title inside English text. Rule from the `state-titles-in-english` memory, corrected by Nilton on 2026-05-26. |
| Supreme Leader | **Верховный Лидер** | Líder Supremo | Appears in README ("Want a favor from the Верховный Лидер?"). |
| Director of the bureau | Director Norman · Директор: Норман | Diretor Norman | Signs documents ("APPROVED BY: Director Norman"). |

Salutes stay in Russian in every language. They are punctuation, used sparingly:
**Слава Генсеку** · **Слава НИРВЫТЕХ** · **Да здравствует Верховный Генсек** ·
**За Верховного Лидера** · **С честью, Генсек**.

## Documents

Public docs are **numbered forms**. The header block is a framed ledger of
`FIELD ....: value` rows, dot-leadered, inside a single-line box:

```
┌──────────────────────────────────────────────────────────────┐
│ ДОКУМЕНТ № ........: 003                                     │
│ TITLE ..............: True Contributing Guide                │
│ CLASSIFICATION .....: OPEN CALL · POSTED IN PUBLIC SQUARES   │
│ DIRECTORATE ........: Public Works (Общественные Работы)     │
│ APPROVED BY ........: Director Norman                        │
│ COUNTERSIGNED ......: Supreme Gensek of the Supreme Party Vector │
│ EFFECTIVE DATE .....: 2026-05-20                             │
└──────────────────────────────────────────────────────────────┘
```

Numbering seen in `glory-to-protocol`: 001 README · 002 (Code of Conduct) · 003 True
Contributing · 004 (True Code of Conduct). Numbers are per repo. **2026-05-20** is the
effective date on every founding document.

Section headings carry a Cyrillic eyebrow: `СВОДКА · TL;DR`, `АРХИВ · Documentation`,
`ОТКАЗ · Disclaimer`, `ВКЛАД · Contributing`, `КОДЕКС · Code of Conduct`,
`ЛИЦЕНЗИЯ · License`. Legal articles are numbered Roman (`Article I`).

Every public doc has a plain twin and, where the voice is laid on thick, a `TRUE_*`
twin "for citizens of elevated clearance" (Для граждан повышенного допуска). Where
they diverge on substance, the plain one holds.

## Stamps

Four decisions, bilingual, always Cyrillic first:

| Stamp | Cyrillic | English | Meaning | Color (protocol) |
|---|---|---|---|---|
| approve | ОДОБРЕНО | APPROVED | request granted, action complete | green |
| reject | ОТКАЗАНО | REJECTED | denied; carries a reason | red |
| order | ПРИКАЗ | DIRECT ORDER | the bureau dictates an action | blue |
| review | К СВЕДЕНИЮ | FOR REVIEW | awaiting an external decision | yellow |

Seal stamps on SVG headers: **ДОСТОЯНИЕ НАРОДА / PROPERTY OF THE PEOPLE** (license
seal), **ОДОБРЕНО / APPROVED · OFFICIAL RELEASE**, plus "together", "watching",
"redacted" variants. Rendered as two or three concentric rings, text on arcs, a ★ or
✓ in the center, rotated a few degrees, with ink grain and displacement.

Other recurring glyphs: `★` (the state), `▌` (section marker in gensek),
`ОФИЦИАЛЬНО` as a rule caption.

## Voice

Deadpan. The bureau is picky, patient and literal. It welcomes labor and files it.
Humor comes from treating ordinary dev procedure as state procedure, never from
winking at the reader. Short declaratives. The Directorate "does not review
unannounced material". Threats are administrative, not violent.

Out of canon: fake Cyrillic (Я for R, И for N), hammer-and-sickle, real-world states,
leaders or parties, anything from *Papers, Please* beyond atmosphere (see the
protocol README disclaimer; Arstotzka and its symbols never appear).

## Languages

- UI strings exist in **en, pt-br, ru** wherever a UI exists (gensek rule).
- Public prose is **bilingual en-us + pt-br**, born together.
- Cyrillic labels are the *state's* voice and appear in every language.

## Not written anywhere (do not invent)

- The Tragedy.
- Norman's border-crossing origin.
- What the other directorates are, beyond Public Works and Internal Affairs.
- Any map, flag or anthem of Mashinograd.
