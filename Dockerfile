# Dockerfile is based on the following tutorial:
# https://www.erraticbits.ca/post/2021/fastapi/

# Build step #1: build the React front end
FROM node:20-bookworm-slim as build-step

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/package.json  ./

RUN npm install

COPY ./frontend/ ./

RUN npm run build


FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry for packages management
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false

# Use /app as the working directory
WORKDIR /app

# Copy poetry files & install the dependencies
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
COPY --from=build-step /app/dist /app/static

RUN poetry install --no-interaction --no-ansi --no-root --without dev
RUN python -c 'from fastembed.embedding import DefaultEmbedding; DefaultEmbedding("sentence-transformers/all-MiniLM-L6-v2")'

# Finally copy the application source code and install root
COPY qdrant_demo /app/qdrant_demo

EXPOSE 8000

CMD uvicorn qdrant_demo.service:app --host 0.0.0.0 --port 8000 --workers ${WORKERS:-1}

