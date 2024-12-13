# Learn FastAPI

## Format 

```shell
poetry run black src
poetry run isort src
poetry run pylint src
poetry run mypy src
```

## Add dependency

```shell
poetry add fastapi
```

## Add dev dependency

```shell
poetry add isort --group dev
```

## Install

```shell
poetry install
```

### Start dev

```shell
poetry shell
uvicorn src.main:app --reload --host 0.0.0.0 --port 3000
```

### Create migration

```shell
alembic revision -m "create user"
```

### Apply migration

```shell
alembic upgrade head
```
