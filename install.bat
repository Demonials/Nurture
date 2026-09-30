@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 install.py
    if not errorlevel 1 goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python install.py
    if not errorlevel 1 goto done
)

where winget >nul 2>nul
if %errorlevel%==0 (
    echo Python was not found. Nurture installer will try to install Python 3.13 using winget.
    winget install --id Python.Python.3.13 --exact --scope user --accept-source-agreements --accept-package-agreements
    if not errorlevel 1 (
        if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
            "%LocalAppData%\Programs\Python\Python313\python.exe" install.py
            goto done
        )
    )
)

echo.
echo Python 3 could not be found or installed automatically.
echo Install Python 3, then run install.bat again.
exit /b 1
:done
pause
