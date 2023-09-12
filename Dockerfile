FROM python:3.11-slim as build
ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1 

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential gcc 

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/venv ./venv
COPY --chown=python:python . .

USER 999
ENV BROKER=broker.emqx.io
ENV PORT=1883
ENV TOPIC=/test/#
ENV USER=emqx
ENV PASSWORD=public
ENV PATH="/usr/app/venv/bin:$PATH"
CMD [ "python", "app.py" ]
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health