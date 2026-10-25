#!/usr/bin/env python3
"""Install the Nirvytekh theme and the g2 snippets into Obsidian vaults.

    python3 tools/install_obsidian.py --vault ~/vault            # one vault
    python3 tools/install_obsidian.py --all                      # every registered vault already on Nirvytekh
    python3 tools/install_obsidian.py --all --include-others     # also vaults on another theme
    python3 tools/install_obsidian.py --all --dry-run            # say what would change, touch nothing
    python3 tools/install_obsidian.py --vault ~/vault --no-snippets

What it does, per vault:
  * copies obsidian/theme.css + manifest.json  ->  <vault>/.obsidian/themes/Nirvytekh/
  * copies obsidian/snippets/g2-*.css          ->  <vault>/.obsidian/snippets/
  * keeps a previous theme.css once, as theme.css.prev, when it differs from the new one

--all reads ~/.config/obsidian/obsidian.json and, by default, only upgrades vaults whose
appearance.json already selects Nirvytekh: it replaces the June theme, it does not push
the theme into a vault that chose another one. --include-others lifts that filter.

What it does not do: edit appearance.json. A running Obsidian rewrites that file on exit,
so the theme and the snippets are selected in Settings > Appearance. The script reports
what appearance.json currently says so you know whether there is anything to flip.

Run python3 tools/derive_tokens.py first: obsidian/theme.css is its output.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "obsidian"
THEME_NAME = "Nirvytekh"
REGISTRY = Path.home() / ".config" / "obsidian" / "obsidian.json"


def registry_vaults() -> list[Path]:
    if not REGISTRY.exists():
        sys.exit(f"no Obsidian registry at {REGISTRY}; pass --vault instead")
    data = json.loads(REGISTRY.read_text())
    return [Path(v["path"]) for v in data.get("vaults", {}).values() if "path" in v]


def plan(vault: Path, snippets: bool) -> list[tuple[Path, Path]]:
    dot = vault / ".obsidian"
    if not dot.is_dir():
        raise FileNotFoundError(f"{vault} has no .obsidian directory; not a vault")
    pairs = [
        (SRC / "theme.css", dot / "themes" / THEME_NAME / "theme.css"),
        (SRC / "manifest.json", dot / "themes" / THEME_NAME / "manifest.json"),
    ]
    if snippets:
        pairs += [(p, dot / "snippets" / p.name) for p in sorted((SRC / "snippets").glob("g2-*.css"))]
    return pairs


def same(a: Path, b: Path) -> bool:
    return b.exists() and a.read_bytes() == b.read_bytes()


def current_theme(vault: Path) -> str | None:
    f = vault / ".obsidian" / "appearance.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text()).get("cssTheme", "")
    except json.JSONDecodeError:
        return None


def report_appearance(vault: Path) -> str:
    f = vault / ".obsidian" / "appearance.json"
    if not f.exists():
        return "appearance.json: missing (Obsidian writes it on first open)"
    try:
        a = json.loads(f.read_text())
    except json.JSONDecodeError:
        return "appearance.json: unreadable"
    theme = a.get("cssTheme", "")
    scheme = a.get("theme", "")
    enabled = [s for s in a.get("enabledCssSnippets", []) if s.startswith("g2-")]
    notes = []
    notes.append(f"cssTheme={theme or '(default)'}" + ("" if theme == THEME_NAME else f"  <- select {THEME_NAME}"))
    notes.append(f"scheme={scheme}" + ("  <- 'system' is out of canon; pick obsidian (dark) or moonstone (paper)" if scheme == "system" else ""))
    notes.append("snippets on: " + (", ".join(enabled) if enabled else "none  <- enable g2-* as needed"))
    return "appearance.json: " + " · ".join(notes)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", action="append", type=Path, default=[], help="vault root; repeatable")
    ap.add_argument("--all", action="store_true", help="every vault in Obsidian's registry")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-snippets", action="store_true")
    ap.add_argument("--include-others", action="store_true", help="with --all: also vaults not on Nirvytekh")
    args = ap.parse_args(argv)

    if not (SRC / "theme.css").exists():
        sys.exit("obsidian/theme.css missing: run python3 tools/derive_tokens.py first")
    explicit = [v.expanduser().resolve() for v in args.vault]
    vaults = list(explicit)
    if args.all:
        for v in registry_vaults():
            if not (v / ".obsidian").is_dir():
                print(f"[{v}]\n  skip: not a vault (stale registry entry)")
                continue
            if not args.include_others and current_theme(v) != THEME_NAME:
                print(f"[{v}]\n  skip: on theme {current_theme(v) or '(default)'}; pass --include-others to install anyway")
                continue
            vaults.append(v)
    if not vaults:
        ap.error("give --vault PATH or --all")

    failures = 0
    for vault in dict.fromkeys(vaults):
        print(f"\n[{vault}]")
        try:
            pairs = plan(vault, not args.no_snippets)
        except FileNotFoundError as e:
            print(f"  skip: {e}")
            failures += 1
            continue
        for src, dst in pairs:
            rel = dst.relative_to(vault)
            if same(src, dst):
                print(f"  = {rel}")
                continue
            verb = "~" if dst.exists() else "+"
            print(f"  {verb} {rel}")
            if args.dry_run:
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() and dst.name == "theme.css" and not dst.with_suffix(".css.prev").exists():
                shutil.copy2(dst, dst.with_suffix(".css.prev"))
                print(f"    kept previous as {rel.with_suffix('.css.prev')}")
            shutil.copy2(src, dst)
        print("  " + report_appearance(vault))
    if args.dry_run:
        print("\ndry run: nothing written")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
