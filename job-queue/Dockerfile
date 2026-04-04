FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    boto3 \
    requests \
    python-dateutil \
    tenacity

# Copy worker script
COPY worker.py /app/worker.py
COPY config.yaml /app/config.yaml

# Run worker
CMD ["python", "-u", "worker.py"]
