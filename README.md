# A7DO Project Life

This repository has three practical ways to view output:

1. Terminal output from `a7do_environment.py`
2. Browser output from `run_dashboard.py` via Streamlit
3. Browser output from `streamlit_pregnancy_app.py` via Streamlit

## What You Can View

- `a7do_environment.py` prints JSON world state and a text dashboard in the terminal
- `run_dashboard.py` opens a live Streamlit dashboard with world state, memory, pulse, messages, and English-learning output
- `streamlit_pregnancy_app.py` opens a Streamlit UI for prenatal and postnatal simulation output
- `tests/` contains automated checks; these show pass/fail output in the VS Code terminal or Test Explorer
- `jwst_lrd_pipeline/` is a separate scaffold; its `results/` and `data/` outputs are not present yet and are only created after running those scripts with real inputs

## Run In VS Code

Open the folder in VS Code, then use the integrated terminal in the project root.

### 1. Select Python

Use Python `3.11+`.

In VS Code:

- `Ctrl+Shift+P`
- Run `Python: Select Interpreter`
- Choose the interpreter you want to use for this folder

### 2. Optional Virtual Environment

If you want an isolated environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
```

### 3. Run The Main Outputs

Terminal dashboard output:

```powershell
python a7do_environment.py --ticks 10 --render-dashboard
```

Live introspection dashboard:

```powershell
python -m streamlit run run_dashboard.py
```

Pregnancy and fetal development app:

```powershell
python -m streamlit run streamlit_pregnancy_app.py
```

After Streamlit starts, open the local URL shown in the terminal, usually:

- `http://localhost:8501`

If one app is already running, Streamlit may choose another port.

## Run Tests

```powershell
python -m pytest -q
```

If `pytest` is missing, install it with:

```powershell
python -m pip install pytest
```

## VS Code Shortcuts Added

This repo now includes:

- `.vscode/launch.json` for one-click Run and Debug
- `.vscode/tasks.json` for terminal tasks

Use:

- `Run and Debug` for the Python/Streamlit launch profiles
- `Terminal -> Run Task` for the predefined commands

## Current Status

- `a7do_environment.py` runs successfully
- `streamlit` and `numpy` are installed in the current environment
- the two Streamlit apps start as long-running web servers, which is expected
- there are no existing generated `results/` or `outputs/` folders at the repository root right now
- `pytest` is not installed in the current environment yet
