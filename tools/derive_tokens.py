#!/usr/bin/env python3
"""Derive the g2 design tokens from master seeds and gate them on WCAG contrast.

Mirrors the derivation in glory-to-gensek/src/theme/derive.rs and the blog's
tokens.css: a theme is a master trio (bg, fg, accent) plus a few fixed overrides;
every other token is mixed in OKLab and lifted until it clears its contrast target.

    python3 tools/derive_tokens.py          # writes tokens/*.css, *.toml, *.kt, report
    python3 tools/derive_tokens.py --check  # same math, writes nothing, exit 1 on fail

The generated files are the only place downstream repos read colors from. The seeds
below are the only place a human edits them. If a formula changes here, change it in
derive.rs too, or the two surfaces drift.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tokens"

# ---------------------------------------------------------------- sRGB <-> OKLab


def _to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


Rgb = tuple[float, float, float]
Lab = tuple[float, float, float]


def hex_to_rgb(h: str) -> Rgb:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb: Rgb) -> str:
    return "#" + "".join(f"{round(max(0.0, min(1.0, c)) * 255):02x}" for c in rgb)


def to_oklab(rgb: Rgb) -> Lab:
    r, g, b = (_to_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def from_oklab(lab: Lab) -> Rgb:
    L, a, b = lab
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = (v**3 for v in (l_, m_, s_))
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(_to_srgb(c) for c in (r, g, bl))  # type: ignore[return-value]


# ---------------------------------------------------------------- color ops (derive.rs)


def mix(a: str, b: str, weight_a: float) -> str:
    """mix(A weight%, B) in OKLab, like color-mix(in oklab, A w%, B)."""
    la, lb = to_oklab(hex_to_rgb(a)), to_oklab(hex_to_rgb(b))
    return rgb_to_hex(from_oklab(tuple(la[i] * weight_a + lb[i] * (1 - weight_a) for i in range(3))))  # type: ignore[arg-type]


def lightness(h: str) -> float:
    return to_oklab(hex_to_rgb(h))[0]


def chroma(h: str) -> float:
    _, a, b = to_oklab(hex_to_rgb(h))
    return math.hypot(a, b)


def hue_deg(h: str) -> float:
    _, a, b = to_oklab(hex_to_rgb(h))
    return math.degrees(math.atan2(b, a)) % 360


def hue_distance(a: str, b: str) -> float:
    d = abs(hue_deg(a) - hue_deg(b)) % 360
    return min(d, 360 - d)


def with_lightness(h: str, L: float) -> str:
    _, a, b = to_oklab(hex_to_rgb(h))
    return rgb_to_hex(from_oklab((max(0.0, min(1.0, L)), a, b)))


def rotate_hue(h: str, deg: float) -> str:
    L, a, b = to_oklab(hex_to_rgb(h))
    c, ang = math.hypot(a, b), math.atan2(b, a) + math.radians(deg)
    return rgb_to_hex(from_oklab((L, c * math.cos(ang), c * math.sin(ang))))


def _luminance(h: str) -> float:
    r, g, b = (_to_linear(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def lift(color: str, bg: str, target: float, dark: bool) -> str:
    """Move `color`'s lightness away from `bg` (keeping hue and chroma) until it
    clears `target` contrast. Mirrors the gensek 'lifted to 4.5:1' step."""
    step = 0.01 if dark else -0.01
    L = lightness(color)
    cur = color
    for _ in range(90):
        if contrast(cur, bg) >= target:
            return cur
        L += step
        if not 0.0 <= L <= 1.0:
            break
        cur = with_lightness(color, L)
    return cur


def away_from_bg(color: str, delta: float, dark: bool) -> str:
    return with_lightness(color, lightness(color) + (delta if dark else -delta))


# ---------------------------------------------------------------- seeds


@dataclass(frozen=True)
class Seed:
    name: str
    label: str
    bg: str
    fg: str
    accent: str
    signal: str  # stamp red; fixed by hand, the bureau has two accents
    ok: str
    warn: str
    bad: str
    info: str
    note_lightness: float
    note: str | None = None  # hand-fixed second hue; None derives it (gensek §10)


SEEDS = [
    Seed(
        name="bureau",
        label="БЮРО · bureau (canonical, dark)",
        bg="#0e0a05",  # warm near-black: direktiva / zoloto-durakov
        fg="#e8c887",  # cream
        accent="#d4af37",  # gold
        signal="#c0392b",  # stamp red
        ok="#6c782e",  # olive
        warn="#ffb000",  # amber
        bad="#c0392b",
        info="#5a7a8c",  # steel, the one cool accent
        note_lightness=0.78,
        note="#6fa86f",  # sage: the protocol badge green, gensek's hand-fixed note
    ),
    Seed(
        name="paper",
        label="БЛАНК · paper (optional, light)",
        bg="#e8dcbf",  # aged form paper
        fg="#1c1407",  # ink
        accent="#6e5010",  # dark gold, legible on paper
        signal="#a32616",  # stamp red, ink density
        ok="#4f5a1c",
        warn="#8a5a00",
        bad="#a32616",
        info="#3e5a6a",
        note_lightness=0.45,
        note="#3f6b3f",  # sage at ink density
    ),
]

# load-bearing pairs: (token, against, target)
GATES = [
    ("fg", "bg", 7.0),
    ("fg_bright", "bg", 7.0),
    ("fg", "panel", 7.0),
    ("fg", "panel_alt", 4.5),
    ("fg", "selection", 4.5),
    ("muted", "bg", 4.5),
    ("faint", "bg", 3.0),
    ("accent", "bg", 4.5),
    ("accent_ink", "accent", 4.5),
    ("note", "bg", 4.5),
    ("note", "note_bg", 4.5),
    ("ok", "bg", 4.5),
    ("warn", "bg", 4.5),
    ("bad", "bg", 4.5),
    ("info", "bg", 4.5),
    ("signal_text", "bg", 4.5),
    ("signal", "bg", 3.0),
    ("border", "bg", 1.5),
]


def derive(seed: Seed) -> dict[str, str]:
    dark = lightness(seed.bg) < 0.5
    t: dict[str, str] = {}
    t["bg"] = seed.bg
    t["fg"] = seed.fg
    t["accent"] = seed.accent
    t["bg_alt"] = mix(seed.fg, seed.bg, 0.04)
    t["panel"] = mix(seed.fg, seed.bg, 0.08)
    t["panel_alt"] = mix(seed.fg, seed.bg, 0.13)
    t["well"] = with_lightness(seed.bg, lightness(seed.bg) - (0.02 if dark else 0.05))
    t["fg_bright"] = away_from_bg(seed.fg, 0.07, dark)
    t["muted"] = lift(mix(seed.fg, seed.bg, 0.55), seed.bg, 4.5, dark)
    t["faint"] = lift(mix(seed.fg, seed.bg, 0.38), seed.bg, 3.0, dark)
    t["accent_bright"] = away_from_bg(seed.accent, 0.12, dark)
    t["border"] = mix(seed.accent, seed.bg, 0.45)
    t["border_faint"] = mix(seed.accent, seed.bg, 0.22)
    t["border_focus"] = seed.accent
    t["selection"] = mix(seed.accent, seed.bg, 0.18)
    # ink on a filled accent surface: whichever of well / fg_bright reads better
    cands = [t["well"], t["fg_bright"]]
    t["accent_ink"] = max(cands, key=lambda c: contrast(c, seed.accent))
    # note: hue rotated away from accent, then lifted (gensek §10)
    note = seed.note or with_lightness(rotate_hue(seed.accent, 140), seed.note_lightness)
    if seed.note is None and chroma(seed.accent) >= 0.02 and hue_distance(note, seed.accent) < 30:
        best = max((rotate_hue(seed.accent, d) for d in (120, 180, 240)), key=lambda c: hue_distance(c, seed.accent))
        note = with_lightness(best, seed.note_lightness)
    # the wash is the harder background, so lift against it; bg then passes too
    t["note_bg"] = mix(note, seed.bg, 0.12)
    t["note"] = lift(note, t["note_bg"], 4.5, dark)
    for k in ("ok", "warn", "bad", "info"):
        t[k] = lift(getattr(seed, k), seed.bg, 4.5, dark)
    t["signal"] = seed.signal
    t["signal_text"] = lift(seed.signal, seed.bg, 4.5, dark)
    t["signal_bg"] = mix(seed.signal, seed.bg, 0.14)
    return t


ORDER = [
    "bg", "bg_alt", "panel", "panel_alt", "well",
    "fg", "fg_bright", "muted", "faint",
    "accent", "accent_bright", "accent_ink",
    "border", "border_faint", "border_focus", "selection",
    "signal", "signal_text", "signal_bg",
    "note", "note_bg",
    "ok", "warn", "bad", "info",
]

ROLES = {
    "bg": "page / app background",
    "bg_alt": "slightly lifted band",
    "panel": "cards, forms, sidebars",
    "panel_alt": "selected row, banner",
    "well": "deepest surface: sidenav, done items, code wells",
    "fg": "body text",
    "fg_bright": "headings, key values",
    "muted": "secondary text, icons (AA)",
    "faint": "placeholders, disabled (3:1, non-text)",
    "accent": "gold: links, focus, active, filled buttons",
    "accent_bright": "gold highlight: focus ring, hover",
    "accent_ink": "text on a filled accent surface",
    "border": "frame lines",
    "border_faint": "subtle rules, table grid",
    "border_focus": "focused frame (= accent)",
    "selection": "text selection, hovered row",
    "signal": "stamp red for graphics and large text (3:1)",
    "signal_text": "stamp red lifted for body-size text (AA)",
    "signal_bg": "red wash behind a rejected/err row",
    "note": "the second hue: notes, annotations",
    "note_bg": "wash behind a note",
    "ok": "success",
    "warn": "warning",
    "bad": "error",
    "info": "information (the one cool accent)",
}

NON_COLOR_CSS = """
  /* type */
  --g2-font-mono: "JetBrains Mono", "PT Mono", ui-monospace, Menlo, Consolas, monospace;
  --g2-font-sans: "PT Sans", "Fira Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --g2-font-serif: "PT Serif", Georgia, "Times New Roman", serif;
  --g2-font-body: var(--g2-font-sans);
  --g2-tracking-label: 0.12em;
  --g2-tracking-logo: 0.18em;
  /* scale: 1.25 ratio on a 16px base */
  --g2-text-xs: 0.75rem;
  --g2-text-sm: 0.875rem;
  --g2-text-md: 1rem;
  --g2-text-lg: 1.25rem;
  --g2-text-xl: 1.5625rem;
  --g2-text-2xl: 1.953rem;
  --g2-text-3xl: 2.441rem;
  /* space: 4px grid */
  --g2-space-1: 0.25rem;
  --g2-space-2: 0.5rem;
  --g2-space-3: 0.75rem;
  --g2-space-4: 1rem;
  --g2-space-6: 1.5rem;
  --g2-space-8: 2rem;
  --g2-space-12: 3rem;
  /* shape: the bureau has no rounded corners and no shadows */
  --g2-radius: 0;
  --g2-shadow: none;
  --g2-rule: 1px;
  --g2-rule-strong: 2px;
  --g2-measure: 65ch;
