import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


@st.cache
def readData(df):
    data = pd.read_csv(df)
    data['date'] = pd.to_datetime(data['date'])
    data['bathrooms'] = np.int64(round(data['bathrooms']-0.3))
    data['floors'] = np.int64(round(data['floors']-0.3))
    data['waterfront'] = data['waterfront'].apply(lambda x: 'SIM' if x == 1 else 'NÃO')
    data['age'] = np.int64(np.int64(pd.to_datetime(data['date']).dt.strftime('%Y')) - data['yr_built'])
    data.drop(columns=['sqft_lot', 'sqft_above', 'sqft_basement', 'yr_renovated', 'sqft_living15', 'sqft_lot15'], axis=1, inplace=True)

    return data


dataframe = readData('https://raw.githubusercontent.com/HedvaldoCosta/DataScience/main/KcHouse/Datasets/kc_house_data.csv')

mapa = folium.Map(location=[dataframe['lat'].mean(), dataframe['long'].mean()])
marker_cluster = MarkerCluster().add_to(mapa)
data_map = dataframe[['lat', 'long', 'id', 'price', 'bedrooms', 'bathrooms', 'floors']].copy()

for name, row in data_map.iterrows():
    folium.Marker(location=[row['lat'], row['long']], popup=f'''id: {row['id']}
    {row['price']}
    {row['bedrooms']}
    {row['bathrooms']}
    {row['floors']}''').add_to(marker_cluster)
folium_static(mapa)
