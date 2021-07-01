FROM python:3.9.5-slim-buster
LABEL maintainer="ppotatoo"

RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        git; \
    rm -rf /var/lib/apt/lists/*;

WORKDIR /
COPY requirements.txt /

RUN pip install --use-deprecated=legacy-resolver -U -r requirements.txt

COPY / /web


COPY docker_run.sh /run.sh

WORKDIR /web/src/

ENTRYPOINT ["sh"]
CMD ["/run.sh"]

EXPOSE 8000/tcp