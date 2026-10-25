<!-- markdownlint-disable MD041 MD013 -->

<p align="center">
  <a href="README.pt-br.md">
    <img src="https://img.shields.io/badge/leia%20em-portugu%C3%AAs-6fa86f?style=for-the-badge" alt="Leia em Português">
  </a>
</p>

```
┌──────────────────────────────────────────────────────────────────────────┐
│ СТАНДАРТ № .........: 001                                                │
│ TITLE ..............: glory-to-design                                    │
│                       (Стандарт оформления · Design Standard)            │
│ CLASSIFICATION .....: OPEN · FOR ALL BUREAUS OF THE SUITE                │
│ DIRECTORATE ........: Standards (Стандартизация)                         │
│ APPROVED BY ........: Director Norman                                    │
│ EFFECTIVE DATE .....: 2026-10-24                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

## СВОДКА · TL;DR

The design system of the Mashinograd / NIRVYTEKH bureau suite (`glory-to-*`). Three
surfaces, one voice:

| Surface | Showcase | Tokens |
|---|---|---|
| **GUI** (web, desktop and mobile) | `showcase/gui.html` | `tokens/tokens.css` |
| **TUI** (terminal) | `showcase/tui.html` | `tokens/tokens.toml` |
| **WATCH** (Wear OS, Galaxy Watch6 Classic 47 mm) | `showcase/watch.html` | `tokens/tokens.kt` |

Warm near-black field, gold for focus, stamp red for decisions, box-drawing frames
whose weight carries state, Cyrillic labels paired with English. An optional **paper**
theme renders the same system as an aged form.

## Use

```sh
python3 tools/derive_tokens.py     # regenerate tokens/* and the contrast report
```

Web: `<link rel="stylesheet" href="tokens/tokens.css">`, then style with
`var(--g2-accent)` and friends. Switch to paper with `<html data-theme="paper">`.

Terminal (Rust or Python): read `tokens/tokens.toml`. `[themes.bureau]` is the
gensek-shaped master trio; `[resolved.bureau]` is the full table for consumers that do
not derive in OKLab themselves.

Watch (Compose for Wear OS): drop `tokens/tokens.kt` into a source set and paint with
`G2Bureau.accent` and friends. The header says how the table folds into a Material 3
`ColorScheme`. Watch faces built with Watch Face Format copy the hex from `tokens.toml`.

## АРХИВ · Documents

| Shelf | When to open it |
|---|---|
| [`DESIGN.md`](DESIGN.md) | Principles, token model, dated decisions, migration notes. |
| [`docs/canon.md`](docs/canon.md) | The bureau's vocabulary: titles, documents, stamps, salutes, language rules. |
| [`docs/references.md`](docs/references.md) | Eastern-bloc computing and print precedents, with sources. |
| [`tokens/contrast-report.md`](tokens/contrast-report.md) | WCAG ratios for every load-bearing pair, regenerated with the tokens. |

## ОТКАЗ · Disclaimer

The aesthetic is loosely inspired by *Papers, Please* (© Lucas Pope / 3909 LLC) in
atmosphere only. No code, asset, name or symbol from that game, or from any real state,
appears here. The bureau, its language and its symbols are original to the suite.

## ЛИЦЕНЗИЯ · License

[GNU Affero General Public License v3.0](LICENSE), the same licence as the rest of the
suite. Tokens, showcases and documents included.
