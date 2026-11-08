@echo off
REM ============================================================================
REM  run_automation.bat - runs the Desktop & CLI automation framework
REM
REM  Double-click          -> asks which application to test (Enter = default)
REM  run_automation.bat --app excel
REM  run_automation.bat --app all -m smoke --open
REM  run_automation.bat --app notepad --env qa --no-pdf
REM
REM  All arguments are passed straight to automation_framework\run_tests.py.
REM  Exit code = pytest's exit code (0 = all tests passed).
REM ============================================================================
setlocal

pushd "%~dp0automation_framework" || (
    echo Could not find the automation_framework folder next to this file.
    pause
    exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    echo Python was not found on PATH. Install Python 3 and try again.
    popd
    pause
    exit /b 1
)

python run_tests.py %*
set "RESULT=%ERRORLEVEL%"

popd

echo.
if "%RESULT%"=="0" (
    echo ===== ALL TESTS PASSED =====
) else (
    echo ===== TESTS FAILED  ^(exit code %RESULT%^) =====
)

REM Keep the window open when started by double-click (no arguments)
if "%~1"=="" pause

endlocal & exit /b %RESULT%
