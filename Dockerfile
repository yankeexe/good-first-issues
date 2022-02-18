FROM python:3.9-slim-buster as build

RUN apt-get update && apt install -y gcc && \
    useradd -ms /bin/bash gfi

USER gfi

WORKDIR /home/gfi

COPY --chown=gfi:gfi . .

RUN pip install --no-cache-dir --user .

FROM python:3.9-alpine

LABEL description="Find good first issues right from your CLI!"

RUN apk update && \
    apk upgrade expat libuuid && \
    apk add --no-cache ncurses && \
    rm -rf /var/cache/apk/* && \
    addgroup -S gfi && adduser -S gfi -u 1000

USER gfi

WORKDIR /home/gfi

ENV PATH=$PATH:/home/gfi/.local/bin

COPY --from=build --chown=gfi /home/gfi/.local /home/gfi/.local/

ENTRYPOINT [ "gfi" ]
