import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



case = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recover = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

st.write("# Distribution of Cases, Recoveries and Deaths")

rb = st.radio(
     "Select the data",
     ('Cases', 'Recoveries', 'Deaths'))
st.write("You've selected daily " + rb)

y = case[case['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).unstack()
y = np.asarray(y)  
y = y[1 : y.size] - y[0 : (y.size - 1)]
y =  y[np.min(np.where(y !=  0)) : y.size]

r = recover[recover['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).unstack()
r = np.asarray(r)

d = deaths[deaths['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).unstack()
d = np.asarray(d)  
d = d[1 : d.size] - d[0 : (d.size - 1)]
d =  d[np.min(np.where(d !=  0)) : d.size]

if rb == "Cases" : 
    st.line_chart(y)
if rb == "Recoveries" :
    st.line_chart(r)
if rb == "Deaths":
    st.line_chart(d)

