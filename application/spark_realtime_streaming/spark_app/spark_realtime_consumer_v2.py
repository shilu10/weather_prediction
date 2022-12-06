import os
from pyspark.sql.types import StructType, IntegerType, FloatType, ArrayType, StringType
from pyspark.sql.functions import col, udf
from pyspark.sql import SparkSession 
from pyspark.streaming import StreamingContext
import json
from tensorflow.keras.models import load_model
from abc import abstractmethod, abstractstaticmethod
from keras.preprocessing.sequence import TimeseriesGenerator
import numpy as np
import pandas as pd
import joblib

scala_version = '2.12'
spark_version = '3.1.2'
kafka_server = "172.18.0.3:9092"
topic_name = "top"
# 172.18.0.3
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
]

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

spark = SparkSession.builder\
   .master("spark://instance-1.c.ceremonial-hold-369707.internal:7077")\
   .appName("kafka-example")\
   .config("spark.jars.packages", ",".join(packages))\
   .getOrCreate()


df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", topic_name) \
    .option("auto_offset_reset", "earliest") \
    .load()


weatherSchema = StructType() \
     .add("visibility", IntegerType(), True) \
     .add("wind_speed", IntegerType(), True) \
     .add("wind_deg", IntegerType(), True) \
     .add("pressure", IntegerType(), True) \
     .add("humidity", IntegerType(), True) \
     .add("temp", IntegerType(), True) \
     .add("clouds", IntegerType(), True)


class LoadTensorFlowModelInterface: 

  @abstractmethod
  def _load_model(self): 
    pass 

  @abstractmethod
  def broadcasted_model(self): 
    pass 


class TemperatureModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass

    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model 


class HumidityModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass
    
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


class WindSpeedModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass
    
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


class WindDegModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass
  
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


class PressureModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass
  
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


class DewPointModel(LoadTensorFlowModelInterface): 
  
    def __init__(self): 
        pass
    
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


class CloudModel(LoadTensorFlowModelInterface):
  
    def __init__(self):
        pass
  
    def _load_model(self, path: str) -> object:
        loaded_model = load_model(path)
        return loaded_model

    def broadcasted_model(self, model):
        br_model = spark.sparkContext.broadcast(model)
        return br_model


def data_reader_udf(data):
    """
        This Function will convert the string of weather data into the list of weather
        data. 
    """
    try: 
        data = json.loads(data)
        data_list = [data.get("temp"),
                        data.get("humidity"),
                        data.get("pressure"),
                        data.get("wind_speed"),
                        data.get("wind_deg"),
                        data.get("dew_point"),
                        data.get("clouds"),
                        data.get("feels_like"),
                ]
        return data_list

    except Exception as err:
        print(err) 


udf_function = udf(data_reader_udf, ArrayType(ArrayType(FloatType())))


class ModelClient: 

    @abstractmethod
    def _load_model(self): 
        pass 


class LGBModelClient(ModelClient): 

    def __init__(self): 
        pass 

    def _load_model(self, path): 
        
        try: 
            model = joblib.load(path)
            return model

        except Exception as err:
            return err 

    def broadcasted_model(self, model): 
        br_model = spark.sparkContext.broadcast(model)
        return br_model


def create_timeseries_generator(dt, look_before): 

    try: 
        test_generator = TimeseriesGenerator(dt, dt, look_before)
        return test_generator

    except Exception as err:
        return err 


lgb = LGBModelClient()
lgb_model = lgb._load_model("../models/lgb_weather_model.pkl")
lgb_model = lgb.broadcasted_model(lgb_model)

cloud = CloudModel()
cloud_model = cloud._load_model("../models/dew_point_model_lstm.h5")
_broadcasted_cloud_model = cloud.broadcasted_model(cloud_model)

dewpoint = DewPointModel()
dewpoint_model = dewpoint._load_model("../models/dew_point_model_lstm.h5")
_broadcasted_dewpoint_model = dewpoint.broadcasted_model(dewpoint_model)

