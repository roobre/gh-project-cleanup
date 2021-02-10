FROM alpine:latest

RUN apk add python3 py3-pip py3-setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ghp-cleanup.py .
COPY docker_entrypoint.sh .

ENTRYPOINT ./docker_entrypoint.sh