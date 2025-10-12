@echo off
echo ===============================
echo Compilando Organizador de Archivos
echo ===============================

REM --- Cerrar el exe si está corriendo ---
echo Cerrando organizador.exe si esta corriendo...
taskkill /f /im organizador.exe 2>nul

REM --- Borrar compilaciones anteriores ---
echo Limpiando carpetas antiguas...
rmdir /s /q dist
rmdir /s /q build
del organizador.spec 2>nul

REM --- Borrar logs antiguos si existe ---
if exist log.txt del log.txt

REM --- Compilar con PyInstaller ---
echo Compilando organizador.py...
pyinstaller --onefile --noconsole organizador.py

REM --- Ejecutar el exe automáticamente ---
echo Abriendo organizador.exe...
start dist\organizador.exe

echo ===============================
echo Proceso finalizado.
pause
