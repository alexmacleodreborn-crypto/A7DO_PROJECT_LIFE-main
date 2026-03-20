## A7DO Project Life

This repository now includes a runnable A7DO bootstrap that assembles the existing subsystem files into a working local environment.

### Run

Use a local Python 3 interpreter from the repo root:

```powershell
python a7do_environment.py --ticks 10 --render-dashboard
```

The Streamlit dashboard entry point is still available in [run_dashboard.py](/c:/Users/alexm/OneDrive/Desktop/A7DO_PROJECT_LIFE-main/run_dashboard.py) for interactive inspection.

### Main entry points

- [a7do_environment.py](/c:/Users/alexm/OneDrive/Desktop/A7DO_PROJECT_LIFE-main/a7do_environment.py): runs the assembled A7DO and world loop.
- [00_CORE_EXISTENCE/bootstrap/life_loop.py](/c:/Users/alexm/OneDrive/Desktop/A7DO_PROJECT_LIFE-main/00_CORE_EXISTENCE/bootstrap/life_loop.py): authoritative life/world integration loop.
- [simulate_evidence.py](/c:/Users/alexm/OneDrive/Desktop/A7DO_PROJECT_LIFE-main/simulate_evidence.py): deterministic evidence simulation with optional ledger persistence.
