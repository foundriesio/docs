FROM alpine:3.13

COPY requirements.txt /

RUN apk add --no-cache --virtual .build-deps build-base python3-dev && \
    apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache --upgrade setuptools wheel && \
    pip3 install --no-cache -r /requirements.txt && \
    apk del .build-deps

WORKDIR /git/mkdocs

EXPOSE 8000/tcp
