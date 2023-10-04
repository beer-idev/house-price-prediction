import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import altair as alt

PATH = 'web5.csv'

df = pd.read_csv(PATH)
df = df.drop(["Unnamed: 0"], axis=1)

st.sidebar.header("Filter")
selected_location = st.sidebar.multiselect("Location", sorted(list(df.location.unique())), sorted(list(df.location.unique())))
selected_bedroom = st.sidebar.selectbox("Bedrooms", sorted(list(df.bedroom.unique())))
# price_min = int(df['price'].min())
# price_max = int(df['price'].max())
# price_range = st.sidebar.slider("Price Range", price_min, price_max, (price_min, price_max), step=1000)
price_input = st.sidebar.number_input('Price', min_value=0)



# @st.cache
def filter_data(locations, bedrooms, price, data): 
    data = data[(data.location.isin(locations))]
    data = data[data['bedroom'].isin([bedrooms])]

    data['price_difference'] = abs(data['price'] - price)
    data = data.sort_values(by='price_difference').head(10)
    return data

df = filter_data(selected_location, selected_bedroom, price_input, df)
st.header("Prediction Data")
st.write(df)

st.header("Price Trends")
location_price_trends = df.groupby('location')['price'].sum()
st.bar_chart(location_price_trends)

location_price_trends1 = df.groupby('location')['price'].mean()
location_price_trends1 = location_price_trends1.reset_index()  # Reset the index for the DataFrame

st.subheader("Average Price Trends by Location (Table)")
st.write(location_price_trends1)

st.header("Area Trends")
location_area_trends = df.groupby('location')['area'].sum()
st.bar_chart(location_area_trends)

table_location_area_trends = df.groupby('location')['area'].mean()
table_location_area_trends = table_location_area_trends.reset_index()  # Reset the index for the DataFrame

st.subheader("Average Area Trends by Location (Table)")
st.write(table_location_area_trends)