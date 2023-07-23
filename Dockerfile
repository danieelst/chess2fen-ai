FROM tensorflow/tensorflow:latest-gpu

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install
RUN apt-get -y install libpangocairo-1.0-0
RUN pip3 install -r requirements.txt
