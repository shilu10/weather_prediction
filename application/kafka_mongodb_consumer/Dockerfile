FROM python:3.10.8-buster

WORKDIR app/

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app/ .

RUN pip3 install -r requirements.txt

CMD ["python3", "mongodb_consumer.py"]
