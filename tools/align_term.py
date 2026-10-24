#!/usr/bin/env python3
"""Normalize the terminal mockups (<pre class="term">) in showcase/tui.html.

Two things go wrong in hand-written box drawing inside HTML: the column count drifts
by a character here and there, and glyphs the monospace face lacks (✓ ✗ ★ ▸ ● ■ ⏎)
fall back to another font with a different advance width. This script fixes both:

1. Wraps every such glyph in <i class="g"> (CSS gives it exactly 1ch).
2. For every block, takes the frame-char columns of the first line with N frame
   characters as the anchors for every later line with N frame characters, and the
   block's width from its first top-border line (or an override), then pads or trims
   the fill run (spaces, or ─ ━ ═ on border lines) immediately before each frame
   character until it lands on its anchor.

    python3 tools/align_term.py          # rewrite showcase/tui.html in place
    python3 tools/align_term.py --check  # report only; exit 1 if anything is off
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "showcase" / "tui.html"

FRAME = set("┌┐└┘│┏┓┗┛┃╔╗╚╝║├┤┬┴╩╦╠╣")
FILL = set(" ─━═")
GLYPHS = set("✓✗★▸●■⏎")
WIDTH_OVERRIDE = {5: 80, 2: 74, 16: 36, 17: 36, 18: 36, 19: 36}

Tok = tuple[str, str]  # ("tag", "<span ...>") | ("ch", "x")


def tokenize(src: str) -> list[Tok]:
    out: list[Tok] = []
    i = 0
    while i < len(src):
        c = src[i]
        if c == "<":
            j = src.index(">", i)
            out.append(("tag", src[i : j + 1]))
            i = j + 1
        elif c == "&":
            j = src.index(";", i)
            out.append(("ch", src[i : j + 1]))  # one visible char, kept escaped
            i = j + 1
        else:
            out.append(("ch", c))
            i += 1
    return out


def visible(tok: Tok) -> str:
    return html.unescape(tok[1]) if tok[0] == "ch" else ""


def frame_positions(toks: list[Tok]) -> list[int]:
    """Token indexes of frame chars, in order."""
    return [i for i, t in enumerate(toks) if t[0] == "ch" and visible(t) in FRAME]


def column_of(toks: list[Tok], idx: int) -> int:
    return sum(1 for t in toks[:idx] if t[0] == "ch")


def adjust_before(toks: list[Tok], idx: int, delta: int) -> tuple[list[Tok], int, str | None]:
    """Grow (delta>0) or shrink (delta<0) the fill run right before token idx.
    Returns (tokens, new idx, error)."""
    # fill char is whatever visible char sits immediately before idx
    k = idx - 1
    while k >= 0 and toks[k][0] == "tag":
        k -= 1
    if k < 0 or visible(toks[k]) not in FILL:
        return toks, idx, "no fill run before frame char"
    fill = visible(toks[k])
    if delta > 0:
        toks = toks[: k + 1] + [("ch", fill)] * delta + toks[k + 1 :]
        return toks, idx + delta, None
    # shrink: remove up to -delta fill tokens walking back over tags
    need = -delta
    run: list[int] = []  # token indexes of the fill run, nearest first
    j = k
    while j >= 0:
        if toks[j][0] == "ch":
            if visible(toks[j]) != fill:
                break
            run.append(j)
        j -= 1
    if len(run) < need:
        return toks, idx, f"fill run too short: needed {need}, had {len(run)}"
    for j in run[:need]:  # nearest first, so later indexes are deleted first
        del toks[j]
    return toks, idx - need, None


def normalize_block(lines: list[str], target: int | None) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    toks_lines = [tokenize(l) for l in lines]
    if target is None:
        for tl in toks_lines:
            vis = "".join(visible(t) for t in tl)
            if vis and vis[0] in "┌┏╔":
                target = len(vis)
                break
    if target is None:
        return lines, []  # an unframed block (a list, a footer strip) has nothing to align
    anchors: dict[int, list[int]] = {}
    out: list[str] = []
    for n, tl in enumerate(toks_lines):
        fp = frame_positions(tl)
        vis = "".join(visible(t) for t in tl)
        if not fp or vis.rstrip()[-1:] not in FRAME:
            out.append("".join(t[1] for t in tl))  # not a framed line: leave alone
            continue
        key = len(fp)
        if key not in anchors:
            # first line of its kind: only its last frame char is forced to target-1
            cols = [column_of(tl, i) for i in fp]
            delta = (target - 1) - cols[-1]
            if delta:
                tl, _, err = adjust_before(tl, fp[-1], delta)
                if err:
                    errs.append(f"line {n}: {err}")
            fp = frame_positions(tl)
            anchors[key] = [column_of(tl, i) for i in fp]
            out.append("".join(t[1] for t in tl))
            continue
        want = anchors[key]
        for k in range(1, key):
            fp = frame_positions(tl)
            have = column_of(tl, fp[k])
            delta = want[k] - have
            if delta:
                tl, _, err = adjust_before(tl, fp[k], delta)
                if err:
                    errs.append(f"line {n}, frame {k}: {err} ({vis[:40]!r})")
        out.append("".join(t[1] for t in tl))
    # final verification
    for n, l in enumerate(out):
        vis = "".join(visible(t) for t in tokenize(l))
        if vis.rstrip()[-1:] in FRAME and len(vis.rstrip()) != target:
            errs.append(f"line {n}: width {len(vis.rstrip())} != {target}")
    return out, errs


def wrap_glyphs(block: str) -> str:
    def rep(m: re.Match[str]) -> str:
        return f'<i class="g">{m.group(0)}</i>'

    # do not double-wrap
    parts = re.split(r'(<i class="g">.</i>)', block)
    return "".join(p if p.startswith('<i class="g">') else re.sub("[" + "".join(GLYPHS) + "]", rep, p) for p in parts)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    src = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(r'(<pre class="term[^"]*"[^>]*>)(.*?)(</pre>)', re.S)
    failures: list[str] = []
    idx = -1

    def fix(m: re.Match[str]) -> str:
        nonlocal idx
        idx += 1
        body = wrap_glyphs(m.group(2))
        lines = body.split("\n")
        new, errs = normalize_block(lines, WIDTH_OVERRIDE.get(idx))
        for e in errs:
            failures.append(f"block {idx}: {e}")
        return m.group(1) + "\n".join(new) + m.group(3)

    out = pattern.sub(fix, src)
    if failures:
        print("\n".join(failures))
    if not check and out != src:
        PAGE.write_text(out, encoding="utf-8")
        print(f"rewrote {PAGE.name}: {idx + 1} blocks")
    elif check:
        print(f"checked {idx + 1} blocks")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
