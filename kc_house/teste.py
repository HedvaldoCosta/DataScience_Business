# Bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px

st.set_page_config(layout='wide')


# Função para ler o dataset
@st.cache(allow_output_mutation=True)
def get_data(path):
    read_data = pd.read_csv(path)
    return read_data


data = get_data('kc_house_data.csv')
data['date'] = pd.to_datetime(data['date']).dt.strftime('%d-%m-%Y')
data['price_m2'] = data['price'] / (data['sqft_lot'] / 10.764)


# Função para ler a url geofile
@st.cache(allow_output_mutation=True)
def get_geofile(url):
    read_geofile = geopandas.read_file(url)
    return read_geofile


geofile = get_geofile('https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')

st.title(body='KC_HOUSE')
st.markdown(body='Welcome to kc house')

geral, tendencia = st.beta_columns((1, 1))

select_zipcode = st.sidebar.multiselect(
    label='Enter Zipcode',
    options=data['zipcode'].unique()
)

if select_zipcode:
    data = data.loc[data['zipcode'].isin(select_zipcode), :]
else:
    data = data.copy()


geral.header(body='Visão Geral')
geral.dataframe(
    data=data.head(10),
    height=300
)

# Estatística Descritiva
num_select = data.select_dtypes(include=['int64', 'float64'])
media = pd.DataFrame(num_select.apply(np.mean))
std = pd.DataFrame(num_select.apply(np.std))
max_value = pd.DataFrame(num_select.apply(np.max))
min_value = pd.DataFrame(num_select.apply(np.min))

dataframe_estat = pd.concat([media, std, max_value, min_value], axis=1).reset_index()
dataframe_estat.columns = ['Attributes', 'averrage', 'std', 'max', 'min']
tendencia.header(body='Tendência central')
tendencia.dataframe(
    data=dataframe_estat.head(10),
    height=300
)

