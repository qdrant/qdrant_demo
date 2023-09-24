FROM python:3.8

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2") '

# Creating folders, and files for a project:
COPY . /code

CMD uvicorn qdrant_demo_v2.service:app --host 0.0.0.0 --port 8000 --workers ${WORKERS:-1}

