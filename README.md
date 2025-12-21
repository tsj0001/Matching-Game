# Matching Game (Statistics Demo)

This project simulates the "matching game" where a fair die is rolled six times and a match occurs if roll k equals position k for any k = 1..6. The app visualizes each trial, tracks the success rate, and includes an auto-run mode plus a rolling histogram of match counts.

## Run locally

```bash
python matching_game.py
```

## Build a Windows executable (no admin needed on classroom PC)

Build on your own Windows machine, then copy the `.exe` to the classroom PC.

1) Install PyInstaller:

```bash
python -m pip install pyinstaller
```

2) Build the executable:

```bash
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MatchingGame matching_game.py
```

3) Copy the executable to the classroom PC:

- `dist\MatchingGame.exe`

## Notes

- Build must be done on Windows to create a Windows `.exe`.
- If antivirus flags the file, rebuild with a clean `dist` folder.
