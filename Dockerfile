FROM python:3.13-slim
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates lsb-release && \
    wget --quiet -O /usr/share/keyrings/postgresql.gpg https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
    echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
        > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y postgresql-client-15 && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c"]

CMD ["python manage.py migrate --fake-initial --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 eshop.wsgi:application"]