# Rising Dusk — Handheld Port (ROCKNIX / JELOS / KNULLI)

Port of [Rising Dusk](https://store.steampowered.com/app/848930/Rising_Dusk/) (Studio Stobie) for ARM64 handhelds running ROCKNIX, JELOS, or KNULLI.

Runs the original Windows executable through **Wine + Box64 + Gamescope**.

> **You must own the game on Steam.** This port does not include any game files.

---

## Requirements

| | |
|---|---|
| **CFW** | ROCKNIX, JELOS, or KNULLI (must include Wine and Gamescope) |
| **Does NOT work on** | muOS, ArkOS, MinUI, or any CFW without Wine |
| **Tested on** | ROCKNIX (Retroid Pocket Flip 2, Snapdragon SM8250) |
| **Game** | Rising Dusk — Steam App 848930 (paid) |

---

## Installation

### 1. Download the port

Go to the [Releases](../../releases) page and download `risingdusk.zip`.

Extract it — you will get:
```
RisingDusk.sh
risingdusk/
```

Copy both into `ports/` on your device (merge, do not replace).

### 2. Copy your game files

You need to copy these files from your Steam installation into `ports/risingdusk/` on the device:

```
Rising Dusk.exe
assets/
lime.ndll
steamwrap.ndll
```

**Do NOT copy `steam_api.dll` or `steam_api64.dll`** — the port already includes offline-compatible replacements.

#### Automatic (recommended)

Run the included preparation script on your PC — it finds Steam automatically and copies the right files:

**Windows:** double-click `prepare_port.bat` (requires [Python 3](https://www.python.org/downloads/) with *Add to PATH* ticked)

**macOS / Linux:**
```bash
python3 prepare_port.py
```

Then copy the contents of the generated `risingdusk_ready/` folder into `ports/risingdusk/` on your device.

### 3. Launch

Open PortMaster or EmulationStation → Ports → Rising Dusk.

On first launch Wine sets up its prefix (~30 seconds). Subsequent launches are immediate.

### 4. Artwork (optional)

To get the cover and screenshot to appear in EmulationStation, add this entry to `/roms/ports/gamelist.xml` inside the `<gameList>` block:

```xml
<game>
  <path>./RisingDusk.sh</path>
  <name>Rising Dusk</name>
  <desc>An Anti-Coin Collection Platformer inspired by Japanese folktales. Befriend an assortment of ghosts and ghouls as you explore the world hidden in the dusk.</desc>
  <image>./risingdusk/cover.png</image>
  <thumbnail>./risingdusk/screenshot.png</thumbnail>
  <developer>Studio Stobie</developer>
  <publisher>Studio Stobie</publisher>
  <releasedate>20180726T000000</releasedate>
  <genre>Indie, Platformer</genre>
  <players>1</players>
</game>
```

---

## Controls

| Button | Action |
|---|---|
| Left Stick | Move |
| D-Pad | Move |
| A / B / X / Y | In-game actions |
| Start / Select | Menu / Escape |

---

## Known issues

- On some ROCKNIX builds the game must be launched from a terminal rather than EmulationStation. Run `/roms/ports/RisingDusk.sh` directly if the menu entry does not work.
- Faint audio artefacts may be audible at very low volume due to the Wine/Box64 audio pipeline.

---

## Third-party components

### Goldberg Steam Emulator

The files `risingdusk/steam_api.dll` and `risingdusk/steam_api64.dll` included in this port are **not** Valve's Steam client libraries. They are part of the [Goldberg Steam Emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator/blob/master/README.md)  by Mr_Goldberg, a clean-room reimplementation of the Steam API released under the **MIT licence** (see `risingdusk/licenses/goldberg.txt`).

These files replace the original `steam_api.dll` so the game can initialise without Steam running on the device. The user must still own and purchase the game on Steam — without the original game files this port does nothing.

---

## Credits

Port by [Clara Ogalla Moreno (Crazyx98)](https://github.com/clarax98).  
[Box64](https://github.com/ptitSeb/box64) by ptitSeb.  
[Wine](https://www.winehq.org/) — the Wine project.  
[Gamescope](https://github.com/ValveSoftware/gamescope) — Valve.  
[Goldberg Steam Emulator](https://gitlab.com/Mr_Goldberg/goldberg_steam_emu) — Mr_Goldberg (MIT licence).  
[PortMaster](https://portmaster.games) — the PortMaster team.  
Rising Dusk © Studio Stobie — all game content belongs to its respective owner.
