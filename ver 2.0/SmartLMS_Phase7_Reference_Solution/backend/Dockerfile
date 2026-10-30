FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies in a separate layer.
COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy Flask application, migrations and source.
COPY . .

EXPOSE 5000

CMD ["flask", "--app", "run.py", "run", "--host=0.0.0.0", "--port=5000"]
