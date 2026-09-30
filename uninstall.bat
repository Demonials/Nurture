@echo off
setlocal
python -c "import winreg; [winreg.DeleteKey(winreg.HKEY_CURRENT_USER, p) for p in [r'Software\\Classes\\Nurture.Source\\shell\\open\\command', r'Software\\Classes\\Nurture.Source\\shell\\open', r'Software\\Classes\\Nurture.Source\\shell', r'Software\\Classes\\Nurture.Source', r'Software\\Classes\\.usd']]"
if exist "%LOCALAPPDATA%\Nurture" rmdir /s /q "%LOCALAPPDATA%\Nurture"
echo Nurture file association and installation removed.
pause