pressure_obj = PressureModel() 
pressure_model = pressure_obj._load_model("../models/pressure_lstm_model.h5")
_broadcasted_pressure_model = pressure_obj.broadcasted_model(pressure_model)

humidity_obj = HumidityModel()
humidity_model = humidity_obj._load_model("../models/humidity_model_lstm.h5")
_broadcasted_humidity_model = humidity_obj.broadcasted_model(humidity_model)

wind_deg_obj = WindDegModel()
wind_deg_model = wind_deg_obj._load_model("../models/wind_deg_model_lstm.h5")
_broadcasted_wind_deg_model = wind_deg_obj.broadcasted_model(wind_deg_model)

wind_speed_obj = WindDegModel()
wind_speed_model = wind_speed_obj._load_model("../models/wind_speed_lstm_model.h5")
_broadcasted_wind_speed_model = wind_speed_obj.broadcasted_model(wind_speed_model)

temp_obj = TemperatureModel()
temp_model = temp_obj._load_model("../models/temperature_lstm.h5")
_broadcasted_temp_model = temp_obj.broadcasted_model(temp_model)


def load_generators(**kwargs): 

    try: 
        temp_generator = create_timeseries_generator(np.array(kwargs.get("temp")), 6) 
        pressure_generator = create_timeseries_generator(np.array(kwargs.get("pressure")), 2)
        wind_speed_generator = create_timeseries_generator(np.array(kwargs.get("wind_speed")), 2)
        wind_deg_generator = create_timeseries_generator(np.array(kwargs.get("wind_deg")), 2)
        humidity_generator = create_timeseries_generator(np.array(kwargs.get("humidity")), 2)
        dew_point_generator = create_timeseries_generator(np.array(kwargs.get("dew_point")), 2)
        cloud_generator = create_timeseries_generator(np.array(kwargs.get("cloud")), 2)
        feels_like_generator = create_timeseries_generator(np.array(kwargs.get("feels_like")), 2)

        return [
                temp_generator, 
                pressure_generator, 
                wind_speed_generator,
                wind_deg_generator,
                humidity_generator,
                dew_point_generator,
                cloud_generator,
                feels_like_generator  
            ]
    
    except Exception as err:
        return err 


def predict(**kwargs): 

    try: 
        feels_like_prediction = _broadcasted_temp_model.value.predict(kwargs.get("feels_like_generator")) 
        cloud_prediction = _broadcasted_cloud_model.value.predict(kwargs.get("cloud_generator"))
        temp_prediction = _broadcasted_temp_model.value.predict(kwargs.get("temp_generator"))
        humidity_prediction = _broadcasted_humidity_model.value.predict(kwargs.get("humidity_generator"))
        pressure_prediction = _broadcasted_pressure_model.value.predict(kwargs.get("pressure_generator"))
        wind_deg_prediction = _broadcasted_wind_deg_model.value.predict(kwargs.get("wind_deg_generator"))
        wind_speed_prediction = _broadcasted_wind_speed_model.value.predict(kwargs.get("wind_speed_generator"))
        dew_point_predicton = _broadcasted_dewpoint_model.value.predict(kwargs.get("dew_point_generator"))

        return [
            feels_like_prediction[-1][0],
            cloud_prediction[-1][0],
            temp_prediction[-1][0],
            humidity_prediction[-1][0],
            pressure_prediction[-1][0],
            wind_deg_prediction[-1][0],
            wind_speed_prediction[-1][0],
            dew_point_predicton[-1][0],
        ]

    except Exception as err:
        return err 

