FROM python:3.10.8-alpine3.17
COPY app/ .
RUN pip3 install -r requirements.txt
CMD ["python3", "kafka_producer.py"]


