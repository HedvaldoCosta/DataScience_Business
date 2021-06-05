# Importação das bibliotecas
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout='wide')


# Extração e transformação dos dados
def get_data(path):
    read_path = pd.read_csv(path)
    return read_path


data = get_data('Datasets/kc_house_data.csv')
# Remoção das colunas desnecessárias para o insight
data = data.drop(columns=['sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'yr_renovated'])
# Formatando colunas de tempo
data['date'] = pd.to_datetime(data['date']).dt.strftime('%d-%m-%Y')
data['year'] = np.int64(pd.to_datetime(data['date']).dt.strftime('%Y'))
data['age'] = data['year'] - data['yr_built']

# Formatando o tipo das colunas
data['bathrooms'] = np.int64(round(data['bathrooms'] - 0.3))
data['floors'] = np.int64(round(data['floors'] - 0.3))
data['sqft_living'] = round(data['sqft_living'] / 10.764, 2)

data['level'] = data['price'].apply(
    lambda x: 0 if (x >= 0) & (x < 321950) else
    1 if (x >= 321950) & (x < 450000) else
    2 if (x >= 450000) & (x < 645000) else
    3
)

data['waterfront'] = data['waterfront'].apply(lambda x: 'no' if x == 0 else 'yes')

data = data.drop(data[data['age'] < 0].index, axis=0)
st.write(data.head())
