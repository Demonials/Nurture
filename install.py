import os
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "Nurture"
INSTALL_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / APP_NAME
SOURCE_DIR = Path(__file__).resolve().parent


def find_python():
    candidates = []
    if sys.executable:
        candidates.append(Path(sys.executable).resolve())
    for name in ("python.exe", "py.exe"):
        found = shutil.which(name)
        if found:
            p = Path(found).resolve()
            if p not in candidates:
                candidates.append(p)
    for p in candidates:
        try:
            subprocess.run([str(p), "-c", "import sys; print(sys.version_info[0])"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return p
        except Exception:
            pass
    return None


def ensure_python():
    py = find_python()
    if py:
        return py
    winget = shutil.which("winget")
    if winget:
        print("Python 3 was not found. Installing Python 3 with winget...")
        subprocess.run([winget, "install", "--id", "Python.Python.3.13", "--exact", "--scope", "user", "--accept-source-agreements", "--accept-package-agreements"], check=True)
        py = find_python()
        if py:
            return py
    print("Python 3 is required. Install Python 3 and run install.bat again.")
    raise SystemExit(1)


def add_to_user_path(directory):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
        try:
            current, kind = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current, kind = "", winreg.REG_EXPAND_SZ
        entries = [x for x in current.split(";") if x]
        target = str(directory)
        if target.lower() not in {x.lower() for x in entries}:
            entries.append(target)
            winreg.SetValueEx(key, "Path", 0, kind, ";".join(entries))


def register_file_association(python_exe, launcher):
    import winreg
    command = f'"{python_exe}" "{launcher}" "%1"'
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.usd") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Nurture.Source")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Nurture.Source") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Nurture Source File")
        winreg.SetValueEx(key, "NeverShowExt", 0, winreg.REG_SZ, "")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Nurture.Source\DefaultIcon") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{INSTALL_DIR / "Nurture.ico"}",0')
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Nurture.Source\shell\open\command") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
    # Refresh Explorer so the new icon/association appears without rebooting.
    try:
        import ctypes
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
    except Exception:
        pass


def main():
    if os.name != "nt":
        print("Nurture installer currently targets Windows.")
        return 1
    python_exe = ensure_python()
    print("Installing Nurture...")
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
    shutil.copytree(SOURCE_DIR, INSTALL_DIR, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".gitignore"))

    launcher = INSTALL_DIR / "launcher.py"
    ntr = INSTALL_DIR / "ntr.cmd"
    ntr.write_text(
        '@echo off\r\n'
        f'"{python_exe}" "{launcher}" %*\r\n', encoding="utf-8")

    add_to_user_path(INSTALL_DIR)
    register_file_association(python_exe, launcher)

    print(f"Installed to: {INSTALL_DIR}")
    print("Registered .usd -> Nurture with the Nurture icon.")
    print("Added Nurture to your user PATH.")
    print("Open a NEW Command Prompt, then use: ntr calculator.usd")
    print("Double-clicking any .usd file will now run it with Nurture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
