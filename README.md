<h1 align="center">
Marvelous MLOps End-to-end MLOps with Databricks course

## Practical information
- Weekly lectures on Wednesdays 16:00-18:00 CET.
- Code for the lecture is shared before the lecture.
- Presentation and lecture materials are shared right after the lecture.
- Video of the lecture is uploaded within 24 hours after the lecture.

- Every week we set up a deliverable, and you implement it with your own dataset.
- To submit the deliverable, create a feature branch in that repository, and a PR to main branch. The code can be merged after we review & approve & CI pipeline runs successfully.
- The deliverables can be submitted with a delay (for example, lecture 1 & 2 together), but we expect you to finish all assignments for the course before the 25th of November.


## Set up your environment
In this course, we use Databricks 15.4 LTS runtime, which uses Python 3.11.
In our examples, we use UV. Check out the documentation on how to install it: https://docs.astral.sh/uv/getting-started/installation/

To create a new environment and create a lockfile, run:

```
uv venv -p 3.11.9 .venv
.venv\Scripts\activate
uv pip install -r pyproject.toml --all-extras
uv lock
```

## Databricks Commands

### Authentication

```
# Authentication
databricks auth login --configure-cluster --host <workspace-url>

# Profiles
databricks auth profiles
cat ~/.databrickscfg

# Root Dir
databricks fs ls dbfs:/

export DATABRICKS_CONFIG_PROFILE=DEFAULT
```

### Catalog Creation

- catalog name: credit
- schema_name: default
- volume name: data

```
# Create

databricks volumes create mlops_students rageshns data MANAGED

# Push

databricks fs cp data/data.csv dbfs:/Volumes/mlops_students/rageshns/data/data.csv

# Show files
databricks fs ls dbfs:/Volumes/mlops_students/rageshns/data
```


delete functions:-
databricks functions delete mlops_students.rageshns.calculate_house_age
databricks functions delete mlops_students.rageshns.return_predictions



### Package Creation

```
# Build
uv build

# Create
databricks volumes create mlops_students rageshns packages MANAGED

# Push
databricks fs cp dist/credit_default_databricks-0.0.11-py3-none-any.whl dbfs:/Volumes/mlops_students/rageshns/packages

# Overwrite Package
databricks fs cp dist/credit_default_databricks-0.0.11-py3-none-any.whl dbfs:/Volumes/mlops_students/rageshns/packages --overwrite
```

### Token Creation

First create a token under Settings --> User --> Developer

```
# Create Scope
databricks secrets create-scope secret-scope

# Add secret after running command
databricks secrets put-secret secret-scope databricks-token

# List secrets
databricks secrets list-secrets secret-scope
```

## Data

Default of Credit Card Clients Dataset
https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset/data


## Fifth PR - Branch: inference

- Added monitoring folder
- Added refresh_monitor.py workflow
- Updated bundle file with monitoring

## Fourth PR - Branch: bundles

- Updated config class with A/B test params
- Updated test data cleaning
- Updated config file
- Token creation
- Added workflows preprocessing, train_model, evaluate_model, deploy_model
- Added create_source_data notebook
- Fixed dependencies in pyproject.toml (v 0.0.11)

## Third PR - Branch: serving

- Reorganized Notebooks Folders
- Changed env var "CONFIG DATABRICKS" and "CODE_PATH"
- New Workspace mlops_students (change catalog and schame name)
- Pyarrow incompatibility with mlflow/feature lookup. Changed o 14.0.2 in wheel 0.0.9
- Added Notebooks feature/model serving

## Second PR - Branch: mlflow

- Added hatchling
- Activated editabel mode: uv pip install -e .
- Removed "src" imports
- Improved src code, added utils and model training
- Added logs to .gitignore
- Added training to main
- Added .gitattributes
- Added mlflow notebooks (base, custom and feature store)
- Added Pydantic

## First PR - Branch: setup

- Corrected README.md ".venv" instead of "venv"
- Added README.md Databricks instructions
- Added install pre-commit in ci.yml
- Create databricks Schema and Volume
- Pushed data and package to schema
- Created new packages
- Created logs file
- Added larger size data for pre-commit (upt to 3 MB)
- Added pytest, loguru, precommit, imbalanced-learn and ruff in dependencies
- Added Makefile
