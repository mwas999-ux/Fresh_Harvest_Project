FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure static and media folders exist
RUN mkdir -p staticfiles media

# Combined command: Migrate -> Collect Static -> Run
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT