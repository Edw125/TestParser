FROM python:3.10.4-slim as builder

WORKDIR /app

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]