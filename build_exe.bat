@echo off
setlocal

REM Build a standalone Windows executable with PyInstaller.
REM Requires: pyinstaller installed on this machine.

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
  echo PyInstaller is not installed for this Python.
  echo Install it with: python -m pip install pyinstaller
  exit /b 1
)

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name MatchingGame ^
  matching_game.py
if errorlevel 1 (
  echo Failed to build MatchingGame.
  exit /b 1
)

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name CoinFlipGame ^
  coin_flip_game.py
if errorlevel 1 (
  echo Failed to build CoinFlipGame.
  exit /b 1
)

echo.
echo Build complete. Your executable is in the dist folder:
echo   dist\MatchingGame.exe
echo   dist\CoinFlipGame.exe
endlocal
