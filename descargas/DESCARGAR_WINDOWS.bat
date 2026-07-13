@echo off
setlocal
set "URL=https://github.com/MatiasArg1888/ce19/releases/latest/download/CODIGO-ESCONDIDO-19-WINDOWS.zip"
set "OUT=%USERPROFILE%\Downloads\CODIGO-ESCONDIDO-19-WINDOWS.zip"

echo Descargando CODIGO ESCONDIDO 19 para Windows...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%OUT%'"

if errorlevel 1 (
    echo.
    echo No se pudo descargar el paquete. Verifique su conexion o que exista una version publicada.
    pause
    exit /b 1
)

echo.
echo Descarga completa:
echo %OUT%
explorer.exe /select,"%OUT%"
pause
