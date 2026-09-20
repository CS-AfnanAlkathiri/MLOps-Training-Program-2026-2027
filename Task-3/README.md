# Task 3 - From Notebooks to Production

This project converts the Task 2 late-delivery model into a production-style inference pipeline.

The training process remains in the Task 2 notebooks. Task 3 focuses on inference, validation, configuration, testing, APIs, containers, model tracking, and monitoring.

## Current Structure

- `app/` - API application
- `config/` - project configuration
- `data/` - sample input data
- `models/` - saved model and preprocessing artifacts
- `requirements/` - runtime and development dependencies
- `src/` - inference pipeline modules
- `tests/` - automated tests
- `predict.py` - command-line prediction entry point

## Environment Setup

The commands below use **Windows PowerShell**. Run them from the `Task-3` directory unless otherwise specified.

### 1. Clone the repository

```powershell
git clone https://github.com/CS-AfnanAlkathiri/MLOps-Training-Program-2026-2027.git
cd MLOps-Training-Program-2026-2027\Task-3
```

### 2. Create a virtual environment

Python 3.13 is used in the project's CI workflow.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements/runtime.txt
python -m pip install -r requirements/dev.txt
```

Check the environment:

```powershell
python -m pip check
```

## Model and Data Artifacts

Task 3 uses the model and fitted preprocessing artifacts developed in Task 2. The model is **not retrained** as part of the Task 3 inference pipeline.

The model and sample input data are tracked using DVC, with Google Drive configured as the remote storage location.

Before running inference on a fresh clone:

1. Install DVC with Google Drive support, preferably in a separate virtual environment.
2. Configure Google Drive authentication for your own authorized account or service account.
3. Download the tracked artifacts from inside `Task-3`:

```powershell
dvc pull
```

Authentication credentials are private and must not be committed to GitHub. The repository's GitHub Actions workflow uses the `GDRIVE_SERVICE_ACCOUNT_JSON` repository secret to download artifacts during CI.

**Important:** A new contributor cannot run `dvc pull` successfully without access to the configured private Google Drive remote.

## Run the API

For local inference using the downloaded model artifacts, set the model source to `local`:

```powershell
$env:MODEL_SOURCE = "local"
```

Start the FastAPI application:

```powershell
python -m uvicorn app.main:app --port 8000
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Available endpoints include:

| Endpoint              | Purpose                              |
| --------------------- | ------------------------------------ |
| `GET /health`         | Check API health                     |
| `GET /model-info`     | Display model information            |
| `POST /predict`       | Predict one order                    |
| `POST /predict-batch` | Predict multiple orders              |
| `GET /metrics`        | Expose Prometheus monitoring metrics |

### Example prediction request

In `/docs`, expand `POST /predict`, select **Try it out**, and submit:

```json
{
  "order_purchase_timestamp": "2018-06-21T08:29:29",
  "order_estimated_delivery_date": "2018-07-17T00:00:00",
  "customer_state": "MG",
  "seller_state": "SP",
  "item_count": 1,
  "total_price": 46.0,
  "total_freight_value": 18.42,
  "unique_products": 1,
  "unique_sellers": 1,
  "payment_count": 2,
  "total_payment_value": 64.42,
  "max_installments": 1,
  "payment_type_count": 2,
  "distance_km": 635.2422079475232
}
```

A successful response includes the predicted outcome, late-delivery probability, model version, and unique prediction ID.

## Docker

The project includes a `Dockerfile` and Docker Compose configuration.

The Compose setup includes services for the API, MLflow, PostgreSQL, and MinIO.

Docker Desktop must be installed and running before using Docker locally. The full Compose environment may also require service configuration and initial object-storage setup; it should not be treated as a verified one-command installation on a fresh computer.

The CI/CD pipeline builds and publishes the API image to GitHub Container Registry after the preceding checks pass on pushes to `main`.

The published container package is **private** and requires authorized access to pull it.

## Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The test suite covers API endpoints, prediction logic, preprocessing, input validation, Great Expectations validation, and drift detection.

Check code quality:

```powershell
python -m ruff check app src tests
python -m ruff format --check app src tests
```

The GitHub Actions workflow runs code-quality checks, retrieves DVC artifacts, runs the tests, and builds and publishes the Docker image on successful pushes to `main`.

## Monitoring

Monitoring is implemented using Prometheus metrics and structured prediction logs.

The `/metrics` endpoint exposes:

* `api_requests_total`: API request counts and HTTP status codes.
* `api_request_duration_seconds`: API response-time measurements.
* `model_predictions_total`: Counts of `late` and `on_time` predictions.

Each prediction is recorded in:

```text
logs/prediction_events.jsonl
```

The records include a timestamp, prediction ID, predicted outcome, probability, and model version.

The `logs/` directory is excluded from Git. Production use requires persistent, access-controlled log storage.

### Prediction drift

The drift baseline was calculated using 14,471 historical validation orders.

Run the drift checker:

```powershell
python -m src.drift_check
```

It compares the latest 100 predictions against the historical predicted late-delivery rate. Until 100 predictions are available, it reports insufficient data.

The baseline and monitoring rules are documented in:

```text
config/drift_baseline.json
MONITORING.md
```

The drift checker currently runs manually. Automatic alert scheduling, notifications, and dashboards have not been configured.

**Important:** A drift alert indicates a change in the prediction distribution; it does not establish that model accuracy has decreased.

## Reproducibility Notes

The inference pipeline reuses the saved model and preprocessing artifacts from Task 2.

Reproducing the project requires:

* Python and the project's dependencies.
* Access to the private DVC remote to download model artifacts.
* The appropriate model-source configuration.
* Docker and additional service configuration when running the containerized environment.

The drift baseline generation script also requires the Task 2 validation dataset:

```powershell
python -m src.drift_baseline
```

Recalculate the baseline when the reference model or classification threshold changes.

For the detailed monitoring plan, see `MONITORING.md`.
