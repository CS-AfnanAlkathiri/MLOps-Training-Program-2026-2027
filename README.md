# MLOps Training Program 2026–2027

**Training Program by [Qafza Tech](https://qafzatech.com)**

This repository documents my projects, tasks, and learning outcomes from the MLOps Training Program by Qafza Tech.

The training focuses on developing practical skills in Machine Learning Operations (MLOps) through hands-on projects, from data management and model development to deployment, automation, and monitoring.

## About Qafza Tech

[Qafza Tech](https://qafzatech.com/about) is a technology-focused training platform and community that supports learning and skills development in fields such as data and artificial intelligence.

The MLOps Training Program provides an opportunity to explore machine learning workflows and apply MLOps practices through practical tasks and projects.

## Program Overview

The program focuses on applying MLOps concepts throughout the machine learning lifecycle.

Using a real-world e-commerce dataset as a case study, the tasks progressively cover:

* Data ingestion and database management.
* Data preparation and machine learning development.
* Model deployment and production-style inference.
* Testing, versioning, automation, and monitoring.

Each task builds on the previous one, connecting the different stages of an end-to-end machine learning workflow.

## Main Project

### Olist Delivery Prediction

The main case study uses the **Olist Brazilian E-Commerce Dataset**, which contains information about customers, orders, order items, payments, reviews, products, sellers, and geolocation.

The machine learning objective is to predict whether an e-commerce order will be delivered **late or on time**.

Predicting delivery delays can help identify potential operational issues and support more informed decisions related to delivery performance and customer experience.

## Tasks Overview

### Task 1 — Data Ingestion and Database Management

The first task establishes the data foundation for the machine learning workflow.

It focuses on working with the Olist dataset, ingesting data into PostgreSQL, and preparing a structured database for subsequent analysis and model development.

**Key areas:** Python, PostgreSQL, Docker, data ingestion, and database workflows.

[Explore Task 1](Task-1/)

### Task 2 — Machine Learning Development

The second task focuses on building and evaluating a machine learning model to predict late deliveries.

The workflow is organized into six Jupyter notebooks covering:

* Reading and joining the datasets.
* Creating the late-delivery target labels.
* Splitting the data into training, validation, and test sets.
* Exploratory data analysis (EDA).
* Feature engineering and preprocessing.
* Model training, threshold tuning, and evaluation.

The task produces a trained Logistic Regression model and fitted preprocessing artifacts that are reused in Task 3.

**Key areas:** Data preprocessing, EDA, feature engineering, scikit-learn, classification, and model evaluation.

[Explore Task 2](Task-2/)

### Task 3 — From Notebooks to Production

The third task transforms the model developed in Task 2 into a production-style inference system.

It moves the workflow beyond Jupyter notebooks by introducing modular Python code, configuration management, automated testing, and a FastAPI service for predictions.

The project also incorporates:

* **DVC:** Data and model artifact versioning.
* **Great Expectations:** Input data validation.
* **MLflow:** Experiment tracking and model registration.
* **FastAPI:** Prediction endpoints.
* **Docker Compose:** Containerized services and orchestration.
* **GitHub Actions:** Continuous integration and Docker image publishing.
* **Monitoring:** API metrics, prediction logging, and prediction-drift checks.

The inference pipeline reuses the trained model and fitted preprocessing artifacts from Task 2 rather than retraining the model.

The project includes automated tests, a containerized inference environment, and documented setup and monitoring procedures.

**Key areas:** MLOps, model serving, API development, Docker, CI/CD, model versioning, testing, and monitoring.

[Explore Task 3](Task-3/) | [Task 3 Documentation](Task-3/README.md)

## Repository Structure

```text
MLOps-Training-Program-2026-2027/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Task-1/
│   ├── dataset/
│   ├── MLOps_Task1.pdf
│   └── Task1_Olist_Database.ipynb
│
├── Task-2/
│   ├── artifacts/
│   └── Notebook_1 ... Notebook_6
│
├── Task-3/
│   ├── app/
│   ├── config/
│   ├── data/
│   ├── models/
│   ├── notebooks/
│   ├── requirements/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   ├── Dockerfile.mlflow
│   ├── docker-compose.yml
│   ├── MONITORING.md
│   └── README.md
│
├── .pre-commit-config.yaml
└── README.md
```

*This structure highlights the main folders and files rather than listing every dataset, notebook, or generated artifact.*

## Goal

My goal throughout this training is to develop practical experience in building, managing, deploying, and monitoring machine learning systems using MLOps practices.

This repository serves as a record of my progress, technical projects, and the skills developed throughout the program.

## Training Provider

**Qafza Tech**

Program: MLOps Training Program

Website: [qafzatech.com](https://qafzatech.com)

## License and Acknowledgment

This repository contains my personal work and learning outcomes from the MLOps Training Program.

Training materials and proprietary content provided by Qafza Tech remain the property of Qafza Tech and are used for educational purposes.
