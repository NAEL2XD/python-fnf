@ECHO OFF
ECHO Compiling...
setlocal
cd /d %~dp0
rmdir export /S /Q
pyinstaller --onefile Compile.py
del Compile.spec
cd dist
mkdir assets
ren Compile.exe PyFNF.exe
cd /d %~dp0
robocopy assets dist/assets /E
ren dist export
ECHO Done Compiling!
pause