FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends tini git && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN mkdir -p data models artifacts .cache
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["python","-m","pipeline.monitor","--help"]

