# Importando bibliotecas necessárias
import streamlit as st, pandas as pd, numpy as np, folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

@st.cache(allow_output_mutation=True)
# Lendo o arquivo para a construção do código
def get_data(path):
    read_data = pd.read_csv(path)
    return read_data


data = get_data('kc_house_data.csv')
data['date'] = pd.to_datetime(data['date'])
data['Price_m²'] = data['price'] / (data["sqft_lot"] / 10.764)

# Visão geral dos dados
st.title('KC HOUSE ANÁLISE')
st.markdown('Bem-vindo ao kc house')
select_columns = st.sidebar.multiselect(
    label='Enter Columns',
    options=data.columns
)
select_zipcode = st.sidebar.multiselect(
    label='Enter Zipcode',
    options=data['zipcode'].unique()
)

if (select_columns != []) & (select_zipcode != []):
    data = data.loc[data['zipcode'].isin(select_zipcode), select_columns]
elif (select_columns == []) & (select_zipcode != []):
    data = data.loc[data['zipcode'].isin(select_zipcode), :]
elif (select_columns != []) & (select_zipcode == []):
    data = data.loc[:, select_columns]
else:
    data = data.copy()

st.header(body='Visão geral')
st.dataframe(
    data=data.head(10),
    height=300
)
data_averrage, data_statistc = st.beta_columns((1, 1))

# Medidas de tendência
count_id = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
averrage_price = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
averrage_sqft = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
averrage_price_m2 = data[['Price_m²', 'zipcode']].groupby('zipcode').mean().reset_index()

# Fusão das medidas
merge1 = pd.merge(
    left=count_id,
    right=averrage_price,
    how="inner",
    on='zipcode'
)
merge2 = pd.merge(
    left=merge1,
    right=averrage_sqft,
    how="inner",
    on='zipcode'
)
merge3 = pd.merge(
    left=merge2,
    right=averrage_price_m2,
    how="inner",
    on='zipcode'
)
data_averrage.header(body='Medidas de tendência')
data_averrage.dataframe(
                        data=merge3.head(10),
                        height=300
                        )

# Estatística Descritiva
num_select = data.select_dtypes(include=['int64', 'float64'])
media = pd.DataFrame(num_select.apply(np.mean))
mediana = pd.DataFrame(num_select.apply(np.median))
std = pd.DataFrame(num_select.apply(np.std))
max_value = pd.DataFrame(num_select.apply(np.max))
min_value = pd.DataFrame(num_select.apply(np.min))

dataframe_estat = pd.concat([media, mediana, std, max_value, min_value], axis=1).reset_index()
dataframe_estat.columns = ['Attributes', 'averrage', 'median', 'std', 'max', 'min']

data_statistc.header(body='Estatística Descritiva')
data_statistc.dataframe(
                        data=dataframe_estat.head(10),
                        height=300
                        )

# Densidade de portfolio
c1, c2 = st.beta_columns((1, 1))
df = data.sample(10)
mapa = folium.Map(
    location=[data['lat'].mean(), data['long'].mean()],
    zoom_start=10
)

make_cluster = MarkerCluster().add_to(parent=mapa)
for name, row in df.iterrows():
    folium.Marker( [row['lat'], row['long']], popup=f'Price R${row["price"]} on: {row["date"]}. Features: {row["sqft_living"]} sqft, {row["bedrooms"]} bedrooms, {row["bathrooms"]} bathrooms, year built: {row["yr_built"]}' ).add_to(make_cluster)

with c1:
    folium_static(mapa)
