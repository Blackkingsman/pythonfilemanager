# Python File Manager

Watches a folder and sorts every new file into a subfolder by type the moment it lands: videos, spreadsheets, documents, images, PDFs, and programs. Files with duplicate names are never overwritten.

Built in 2020 to keep my Downloads and Videos folders from turning into a mess.

> Built by hand in 2020, before AI coding tools. Left as originally written.

## Features

- Pick the folder to watch from a small Tkinter GUI
- Reacts to file events in real time with `watchdog`
- Sorts by extension into category folders
- Renames on conflict instead of overwriting
- Remembers the watched folder between runs
- Packaged as a standalone Windows `.exe` with PyInstaller

## Tech

- **Python 3.8**
- `watchdog` for filesystem events
- `tkinter` for the GUI
- PyInstaller for the Windows build

## Running it

```bash
pip install watchdog
python main.py
```

A prebuilt Windows 10 executable is in [`Program_Watcher.zip`](Program_Watcher.zip).

## Branches

`master` has the final GUI version (merged from `v3`). `v2` and `Distro-Branch` hold the earlier script and the PyInstaller build output.
