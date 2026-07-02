# QuantaHealth — Quantum-Accelerated Drug Interaction Checker

**Type:** Personal project
**Domain:** Healthtech / quantum machine learning

**What I built:**
A hybrid quantum-classical classifier that predicts drug-interaction severity over
240,000 labeled drug pairs from DDInter 2.0. The model uses an 8-qubit PennyLane
variational circuit feeding a PyTorch classification head over RDKit molecular
fingerprints. I benchmarked it against a classical baseline and tracked all
experiments in MLflow with a model registry, A/B routing, and one-click rollback;
datasets were versioned with DVC. I deployed the whole thing end to end as a
Dockerized FastAPI service with a Streamlit dashboard designed for pharmacist
workflows.

**Tools & tech:** PennyLane (8-qubit variational circuit), PyTorch, RDKit
(molecular fingerprints), DDInter 2.0 dataset, MLflow (model registry, A/B routing,
rollback), DVC, Docker, FastAPI, Streamlit

**Scale / details:**
- 240K labeled drug pairs.
- 8-qubit variational quantum circuit.
- Benchmarked against a classical baseline.
- Full MLOps: experiment tracking, model registry, dataset versioning, containerized deployment.
