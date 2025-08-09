FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY toto/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY toto/ ./toto/
WORKDIR /app/toto

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "toto.wsgi:application", "--bind", "0.0.0.0:8000"]
