FROM python:3.10.8-buster

EXPOSE 8000

WORKDIR app/

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app/ .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-w=2", "--threads=2", "-b=0.0.0.0:8000", "app:app"]

       
