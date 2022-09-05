FROM python:3.10.4-slim as builder

WORKDIR /app

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y
RUN apt-get install curl -y

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN ["chmod", "+x", "./docker-entrypoint.sh", "./wait.sh"]
CMD ["./wait.sh"]