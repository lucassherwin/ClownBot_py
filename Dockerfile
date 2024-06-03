FROM python:3.11-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/workdir/src

WORKDIR /workdir
RUN pip install hatch

COPY pyproject.toml README.md ./
COPY src/clown_bot src/clown_bot
RUN hatch env create main
CMD ["hatch", "run", "main:bot"]
