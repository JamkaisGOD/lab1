# KU TURSHILT

This project is preconfigured for a Python 3.11+ environment with Jupyter notebooks and Git conventions.

## Environment

### 1) Create and activate the virtual environment

PowerShell:

```powershell
cd "C:\Users\netog\OneDrive\Desktop\KU TURSHILT"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install notebook jupyterlab ipykernel
python -m ipykernel install --user --name ku-turshilt --display-name "Python (ku-turshilt)"
```

### 3) Launch Jupyter

```powershell
jupyter lab
```

## Git rules

Branch naming convention:

- `main`
- `develop`
- `feature/<name>`
- `fix/<name>`
- `hotfix/<name>`
- `docs/<name>`
- `chore/<name>`
- `release/<name>`

Commit convention:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
- `refactor: ...`
- `test: ...`
- `perf: ...`
- `build: ...`
- `ci: ...`

Example:

```bash
git checkout -b feature/data-analysis
git add .
git commit -m "feat: initialize project environment"
```

## File structure

- `.venv/` - local Python environment
- `.githooks/` - Git hooks for branch validation
- `.vscode/` - VS Code workspace settings
- `notebooks/` - Jupyter notebooks
- `src/` - project source code
