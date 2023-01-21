FROM python:3.10.9-bullseye
ARG POETRY_VERSION=1.3.1

RUN apt-get update && apt-get install -y \
  llvm-11 \
  llvm-11-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

