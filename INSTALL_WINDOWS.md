# Nurture on Windows

## Install

1. Make sure Python 3 is installed.
2. Run `install.bat`.
3. Open a new Command Prompt.

Nurture is installed to `%LOCALAPPDATA%\Nurture`.

## Run a Nurture program

```text
ntr example.usd
```

Nurture programs use the normal Command Prompt for `input()`.
No Tkinter popup is used by the CLI runtime.

## Double-click `.usd`

The installer registers `.usd` files with Nurture. Double-clicking a `.usd` file starts the Nurture CLI runner and passes that file to it.

## IDE

Run `ntr` with no file, or run `python nurture.py`, to open the Nurture IDE.

## Uninstall

Run `uninstall.bat` from the original Nurture folder.
