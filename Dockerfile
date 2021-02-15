FROM alpine:latest

RUN apk add python3 py3-pip py3-setuptools

RUN mkdir -p /ghp-cleanup
WORKDIR /ghp-cleanup

COPY requirements.txt ghp-cleanup.py docker_entrypoint.sh ./
RUN pip install -r requirements.txt

ENTRYPOINT /ghp-cleanup/docker_entrypoint.sh
