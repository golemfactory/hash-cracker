FROM python:3.8.7-slim
VOLUME /golem/input /golem/output
COPY worker.py /golem/entrypoint/
WORKDIR /golem/entrypoint
