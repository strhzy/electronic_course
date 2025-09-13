FROM python:3.13-slim

WORKDIR /app
EXPOSE 5250

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install gunicorn

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "-c"]

CMD ["python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 eshop.wsgi:application"]