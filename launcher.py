import os
import sys
from pathlib import Path

# Always run relative to the installed Nurture directory, never the user's CWD.
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)

from nurture_lang.runtime import Runtime


def run_file(path):
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        print(f"Nurture: file not found: {path}")
        return 2
    if path.suffix.lower() != ".usd":
        print("Nurture: expected a .usd source file")
        return 2
    try:
        source = path.read_text(encoding="utf-8")
        Runtime().execute(source)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


def main():
    if len(sys.argv) < 2:
        print("Nurture 0.2.1")
        print("Usage: ntr <file.usd>")
        print("       ntr --help")
        return 0
    arg = sys.argv[1]
    if arg in ("-h", "--help"):
        print("Nurture 0.2.1")
        print("Usage: ntr <file.usd>")
        print("       ntr --help")
        print("       ntr --version")
        return 0
    if arg in ("-v", "--version"):
        print("Nurture 0.2.1")
        return 0
    return run_file(arg)


if __name__ == "__main__":
    raise SystemExit(main())
