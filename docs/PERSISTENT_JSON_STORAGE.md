# Persistent JSON Storage

BedFlow AI intentionally keeps its lightweight JSON persistence layer for the portfolio deployment. PostgreSQL is not required.

## What is persistent

The following mutable records are routed through `BEDFLOW_DATA_DIR`:

- users and password hashes;
- access events;
- discharge tasks;
- immutable task events;
- human decision audit records;
- capacity-simulation runs;
- short-term workflow memory and history.

Static CSV datasets, XGBoost `.joblib` artifacts, policies, source code, and model documentation remain inside the application image.

## Local use

When `BEDFLOW_DATA_DIR` is not set, BedFlow AI preserves the existing local behavior and writes runtime JSON files under `database/`.

```bash
python app.py
```

To keep local runtime records outside the repository:

```bash
export BEDFLOW_DATA_DIR=./data
python app.py
```

Windows PowerShell:

```powershell
$env:BEDFLOW_DATA_DIR = ".\data"
python app.py
```

## Railway

1. Open the BedFlow AI service in Railway.
2. Add a persistent volume.
3. Mount the volume at `/data`.
4. Add the service variable:

```text
BEDFLOW_DATA_DIR=/data
```

5. Redeploy the service.
6. Open `/api/ready` or the **System Operations** tab and confirm that the runtime directory is `/data`.

On first startup, missing JSON files are seeded from packaged defaults when available. Existing files on the mounted volume are never overwritten.

## Docker

The Docker image defaults to `/data`:

```bash
docker build -t bedflow-ai .
docker run --rm -p 8501:8501 -v bedflow-data:/data bedflow-ai
```

## Limitations

Persistent JSON is appropriate for a single BedFlow AI demo service and low write volume. It does not provide database transactions, relational constraints, or safe coordination across multiple application replicas. Keep Railway replica count at one when using this mode.
