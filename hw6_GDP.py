import streamlit as st
import requests as rq
import bs4
import pandas as pd
import plotly.express as px

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
page = rq.get(url)

bs4page = bs4.BeautifulSoup(page.text, 'html.parser')
tables = bs4page.find_all('table',{'class':"wikitable"})

from io import StringIO
GDP = pd.read_html(StringIO(str(tables[0])))[0]
GDP.head()

GDP2 = GDP[1:].copy()
GDP2.columns = GDP2.columns.droplevel(0)
new_column_names = ['Country/Territory', 'UN region', 'IMF_Forecast', 'IMF_Year', 'World_Bank_Estimate', 'World_Bank_Year', 'United_Nations_Estimate', 'United_Nations_Year']
GDP2.columns = new_column_names
GDP2.head()

columns_to_numeric = ['IMF_Forecast', 'World_Bank_Estimate', 'United_Nations_Estimate']
GDP2[columns_to_numeric] = GDP2[columns_to_numeric].apply(pd.to_numeric, errors='coerce')

source = st.radio(
     "Which source of GDP estimate do you want?",
     ('IMF', 'World Bank', 'United Nations'))

if source == "IMF":
    fig = px.bar(GDP2, x = "UN region", y = "IMF_Forecast", color = "Country/Territory")
    fig.update_layout(height=550)
    st.plotly_chart(fig)
elif source == "World Bank":
    fig = px.bar(GDP2, x = "UN region", y = "World_Bank_Estimate", color = "Country/Territory")
    fig.update_layout(height=550)
    st.plotly_chart(fig)
else:
    fig = px.bar(GDP2, x = "UN region", y = "United_Nations_Estimate", color = "Country/Territory")
    fig.update_layout(height=550)
    st.plotly_chart(fig)