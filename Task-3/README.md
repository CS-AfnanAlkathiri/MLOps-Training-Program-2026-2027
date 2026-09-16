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

Create a virtual environment:

```bash
python -m venv .venv