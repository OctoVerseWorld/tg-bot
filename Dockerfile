###########
# BUILDER #
###########
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root



###########
## IMAGE ##
###########
FROM python:3.13-slim

WORKDIR /home/appuser/app

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /home/appuser/app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

COPY . /home/appuser/app

RUN sed -i 's/\r$//' /home/appuser/app/start_app.sh && \
    chmod +x /home/appuser/app/start_app.sh

USER appuser

ENTRYPOINT ["./start_app.sh"]
