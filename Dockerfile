FROM ubuntu:latest

COPY . /gazer
COPY gazer/config/. /config

RUN apt-get update \
    && apt-get install -y python3-pip python3 \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN cd /gazer \
    && pip install . 

CMD ["python", "./gazer/bin/gazer"]
