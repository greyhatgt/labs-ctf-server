FROM python:3.7-slim-buster

WORKDIR /app
ADD . /app
EXPOSE 1000
ENTRYPOINT [ "python", "main.py" ]