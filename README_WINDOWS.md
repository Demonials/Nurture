# Nurture on Windows

## Install

Run `install.bat`.

The installer:
- checks for Python 3 first;
- tries `winget` to install Python 3.13 if Python is missing;
- installs Nurture into `%LOCALAPPDATA%\Nurture`;
- creates the global `ntr` command;
- registers `.usd` files with Nurture;
- assigns the Nurture icon to `.usd` files.

## Run

Open a new Command Prompt:

```text
ntr calculator.usd
```

You can also run any file directly:

```text
ntr C:\path\to\program.usd
```

Or simply double-click a `.usd` file in Explorer.

## Important

The Nurture launcher resolves its own installation directory before importing the runtime. It does not assume that `launcher.py` is located in `C:\` or in the current working directory.