""".rstrip("\n")


def css_block(t: dict[str, str], indent: str = "  ") -> str:
    return "\n".join(f"{indent}--g2-{k.replace('_', '-')}: {t[k]};" for k in ORDER)


def write_css(themes: dict[str, dict[str, str]]) -> str:
    bureau, paper = themes["bureau"], themes["paper"]
    return f"""/* GENERATED by tools/derive_tokens.py. Do not edit; edit the seeds there.
 * g2 design tokens. Dark-first: the bureau theme is canonical and lives on :root.
 * `paper` is an opt-in theme chosen by the user, never by prefers-color-scheme.
 * Usage: <html data-theme="paper"> or <html class="theme-paper"> to switch. */

:root {{
  color-scheme: dark;
{css_block(bureau)}
{NON_COLOR_CSS}
}}

:root[data-theme="paper"],
:root.theme-paper {{
  color-scheme: light;
{css_block(paper)}
  --g2-font-body: var(--g2-font-serif);
}}

/* print is paper: a filed request should look filed when it leaves the printer */
@media print {{
  :root {{
    color-scheme: light;
{css_block(paper, "    ")}
    --g2-font-body: var(--g2-font-serif);
  }}
}}
"""


def write_toml(themes: dict[str, dict[str, str]], seeds: list[Seed]) -> str:
    out = [
        "# GENERATED by tools/derive_tokens.py. Do not edit; edit the seeds there.",
        "# Shape follows glory-to-gensek/src/theme/themes.toml: a master trio plus",
        "# hand-fixed overrides. The [resolved.*] tables are the full derivation, for",
        "# consumers that do not run the OKLab step themselves (protocol, tuicr).",
        "",
    ]
    for s in seeds:
        t = themes[s.name]
        out += [
            f"[themes.{s.name}]            # {s.label}",
            f'bg = "{s.bg}"',
            f'fg = "{s.fg}"',
            f'accent = "{s.accent}"',
            f'heading = "{s.signal}"        # stamp red: the bureau has two accents',
            f'note = "{t["note"]}"',
            f'muted = "{t["muted"]}"',
            f'border = "{t["border"]}"',
            f'selection = "{t["selection"]}"',
            "",
        ]
    for s in seeds:
        t = themes[s.name]
        out.append(f"[resolved.{s.name}]")
        for k in ORDER:
            out.append(f'{k} = "{t[k]}"'.ljust(26) + f"# {ROLES[k]}")
        out.append("")
    return "\n".join(out)


def kotlin_name(token: str) -> str:
    head, *rest = token.split("_")
    return head + "".join(part.capitalize() for part in rest)


def write_kotlin(themes: dict[str, dict[str, str]], seeds: list[Seed]) -> str:
    """Compose for Wear OS consumer: one object per theme, every token a Color.

    Material 3 has more roles than the bureau; the mapping in the header is the
    intended fold, not a second source of truth. Watch Face Format has no variables,
    so faces copy the hex from tokens.toml by hand and this file does not apply.
    """
    out = [
        "// GENERATED by tools/derive_tokens.py. Do not edit; edit the seeds there.",
        "// g2 design tokens for Compose for Wear OS (and any Compose app). Drop the file",
        "// into a source set and set the package line.",
        "//",
        "// Fold into androidx.wear.compose.material3.ColorScheme (approximate):",
        "//   primary = accent · onPrimary = accentInk · primaryDim = accentBright",
        "//   background = bg · onBackground = fg · surfaceContainer = panel",
        "//   surfaceContainerHigh = panelAlt · surfaceContainerLow = well",
        "//   onSurface = fg · onSurfaceVariant = muted · outline = border",
        "//   outlineVariant = borderFaint · error = bad · tertiary = note",
        "//   The stamp red (signal, signalText) has no Material role; use it directly.",
        "",
        "package org.mashinograd.g2",
        "",
        "import androidx.compose.ui.graphics.Color",
        "",
    ]
    for s in seeds:
        t = themes[s.name]
        out.append(f"/** {s.label} */")
        out.append(f"object G2{s.name.capitalize()} {{")
        for k in ORDER:
            decl = f"    val {kotlin_name(k)} = Color(0xFF{t[k][1:].upper()})"
            out.append(decl.ljust(46) + f"// {ROLES[k]}")
        out.append("}")
        out.append("")
    return "\n".join(out)


def write_report(themes: dict[str, dict[str, str]], failures: list[str]) -> str:
    lines = [
        "# Contrast report",
        "",
        "GENERATED by tools/derive_tokens.py. WCAG 2.x contrast for every load-bearing pair.",
        "AA text = 4.5, AAA body = 7.0, graphics / large text = 3.0.",
        "",
    ]
    for name, t in themes.items():
        lines += [f"## {name}", "", "| pair | ratio | target | result |", "|---|---|---|---|"]
        for tok, against, target in GATES:
            r = contrast(t[tok], t[against])
            ok = "pass" if r >= target else "**FAIL**"
            lines.append(f"| `{tok}` on `{against}` | {r:.2f} | {target} | {ok} |")
        hd = hue_distance(t["note"], t["accent"])
        lines += ["", f"Hue distance note ↔ accent: {hd:.0f}° (guard: ≥ 30°)", ""]
    if failures:
        lines += ["## Failures", ""] + [f"- {f}" for f in failures]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    themes = {s.name: derive(s) for s in SEEDS}
    failures: list[str] = []
    for name, t in themes.items():
        for tok, against, target in GATES:
            r = contrast(t[tok], t[against])
            if r < target:
                failures.append(f"{name}: {tok} on {against} = {r:.2f} < {target}")
        if hue_distance(t["note"], t["accent"]) < 30:
            failures.append(f"{name}: note hue within 30° of accent")
    if not check_only:
        OUT.mkdir(exist_ok=True)
        css = write_css(themes)
        (OUT / "tokens.css").write_text(css)
        (ROOT / "showcase" / "tokens.css").write_text(css)  # same file, so showcase pages link it relatively
        (OUT / "tokens.toml").write_text(write_toml(themes, SEEDS))
        (OUT / "tokens.kt").write_text(write_kotlin(themes, SEEDS))
        (OUT / "contrast-report.md").write_text(write_report(themes, failures))
    for name, t in themes.items():
        print(f"[{name}]")
        for k in ORDER:
            print(f"  {k:14} {t[k]}")
    if failures:
        print("\nFAIL:", *failures, sep="\n  ")
        return 1
    print("\nall gates pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
