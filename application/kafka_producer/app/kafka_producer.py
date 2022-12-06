from kafka import KafkaProducer 
import json, requests
import time 
import os


topic_name = "top"
kafka_server = os.environ["bootstrap_server"]
producer = KafkaProducer(bootstrap_servers=kafka_server)
history_topic_name = "weather_data"

api_key = os.environ["api_key"]

lat = 12.9989
lon = 77.592

def get_weather_data(api_key, lat, lon):
    weather_dict = { }
    try: 
        weather_result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")
        weather_result = json.loads(weather_result.text)

        weather_dict.update({"visibility": float(weather_result.get("visibility"))})
        wind = weather_result.get("wind")
        weather_dict.update({"wind_speed": float(wind.get("speed"))})
        weather_dict.update({"wind_deg": float(wind.get("deg"))})
        main_data = weather_result.get("main")
        weather_dict.update({"temp": float(main_data.get("temp"))})
        weather_dict.update({"pressure": float(main_data.get("pressure"))})
        weather_dict.update({"humidity": float(main_data.get("humidity"))})
        print(visibility, temp, pressure, humidity)
        
        weather_dict = json.dumps(weather_dict, indent=2).encode('utf-8')
        producer.send(topic_name, weather_dict)
        
    except Exception as err: 
        print(err)
    
    finally: 
        time.sleep(10)
        get_weather_data(api_key, lat, lon)

count = 0

def get_weather_history_data(api_key, lat, lon, count):

    if count == 0:
        time.sleep(20)
    weather_dict = {
        "temp": [],
        "humidity": [],
        "pressure": [],
        "wind_speed": [],
        "wind_deg": [],
        "dew_point": [],
        "clouds": [],
        "feels_like": []
    }
    try:
        current_time = time.time()
        diff = 23419
        _time = current_time

        for look_before in range(7): 
            weather_result = requests.get(f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&appid={api_key}&dt={round(_time)}")
            weather_result = json.loads(weather_result.text)
            
            weather_result = weather_result.get("data")[0]
            weather_dict.get("feels_like").append(float(weather_result.get("feels_like")))
            weather_dict.get("wind_speed").append(float(weather_result.get("wind_speed")))
            weather_dict.get("wind_deg").append(float(weather_result.get("wind_deg")))
          
            weather_dict.get("temp").append(float(weather_result.get("temp")))
            weather_dict.get("pressure").append(float(weather_result.get("pressure")))
            weather_dict.get("humidity").append(float(weather_result.get("humidity")))
            weather_dict.get("clouds").append(float(weather_result.get("clouds")))
            weather_dict.get("dew_point").append(float(weather_result.get("dew_point")))
            #print(visibility, temp, pressure, humidity)
            print(weather_dict)
            _time -= diff 

        weather_dict = json.dumps(weather_dict, indent=2).encode('utf-8')
        producer.send(history_topic_name, weather_dict)
            
    except Exception as err: 
        print(err)
    
    finally: 
        time_to_sleep = 3600
        if count < 6:
            time_to_sleep = 25
            count += 1

        time.sleep(time_to_sleep)
        count += 1
        get_weather_history_data(api_key, lat, lon, count)
        

#get_weather_data(api_key, lat, lon)
get_weather_history_data(api_key, lat, lon, count)