def prediction_function(dataset):
    
    final_predictions = []
    weather_predictions = []
    temp = dataset[0][::-1]
    humidity = dataset[1][::-1]
    pressure = dataset[2][::-1]
    wind_speed = dataset[3][::-1]
    wind_deg = dataset[4][::-1]
    dew_point = dataset[5][::-1]
    cloud = dataset[6][::-1]
    feels_like = dataset[7][::-1]

    no_of_look_ahead = 5
    
    print(temp, humidity, pressure, wind_speed, wind_deg, dew_point, cloud, feels_like)
    for _ in range(no_of_look_ahead): 
        
         #'clear sky', 'few clouds', 'mist', 'rain', 'scattered clouds'
        _classes = {
            "clear sky": 0.0,
            "few clouds": 1.0,
            "mist": 2.0,
            "rain": 3.0,
            "scattered clouds": 4.0
        }

        generators = load_generators(temp=temp[-7: ], 
                    pressure=pressure[-3: ],
                    wind_speed=wind_speed[-3: ],
                    wind_deg=wind_deg[-3: ],
                    humidity=humidity[-3: ],
                    dew_point=dew_point[-3: ],
                    cloud=cloud[-3: ],
                    feels_like=feels_like[-3: ]    
                    )

        temp_generator = generators[0]
        pressure_generator = generators[1]
        wind_speed_generator = generators[2]
        wind_deg_generator = generators[3]
        humidity_generator = generators[4]
        dew_point_generator = generators[5]
        cloud_generator = generators[6]
        feels_like_generator = generators[7]

        lstm_predictions = predict(
                            feels_like_generator=feels_like_generator,
                            wind_deg_generator=wind_deg_generator,
                            wind_speed_generator=wind_speed_generator,
                            dew_point_generator=dew_point_generator,
                            temp_generator=temp_generator,
                            pressure_generator=pressure_generator,
                            humidity_generator=humidity_generator,
                            cloud_generator=cloud_generator,
                        )
            
        feels_like_prediction = float(lstm_predictions[0])
        cloud_prediction = float(lstm_predictions[1])
        temp_prediction = float(lstm_predictions[2])
        humidity_prediction = float(lstm_predictions[3])
        pressure_prediction = float(lstm_predictions[4])
        wind_deg_prediction = float(lstm_predictions[5])
        wind_speed_prediction = float(lstm_predictions[6])
        dew_point_prediction = float(lstm_predictions[7])
            
        temp.append(temp_prediction)
        cloud.append(cloud_prediction)
        wind_speed.append(wind_speed_prediction)
        wind_deg.append(wind_deg_prediction)
        pressure.append(pressure_prediction)
        humidity.append(humidity_prediction)
        feels_like.append(feels_like_prediction)
        dew_point.append(dew_point_prediction)

        lgb_prediction = lgb_model.value.predict([[temp_prediction, 
                                        feels_like_prediction,
                                        pressure_prediction,
                                        humidity_prediction,
                                        dew_point_prediction, 
                                        cloud_prediction, 
                                        wind_speed_prediction, 
                                        wind_deg_prediction,
                                    ]])

        weather_predictions.append(_classes[str(lgb_prediction[0])])   
    

    final_predictions.append([weather_predictions, temp, cloud, humidity, wind_speed, pressure, dew_point, feels_like, wind_deg])
    return final_predictions

udf_function_for_prediction = udf(prediction_function, ArrayType(ArrayType(ArrayType(FloatType()))))


def processing_func(batch_df, batch_id): 
    batch_df = batch_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    batch_df = batch_df.withColumn("transformed_data", udf_function(batch_df.value))
    udf_function_for_prediction(batch_df.transformed_data)
    batch_df = batch_df.withColumn("predictions", udf_function_for_prediction(batch_df.transformed_data))
    batch_df =  batch_df.drop("value")
    batch_df = batch_df.drop("transformed_data")
    batch_df = batch_df.withColumnRenamed("predictions", "value")
    batch_df.selectExpr("CAST(value AS STRING)") \
            .write.format("kafka")\
            .option("kafka.bootstrap.servers", kafka_server)\
            .option("topic", "predictions")\
            .save()

writer = df.writeStream.trigger(processingTime='30 seconds').foreachBatch(processing_func).start().awaitTermination()
