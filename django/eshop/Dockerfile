FROM python:3.13-slim

WORKDIR /app
EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c"]

CMD ["python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 eshop.wsgi:application"]