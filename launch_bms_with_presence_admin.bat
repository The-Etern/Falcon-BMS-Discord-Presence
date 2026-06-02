@echo off
setlocal

rem -- Ajusta esta ruta al ejecutable real de Falcon BMS.
set "GAME_EXE=C:\Ruta\a\FalconBMS.exe"
set "SCRIPT_DIR=%~dp0"
set "SCRIPT=%SCRIPT_DIR%presensebms.py"

rem -- Comprueba si ya se está ejecutando con permisos de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

rem -- Inicia el script de presencia de Discord y no cierra la consola si falla
start "BMS Presence" cmd /k python "%SCRIPT%"

rem -- Espera un momento para que el script arranque, luego inicia el juego
timeout /t 2 /nobreak >nul
start "Falcon BMS" "%GAME_EXE%"

endlocal
