FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DESTINATION_DIR /hexpayloaddecoder

RUN apt-get update && \
    apt-get install -y tshark

COPY . ${DESTINATION_DIR}/

WORKDIR ${DESTINATION_DIR}

RUN pip install -r requirements.txt
