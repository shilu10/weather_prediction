FROM python:3.10.8-buster

EXPOSE 8501

WORKDIR app/

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY live_weather_dashboard/ .

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "streamlit", "run", "live_weather_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
