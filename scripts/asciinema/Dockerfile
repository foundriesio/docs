FROM frolvlad/alpine-glibc:alpine-3.12

RUN apk add bash wget asciinema --no-cache && adduser -D -s /bin/sh gavin && mkdir /home/gavin/.config && chown -R gavin:gavin /home/gavin/.config

COPY ./entrypoint.sh ./entrypoint.sh

WORKDIR /home/gavin

CMD ["sh", "/entrypoint.sh"]
