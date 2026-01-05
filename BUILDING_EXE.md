Build steps (on your dev machine)

1) Ensure Python is installed and available on PATH.
2) Install PyInstaller:
   python -m pip install pyinstaller
3) Run the build:
   build_exe.bat

Output
- The executables will be created at dist\MatchingGame.exe and dist\CoinFlipGame.exe.
- Copy the .exe files to the classroom PC and run them directly.

Notes
- The build must be done on Windows to produce a Windows .exe.
- If Windows Defender flags the file, re-run the build with a clean dist folder.
