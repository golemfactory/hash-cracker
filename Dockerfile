FROM python:3.8.7-slim
RUN mkdir -p /golem/entrypoint
COPY worker.py /golem/entrypoint/
VOLUME /golem/input /golem/output
WORKDIR /golem/entrypoint
