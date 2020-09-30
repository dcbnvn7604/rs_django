FROM python:3.7-slim-stretch

COPY Pipfile Pipfile.lock /django/

WORKDIR /django

RUN apt update && \
    apt install -y gcc libpq-dev && \
    pip install pipenv && \
    pipenv install

ENTRYPOINT ["bash"]
