Build steps (on your dev machine)

1) Ensure Python is installed and available on PATH.
2) Install PyInstaller:
   python -m pip install pyinstaller
3) Run the build:
   build_exe.bat

Output
- The executable will be created at dist\MatchingGame.exe.
- Copy dist\MatchingGame.exe to the classroom PC and run it directly.

Notes
- The build must be done on Windows to produce a Windows .exe.
- If Windows Defender flags the file, re-run the build with a clean dist folder.
