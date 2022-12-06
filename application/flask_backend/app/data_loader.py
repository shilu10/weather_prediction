from db_connector import db_connection
import math 
from datetime import datetime
import requests
import json
import os

lat = 12.9989
lon = 77.592
api_key = os.environ["api_key"]
openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

_classes = {
        0.0: "clear sky",
        1.0: "few clouds",
        2.0: "mist",
        3.0: "rain",
        4.0: "scattered clouds"
}

data_dict = {} 

mongodb_url = os.environ["mongodb_url"]
client = db_connection(mongodb_url)

def load_data(): 

    document = client.weather_data.weather.find()
    for rec in document:
        data_dict = rec

    # 0 - 5 ---> past data
    # 6 --> current data 
    # 7, 8, 9 , 10, 11 --> future data
    # Temperature is in kelvin unit.
    # Wind Speed -> Meter per sec

    current_weather = None 
    future_weather_prediction_1 = _classes[data_dict["weather_predictions"][0]]
    future_weather_prediction_2 = _classes[data_dict["weather_predictions"][1]]
    future_weather_prediction_3 = _classes[data_dict["weather_predictions"][2]]

    pressure_data_1 =  round(data_dict["pressure"][7], 1)
    pressure_data_2 =  round(data_dict["pressure"][8], 1)
    pressure_data_3 =  round(data_dict["pressure"][9], 1)

    humidity_data_1 =  round(data_dict["humidity"][7], 1)
    humidity_data_2 =  round(data_dict["humidity"][8], 1)
    humidity_data_3 =  round(data_dict["humidity"][9], 1)

    wind_speed_data_1 = round(data_dict["wind_speed"][7], 1)
    wind_speed_data_2 =  round(data_dict["wind_speed"][8], 1)
    wind_speed_data_3 =  round(data_dict["wind_speed"][9], 1)

    wind_deg_data_1 = data_dict["wind_deg"][7]
    wind_deg_data_2 = data_dict["wind_deg"][8]
    wind_deg_data_3 = data_dict["wind_deg"][9]

    dew_point_1 =  data_dict["dew_point"][7]
    dew_point_2 =  data_dict["dew_point"][8]
    dew_point_3 =  data_dict["dew_point"][9]

    clouds1 =  data_dict["clouds"][7]
    clouds2 = data_dict["clouds"][8]
    clouds3 =  data_dict["clouds"][9]

    temperature1 =  int(round((data_dict["temperature"][7] -  273.15), 0))
    temperature2 =  int(round((data_dict["temperature"][8] -  273.15), 0))
    temperature3 =  int(round((data_dict["temperature"][9] -  273.15), 0))

    dt = datetime.now()
    week_day_name = dt.strftime('%A')
    date = datetime.today().day
    current_datetime = [week_day_name, date]

    future_forecast_predictions_1 = [
                                        future_weather_prediction_1,
                                        humidity_data_1,
                                        temperature1,
                                        pressure_data_1,
                                        wind_speed_data_1,
                                        wind_deg_data_1,
                                        clouds1,
                                        dew_point_1,
                                        current_datetime
                                    ]

    future_forecast_predictions_2 = [
                                        future_weather_prediction_2,
                                        humidity_data_2,
                                        temperature2,
                                        pressure_data_2,
                                        wind_speed_data_2,
                                        wind_deg_data_2,
                                        clouds2,
                                        dew_point_2,
                                        current_datetime
                                    ]


    future_forecast_predictions_3 = [
                                        future_weather_prediction_3,
                                        humidity_data_3,
                                        temperature3,
                                        pressure_data_3,
                                        wind_speed_data_3,
                                        wind_deg_data_3,
                                        clouds3,
                                        dew_point_3,
                                        current_datetime
                                    ]

    return [future_forecast_predictions_1, future_forecast_predictions_2, future_forecast_predictions_3]



def get_current_weather(): 
    weather_result = requests.get(openweather_url)
    weather_result = json.loads(weather_result.text)
    current_weather = weather_result.get("weather")[0].get("main")
    print(weather_result)
    temp = weather_result.get("main").get("temp")
    pressure = weather_result.get("main").get("pressure")
    humidity = weather_result.get("main").get("humidity")
    wind_speed = weather_result.get("wind").get("speed")
    temp =  int(round((temp -  273.15), 0))
    dt = datetime.now()
    week_day_name = dt.strftime('%A')
    date = datetime.today().day
    current_datetime = [week_day_name, date]

    return [current_weather, temp, pressure, humidity, wind_speed, current_datetime]
