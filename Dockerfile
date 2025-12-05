FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        nano \
        wget \
        gnupg \
        dirmngr \
        build-essential \
        ca-certificates \
        python3-dev \
        libzmq3-dev \
        libffi-dev \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g yarn

WORKDIR /src/rest
COPY src/requirements.txt /src/rest/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV ENV_TYPE=staging
ENV MONGO_HOST=mongo
ENV MONGO_PORT=27017

WORKDIR /src/app

