# MediVault Backend

Python + FastAPI backend for MediVault.

## Requirements

- Python 3.11 or newer
- PostgreSQL
- Git

## Local setup

From this directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Create a local `.env` file by copying the repository-root `.env.example` and set your local PostgreSQL credentials. Never commit the populated `.env` file.

Start the development server:

```powershell
uvicorn app.main:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Current scope

The initial application entry point exposes a health-check endpoint only. Database models, migrations, authentication, family authorization, and medical-record features will be implemented in their roadmap phases. Do not use this starter as a production service.
