FROM python:3.11-slim

WORKDIR /app

COPY laddr-webhook.py /app/laddr-webhook.py

EXPOSE 8080

CMD ["python", "-u", "laddr-webhook.py", "--port", "8080"]
