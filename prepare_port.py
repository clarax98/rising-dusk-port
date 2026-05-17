#!/usr/bin/env python3
"""
Rising Dusk - Port Preparation Script
======================================
Copies the required game files from your Steam installation into a ready-to-copy
folder. Works on Windows, macOS, and Linux.

Usage:
  Windows : double-click prepare_port.bat, or: python prepare_port.py
  macOS   : python3 prepare_port.py
  Linux   : python3 prepare_port.py

After running, copy the contents of 'risingdusk_ready/' into
'ports/risingdusk/' on your device (merge, do not replace the whole folder).
"""

import os
import sys
import shutil
import pathlib
import platform

# Files to copy from the Steam installation.
# Do NOT include steam_api.dll / steam_api64.dll — the port provides
# offline-compatible Goldberg replacements for those.
REQUIRED_FILES = [
    "Rising Dusk.exe",
    "lime.ndll",
    "steamwrap.ndll",
]
REQUIRED_DIRS = [
    "assets",
]


# ---------------------------------------------------------------------------
# Steam detection
# ---------------------------------------------------------------------------

def find_steam_root() -> pathlib.Path | None:
    system = platform.system()
    candidates: list[pathlib.Path] = []

    if system == "Windows":
        # Try registry first
        try:
            import winreg
            for hive, subkey in [
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\WOW6432Node\Valve\Steam"),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Valve\Steam"),
                (winreg.HKEY_CURRENT_USER,
                 r"SOFTWARE\Valve\Steam"),
            ]:
                try:
                    with winreg.OpenKey(hive, subkey) as k:
                        path, _ = winreg.QueryValueEx(k, "InstallPath")
                        candidates.append(pathlib.Path(path))
                except FileNotFoundError:
                    pass
        except ImportError:
            pass
        # Common fallback locations
        for drive in ["C", "D", "E"]:
            for suffix in [
                r"Program Files (x86)\Steam",
                r"Program Files\Steam",
                r"Steam",
            ]:
                candidates.append(pathlib.Path(f"{drive}:\\{suffix}"))

    elif system == "Darwin":
        candidates = [
            pathlib.Path.home() / "Library/Application Support/Steam",
        ]

    else:  # Linux / other POSIX
        candidates = [
            pathlib.Path.home() / ".local/share/Steam",
            pathlib.Path.home() / ".steam/steam",
            pathlib.Path("/usr/share/steam"),
        ]

    return next((p for p in candidates if p.is_dir()), None)


def find_all_steam_libraries(steam_root: pathlib.Path) -> list[pathlib.Path]:
    """Return all steamapps directories across all Steam libraries."""
    libraries = [steam_root / "steamapps"]

    vdf = steam_root / "steamapps" / "libraryfolders.vdf"
    if vdf.exists():
        for line in vdf.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().strip('"')
            # Library paths are quoted absolute paths in the VDF
            if line.startswith("/") or (len(line) > 2 and line[1] == ":"):
                lib = pathlib.Path(line) / "steamapps"
                if lib.is_dir():
                    libraries.append(lib)

    return libraries


def find_game(steam_root: pathlib.Path) -> pathlib.Path | None:
    for lib in find_all_steam_libraries(steam_root):
        game = lib / "common" / "Rising Dusk"
        if game.is_dir() and (game / "Rising Dusk.exe").exists():
            return game
    return None


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------

def copy_port_files(game_dir: pathlib.Path, out_dir: pathlib.Path) -> list[str]:
    """Copy required files; return list of missing items."""
    missing = []

    for name in REQUIRED_FILES:
        src = game_dir / name
        if src.exists():
            shutil.copy2(src, out_dir / name)
            print(f"  [OK] {name}")
        else:
            missing.append(name)
            print(f"  [--] {name}  (not found — skipped)")

    for name in REQUIRED_DIRS:
        src = game_dir / name
        dst = out_dir / name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            file_count = sum(1 for _ in dst.rglob("*") if _.is_file())
            print(f"  [OK] {name}/  ({file_count} files)")
        else:
            missing.append(name + "/")
            print(f"  [--] {name}/  (not found — skipped)")

    return missing


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 50
    print(sep)
    print("  Rising Dusk — PortMaster Preparation Tool")
    print(sep)
    print()

    # Allow manual game path as argument
    if len(sys.argv) > 1:
        game_dir = pathlib.Path(sys.argv[1])
        if not (game_dir / "Rising Dusk.exe").exists():
            print(f"ERROR: 'Rising Dusk.exe' not found in: {game_dir}")
            _wait_windows()
            sys.exit(1)
        print(f"Using provided path: {game_dir}")
    else:
        print("Looking for Steam...")
        steam_root = find_steam_root()
        if not steam_root:
            print(
                "ERROR: Steam not found.\n"
                "Install Steam and Rising Dusk, or pass the game folder as an argument:\n"
                f"  python prepare_port.py \"C:\\path\\to\\Rising Dusk\""
            )
            _wait_windows()
            sys.exit(1)
        print(f"  Steam: {steam_root}")

        print("Looking for Rising Dusk...")
        game_dir = find_game(steam_root)
        if not game_dir:
            print(
                "ERROR: Rising Dusk not found in any Steam library.\n"
                "Install it via Steam, or pass the folder path manually:\n"
                f"  python prepare_port.py \"C:\\path\\to\\Rising Dusk\""
            )
            _wait_windows()
            sys.exit(1)
        print(f"  Game: {game_dir}")

    # Prepare output directory
    out_dir = pathlib.Path("risingdusk_ready")
    if out_dir.exists():
        print(f"\nRemoving existing '{out_dir}/' ...")
        shutil.rmtree(out_dir)
    out_dir.mkdir()

    print(f"\nCopying files to '{out_dir}/' ...")
    missing = copy_port_files(game_dir, out_dir)

    print()
    if missing:
        print(f"WARNING: {len(missing)} item(s) were not found and were skipped:")
        for m in missing:
            print(f"  - {m}")
        print()

    print(sep)
    print(f"Done!  Output folder: {out_dir.resolve()}")
    print(sep)
    print()
    print("Next steps")
    print("----------")
    print("1. Copy the CONTENTS of 'risingdusk_ready/' into")
    print("   'ports/risingdusk/' on your device.")
    print("   (Merge into the existing folder — do NOT replace it wholesale,")
    print("    because the port provides its own steam_api.dll and config files.)")
    print()
    print("   On Linux/macOS with the device mounted or via SSH:")
    print("     rsync -av risingdusk_ready/ user@device:/roms/ports/risingdusk/")
    print()
    print("   On Windows: copy via File Explorer or WinSCP/MobaXterm.")
    print()
    print("2. Launch Rising Dusk from PortMaster or a terminal. Enjoy!")
    print()

    _wait_windows()


def _wait_windows() -> None:
    """Pause on Windows so the console window stays open."""
    if platform.system() == "Windows":
        input("Press Enter to close...")


if __name__ == "__main__":
    main()
