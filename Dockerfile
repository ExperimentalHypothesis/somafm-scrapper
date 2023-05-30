FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN python -m venv .venv &&  \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [".venv/bin/python", "main.py"]

