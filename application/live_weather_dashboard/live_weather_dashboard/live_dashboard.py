import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
import json 
from pymongo import MongoClient
import pymongo
import os

database_name = "weather_data"
collection_name = "weather"

def do_stuff_on_page_load():
    st.set_page_config(layout="wide")

do_stuff_on_page_load()

db_url = os.environ["mongodb_url"]
data_dict = {} 
client = pymongo.MongoClient(db_url)

document = client.weather_data.weather.find()
for rec in document:
    data_dict = rec
    

col1, col2 = st.columns(2)

df_pressure = pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "pressure": data_dict["pressure"]})
fig1 = px.bar(df_pressure, x='hours', y='pressure', color='pressure', title='Pressure')

df_humidity = pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "humidity": data_dict["humidity"]})
fig2 = px.bar(df_humidity, x='hours', y='humidity', color='humidity', title='Humidity')

df_wind_speed =  pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "wind_speed": data_dict["wind_speed"]})
fig3 = px.bar(df_wind_speed, x='hours', y='wind_speed', color='wind_speed', title='Wind Speed')

df_wind_deg = pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "wind_deg": data_dict["wind_deg"]})
fig4 = px.bar(df_wind_deg, x='hours', y='wind_deg', color='wind_deg', title='wind_deg')

df_dew_point = pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "dew_point": data_dict["dew_point"]})
fig5 = px.bar(df_dew_point, x='hours', y='dew_point', color='dew_point', title='dew_point')

df_clouds =  pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "clouds": data_dict["clouds"]})
fig6 = px.bar(df_clouds, x='hours', y='clouds', color='clouds', title='clouds')

df_temperature =  pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "temperature": data_dict["temperature"]})
fig7 = px.bar(df_temperature, x='hours', y='temperature', color='temperature', title='temperature')

df_feels_like =  pd.DataFrame({"hours": ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"], "feels_like": data_dict["feels_like"]})
fig8 = px.bar(df_feels_like, x='hours', y='feels_like', color='feels_like', title='feels_like')


with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

with col1:
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig4, use_container_width=True)

with col1:
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.plotly_chart(fig6, use_container_width=True)

with col1:
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    st.plotly_chart(fig8, use_container_width=True)
