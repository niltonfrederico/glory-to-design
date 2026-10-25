<!-- markdownlint-disable MD041 MD013 -->

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/read%20in-english-6fa86f?style=for-the-badge" alt="Read in English">
  </a>
</p>

```
┌──────────────────────────────────────────────────────────────────────────┐
│ СТАНДАРТ № .........: 001                                                │
│ TÍTULO .............: glory-to-design                                    │
│                       (Стандарт оформления · Padrão de Design)           │
│ CLASSIFICAÇÃO ......: ABERTO · PARA TODOS OS BUREAUS DA SUÍTE            │
│ DIRETORIA ..........: Padronização (Стандартизация)                      │
│ APROVADO POR .......: Diretor Norman                                     │
│ DATA DE VIGÊNCIA ...: 2026-10-24                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

## СВОДКА · Resumo

O design system da suíte de bureaus Mashinograd / NIRVYTEKH (`glory-to-*`). Três
superfícies, uma voz:

| Superfície | Showcase | Tokens |
|---|---|---|
| **GUI** (web, desktop e mobile) | `showcase/gui.html` | `tokens/tokens.css` |
| **TUI** (terminal) | `showcase/tui.html` | `tokens/tokens.toml` |
| **WATCH** (Wear OS, Galaxy Watch6 Classic 47 mm) | `showcase/watch.html` | `tokens/tokens.kt` |

Campo quase-preto quente, dourado para foco, vermelho de carimbo para decisões,
molduras box-drawing cujo peso carrega estado, rótulos em cirílico pareados com
inglês. Um tema opcional **paper** renderiza o mesmo sistema como formulário
envelhecido.

## Uso

```sh
python3 tools/derive_tokens.py     # regenera tokens/* e o relatório de contraste
```

Web: `<link rel="stylesheet" href="tokens/tokens.css">`, depois estilize com
`var(--g2-accent)` e companhia. Troque para paper com `<html data-theme="paper">`.

Terminal (Rust ou Python): leia `tokens/tokens.toml`. `[themes.bureau]` é o trio
mestre no formato do gensek; `[resolved.bureau]` é a tabela completa para consumidores
que não derivam em OKLab.

Relógio (Compose for Wear OS): copie `tokens/tokens.kt` para um source set e pinte com
`G2Bureau.accent` e companhia. O cabeçalho diz como a tabela se dobra num `ColorScheme`
do Material 3. Watch faces em Watch Face Format copiam o hex do `tokens.toml`.

## АРХИВ · Documentos

| Prateleira | Quando abrir |
|---|---|
| [`DESIGN.md`](DESIGN.md) | Princípios, modelo de tokens, decisões datadas, notas de migração. |
| [`docs/canon.md`](docs/canon.md) | O vocabulário do bureau: títulos, documentos, carimbos, saudações, regras de idioma. |
| [`docs/references.md`](docs/references.md) | Precedentes de computação e impresso do bloco oriental, com fontes. |
| [`tokens/contrast-report.md`](tokens/contrast-report.md) | Razões WCAG de cada par estrutural, regeneradas junto com os tokens. |

## ОТКАЗ · Aviso

A estética é vagamente inspirada em *Papers, Please* (© Lucas Pope / 3909 LLC), só na
atmosfera. Nenhum código, asset, nome ou símbolo do jogo, nem de qualquer Estado real,
aparece aqui. O bureau, sua língua e seus símbolos são originais da suíte.

## ЛИЦЕНЗИЯ · Licença

[GNU Affero General Public License v3.0](LICENSE), a mesma do resto da suíte. Tokens,
showcases e documentos incluídos.
