import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd


def do_stuff_on_page_load():
    st.set_page_config(layout="wide")


do_stuff_on_page_load()

col1, col2 = st.columns(2)

df_rainy_month = pd.DataFrame({"months": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], "rainy_days": [45, 16, 27, 42, 170, 967, 973, 754, 376, 145, 71, 9]})
fig = px.pie(df_rainy_month, values='rainy_days', names='months', title='Percentage of rain in specific month in last 6 years')


df_rainy_days = pd.DataFrame({"days": range(1, 32), "rainy_days": [113, 135, 137, 141, 185, 155, 120, 119, 101, 162, 103, 121, 125, 109, 136, 126, 127, 133, 126, 111, 103, 115, 110, 99, 107, 99, 81, 90, 83, 87, 37]})
fig1 = px.pie(df_rainy_days, values='rainy_days', names='days', title='Percentage of rain in specific day in last 6 years')


df_rainy_year =  pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "rainy_days": [1000, 1287, 1349, 882, 902, 405]})
fig2 = px.pie(df_rainy_year, values='rainy_days', names='years', title='Percentage of rain in an year in last 6 years')


avg_temp_df = pd.DataFrame({"years": [ 2017, 2018, 2019, 2020, 2021, 2022], "avg_temp": [299.17, 296.75, 297.69, 298.15, 297.27, 295.35]})
fig3 = px.bar(avg_temp_df, x='years', y='avg_temp', color='avg_temp', title='Average Temperature in Last 6 Years')


avg_wind_speed_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "avg_wind_speed": [ 3.815488, 4.103544, 4.203423, 2.766489, 2.804709, 2.839636]})
fig4 = px.bar(avg_wind_speed_df, x='years', y='avg_wind_speed', color='avg_wind_speed', title='Average Wind Speed in Last 6 Years')


avg_humidity_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "avg_humidity": [65.425311, 79.662222, 74.879335, 68.106355,  71.269577, 65.82878]})
fig5 = px.bar(avg_humidity_df, x='years', y='avg_humidity', color='avg_humidity', title='Average Humidity in Last 6 Years')


avg_pressure_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "avg_pressure": [1010.368257, 1009.006667,  996.747719, 998.506554,  991.167047, 981.863388]})
fig6 = px.bar(avg_pressure_df, x='years', y='avg_pressure', color='avg_pressure', title='Average Pressure in Last 6 Years')


min_max_temp_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "temps": [309.070000, 304.860000, 304.860000, 308.020000, 308.860000, 302.070000, 293.170000, 293.170000, 291.860000, 287.860000, 286.860000, 287.860000],
                            "type": ["max", "max", "max", "max", "max", "max", "min", "min", "min", "min", "min", "min" ]}) 
fig11 = px.line(min_max_temp_df, x="years", y="temps", markers=True, color="type", title="Maximum and Minimum Temperature in Last 6 years")



wind_speed_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "min_wind_speed": [6.500, 4.04500000, 3.900000, 2.000000, 2.400, 3.7500000, 
                                                                                                                                    21.600000, 9.300000, 11.800000, 9.800000, 12.350000, 7.200000],
                            "type": ["min", "min", "min", "min", "min", "min", "max", "max", "max", "max", "max", "max" ]})
fig13 = px.line(wind_speed_df, x="years", y="min_wind_speed", markers=True, color="type", title="Maximum and Minimum Wind Speed in Last 6 years")


humidity_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "min_max_humidity": [14.000000, 48.000000, 40.000000, 14.000000, 14.000000, 22.00000, 
                                                                                                                                    100.000000, 98.000000, 100.000000, 99.9, 100.000000, 100.000000],
                            "type": ["min", "min", "min", "min", "min", "min", "max", "max", "max", "max", "max", "max" ]})
fig9 = px.line(humidity_df, x="years", y="min_max_humidity", markers=True, color="type", title="Maximum and Minimum humidity in Last 6 years")


pressure_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "min_max_pressure": [1000.000000, 1002.200000, 906.000000, 903.000000, 904.000000, 909.000000, 
                                                                                                                                    1018.000000, 1015.000000, 1019.000000, 1022.300000, 1021.000000, 1023.000000],
                            "type": ["min", "min", "min", "min", "min", "min", "max", "max", "max", "max", "max", "max" ]})

fig10 = px.line(pressure_df, x="years", y="min_max_pressure", markers=True, color="type", title="Maximum and Minimum Pressure in Last 6 years")


avg_wind_deg_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "avg_wind_deg": [215.418050, 237.078889, 239.078889, 174.372490,  153.667861, 109.595628]})
fig7 = px.bar(avg_wind_deg_df, x='years', y='avg_wind_deg', color='avg_wind_deg', title='Average Wind Direction in Last 6 Years')


wind_deg_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "min_max_wind_deg": [0.000000, 0.000000, 0.000000, 0.000000, 0.0000000, 0.000000, 
                                                                                                                                     360.000000,  350.000000, 360.000000, 360.000000, 360.000000, 360.000000],
                            "type": ["min", "min", "min", "min", "min", "min", "max", "max", "max", "max", "max", "max" ]})

fig12 = px.line(wind_deg_df, x="years", y="min_max_wind_deg", markers=True, color="type", title="Maximum and Minimum Wind Deg in Last 6 years")


avg_dew_point_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022], "avg_dew_point": [291.220197, 292.815667, 292.566644, 291.049585,   290.789969, 287.730383]})
fig8 = px.bar(avg_dew_point_df, x='years', y='avg_dew_point', color='avg_dew_point', title='Average Dew Point in Last 6 Years')


dew_point_df = pd.DataFrame({"years": [2017, 2018, 2019, 2020, 2021, 2022, 2017, 2018, 2019, 2020, 2021, 2022], "min_max_dew_point": [275.820000, 289.700000, 286.950000, 273.530000, 269.280000,273.940000, 
                                                                                                                                      299.990000, 296.320000, 296.860000,  297.330000, 301.520000, 297.820000],
                            "type": ["min", "min", "min", "min", "min", "min", "max", "max", "max", "max", "max", "max" ]})
fig14 = px.line(dew_point_df, x="years", y="min_max_dew_point", markers=True, color="type", title="Maximum and Minimum Dew Point in Last 6 years")


with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.plotly_chart(fig1, use_container_width=True)

with col1:
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.plotly_chart(fig3, use_container_width=True)

with col1:
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.plotly_chart(fig5, use_container_width=True)

with col1:
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.plotly_chart(fig7, use_container_width=True)

with col1:
    st.plotly_chart(fig8, use_container_width=True)

with col2:
    st.plotly_chart(fig9, use_container_width=True)

with col1:
    st.plotly_chart(fig10, use_container_width=True)

with col2:
    st.plotly_chart(fig11, use_container_width=True)

with col1:
    st.plotly_chart(fig12, use_container_width=True)

with col1:
    st.plotly_chart(fig13, use_container_width=True)

with col2:
    st.plotly_chart(fig14, use_container_width=True)
