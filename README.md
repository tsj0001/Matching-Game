# Matching Game (Statistics Demo)

This project includes two statistics demos:

- Matching game: roll a fair die six times and a match occurs if roll k equals position k for any k = 1..6.
- Coin flip game: flip a fair coin to track heads/tails proportions and streaks, plus the average flips to reach 10 in a row.

## Run locally

```bash
python matching_game.py
```

```bash
python coin_flip_game.py
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
python -m PyInstaller --noconfirm --clean --onefile --windowed --name CoinFlipGame coin_flip_game.py
```

3) Copy the executable to the classroom PC:

- `dist\MatchingGame.exe`
- `dist\CoinFlipGame.exe`

## Notes

- Build must be done on Windows to create a Windows `.exe`.
- If antivirus flags the file, rebuild with a clean `dist` folder.
