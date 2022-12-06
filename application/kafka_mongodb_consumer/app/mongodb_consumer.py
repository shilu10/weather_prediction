from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import pymongo
import os

bt_server = os.environ["bootstrap_server"]
db_url = os.environ["mongodb_url"]
topic_name = os.environ["prediction_topic_name"]
consumer = KafkaConsumer(prediction_topic_name, bootstrap_servers=bt_server) #auto_offset_reset='earliest', enable_auto_commit=True)
client = pymongo.MongoClient(db_url)
db = client.weather_data
collections = db.weather
##'clear sky', 'few clouds', 'mist', 'rain', 'scattered clouds'


values = {

    "weather_predictions": [],
    "humidity" : [],
    "pressure" : [],
    "dew_point" : [],
    "feels_like" : [],
    "temperature" : [],
    "wind_speed" : [],
    "wind_deg" : [],
    "clouds" : []

}

# [weather_predictions, temp, cloud, humidity, wind_speed, pressure, dew_point, feels_like, wind_deg

def consume():
    try: 

        for message in consumer:
            data = json.loads(message.value)
            data = data[0]
            previous_values = values.copy()
            values.update({"weather_predictions": data[0]})
            values.update({"temperature": data[1]})
            values.update({"clouds": data[2]})
            values.update({"humidity": data[3]})
            values.update({"wind_speed": data[4]})
            values.update({"pressure": data[5]})
            values.update({"dew_point": data[6]})
            values.update({"feels_like": data[7]})
            values.update({"wind_deg": data[8]})    
            if not values == previous_values:
                collections.insert_one(values)
    
    except Exception as err:
        return err 

consume()

