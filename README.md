# Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
git submodule init
git submodule update
```


# Alembic (migrations)

### Create migration
```bash
env DB_USER='BSD' DB_PASS='bonjour' DB_HOST='localhost' DB_NAME='BSD' alembic revision --autogenerate -m "Create a baseline migrations"
```

### Apply migrations
```bash
env DB_USER='BSD' DB_PASS='bonjour' DB_HOST='localhost' DB_NAME='BSD' alembic upgrade head
```

### Revert latest migration
```bash
env DB_USER='BSD' DB_PASS='bonjour' DB_HOST='localhost' DB_NAME='BSD' alembic downgrade -1
```