@ECHO OFF
ECHO Compiling...
setlocal
cd /d %~dp0
pyinstaller --onefile Compile.py
del Compile.spec
rmdir build /S /Q
cd dist
mkdir assets
ren Compile.exe PyFNF.exe
cd /d %~dp0
robocopy assets dist/assets /E
rename dist export
ECHO Done Compiling!
pause