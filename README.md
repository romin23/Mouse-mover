# Mouse Mover

Small GUI tool that wiggles the mouse and (optionally) performs a square double-click pattern to keep a session awake.

## Features
- Start/stop cursor movement with a GUI.
- Two modes: full-screen random movement or localized square pattern with double-clicks.
- Adjustable movement speed, delay between moves, and square width (slider).
- Press `q` anytime to stop movement; close the window to exit.

## Requirements
- Windows (uses `ctypes.windll.user32` and `mouse.ico`).
- Python 3.8+ (tested with 3.14 venv here).
- Dependencies listed in [requirements.txt](requirements.txt).

## Setup (fresh clone)
1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```powershell
pip install -r requirements.txt
```

3) Run the app
```powershell
python rat_move.py
```

## Run via batch file (convenience)
If you prefer, use the included batch script (it activates `.venv` then starts the app):
```powershell
.\n+run_rat_move.bat
```

## Usage tips
- Set **Movement speed (seconds)**: duration for each `moveTo` call.
- Set **Delay between moves (seconds)**: sleep between moves.
- Enable **square double-click pattern** to keep clicks near the current cursor. Adjust **Square width (px)** via the slider.
- Press **q** to stop movement without closing the GUI.

## Troubleshooting
- If Windows blocks the batch file in PowerShell, either run it from CMD or temporarily allow scripts:
	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	```
- Missing modules? Re-run `pip install -r requirements.txt` inside the activated `.venv`.
- Still stuck? Run with the venv interpreter explicitly:
	```powershell
	.\.venv\Scripts\python.exe rat_move.py
	```
