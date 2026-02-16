$ErrorActionPreference = "Stop"

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
  throw "python is required but was not found in PATH."
}

python scripts/bootstrap_local_postgres.py
