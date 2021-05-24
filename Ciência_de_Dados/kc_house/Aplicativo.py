# Importando bibliotecas necessárias
import streamlit as st, pandas as pd, numpy as np, folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas

@st.cache(allow_output_mutation=True)
# Lendo o arquivo para a construção do código
def get_data(path):
    read_data = pd.read_csv(path)
    return read_data


def get_geofile(url):
    read_geofile = geopandas.read_file(url)
    return read_geofile


geofile = get_geofile('https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')

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

c1.header('Mapa densidade')

df = data.sample(10)

mapa = folium.Map(
    location=[data['lat'].mean(), data['long'].mean()],
    default_zoom_start=15
)

make_cluster = MarkerCluster().add_to(mapa)
for name, row in df.iterrows():
    folium.Marker( [row['lat'], row['long']], popup=f'Price R${row["price"]} on: {row["date"]}. Features: {row["sqft_living"]} sqft, {row["bedrooms"]} bedrooms, {row["bathrooms"]} bathrooms, year built: {row["yr_built"]}' ).add_to(make_cluster)

with c1:
    folium_static(mapa)

# Região por preço
df = data[['price', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
df = df.sample(10)
geofile = geofile[geofile['ZIP'].isin(df['zipcode'].tolist())]

c2.header('Mapa Região')
mapa_regiao = folium.Map(
    location=[data['lat'].mean(), data['long'].mean()],
    zoom_start=10
)
mapa_regiao.choropleth(
    data=df,
    geo_data=geofile,
    columns=['zipcode', 'price'],
    key_on='feature.properties.ZIP',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Map prices'
)
with c2:
    folium_static(mapa_regiao)
