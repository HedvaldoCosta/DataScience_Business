# Importação das bibliotecas
import pandas as pd, numpy as np, streamlit as st, folium, geopandas, plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

st.set_page_config(layout='wide')


# Extração e transformação dos dados
@st.cache(allow_output_mutation=True)
def get_data(dataframe):
    read_path = pd.read_csv(filepath_or_buffer=dataframe)
    return read_path


@st.cache(allow_output_mutation=True)
def get_url(geofile):
    read_geofile = geopandas.read_file(filename=geofile)
    return read_geofile


@st.cache(allow_output_mutation=True)
def get_map(dataframe, datageofile):
    density_map = folium.Map(
        location=[dataframe['lat'].mean(), dataframe['long'].mean()]
    )
    price_zipcode = dataframe[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    filter_datageofile = datageofile[datageofile['ZIP'].isin(price_zipcode['zipcode'].tolist())]
    density_map.choropleth(
        data=price_zipcode,
        geo_data=filter_datageofile,
        columns=['zipcode', 'price'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd'
    )
    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in dataframe.iterrows():
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=f'''Price:R${row["price"]}
bedrooms: {row["bedrooms"]}
bathrooms: {row["bathrooms"]}
waterfront: {row["waterfront"]}'''
        ).add_to(marker_cluster)
    return density_map


data = get_data(dataframe='Datasets/kc_house_data.csv')
data_geofile = get_url(geofile='Datasets/Zip_Codes.geojson')
# Remoção das colunas desnecessárias para o insight
data = data.drop(columns=['sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'yr_renovated'])
# Formatando as colunas do data
data['date'] = pd.to_datetime(data['date']).dt.strftime('%d-%m-%Y')
data['year'] = np.int64(pd.to_datetime(data['date']).dt.strftime('%Y'))
data['age'] = data['year'] - data['yr_built']

data['bathrooms'] = np.int64(round(data['bathrooms'] - 0.3))
data['floors'] = np.int64(round(data['floors'] - 0.3))
data['sqft_living'] = round(data['sqft_living'] / 10.764, 2)
data['price'] = np.int64(data['price'])
data['level'] = data['price'].apply(
    lambda x: 0 if (x >= 0) & (x < 321950) else
    1 if (x >= 321950) & (x < 450000) else
    2 if (x >= 450000) & (x < 645000) else
    3
)
data['waterfront'] = data['waterfront'].apply(
    lambda x: 'no' if x == 0 else 'yes'
)
# Retirando as linhas que possuem idade negativa
data = data.drop(data[data['age'] < 0].index, axis=0)
st.sidebar.title(body='Filter map')
st.title(body='Dataset')
# Filtros interativos
filter_zipcode = st.sidebar.multiselect(
    label='Enter zipcode',
    options=data['zipcode'].unique()
)
filter_columns = st.sidebar.multiselect(
    label='Enter columns',
    options=data.columns
)
filter_waterfront = st.sidebar.selectbox(label='Waterfront',
                                         options=data['waterfront'].unique())
filter_price = st.sidebar.slider(label='price',
                                 min_value=75000,
                                 max_value=7700000,
                                 step=1
                                 )

if (filter_waterfront != []) & (filter_columns == []):
    data = data.loc[data['waterfront'].isin([filter_waterfront]), :]
elif (filter_waterfront != []) & (filter_columns != []):
    data = data.loc[data['waterfront'].isin([filter_waterfront]), filter_columns]
elif (filter_zipcode != []) & (filter_columns != []):
    data = data.loc[data['zipcode'].isin(filter_zipcode), filter_columns]
elif (filter_zipcode == []) & (filter_columns != []):
    data = data.loc[:, filter_columns]
elif (filter_zipcode != []) & (filter_columns == []):
    data = data.loc[data['zipcode'].isin(filter_zipcode), :]
else:
    data = data.copy()

st.dataframe(
    data=data.head()
)

c1, c2 = st.beta_columns((1, 1))

is_map = st.checkbox('map')

with c1:
    if is_map:
        folium_static(get_map(dataframe=data,
                              datageofile=data_geofile)
                      )

st.sidebar.title(body='Commerce filters')
st.title(body='Commercial')

g1, g2 = st.beta_columns((1, 1))

min_yrbuilt = int(data['yr_built'].min())
max_yrbuilt = int(data['yr_built'].max())
filter_yrbuilt = st.sidebar.slider(label='Select Year Built',
                                   min_value=min_yrbuilt,
                                   max_value=max_yrbuilt,
                                   value=min_yrbuilt
                                   )
g1.header(body='Average price for year built')
df = data.loc[data['yr_built'] <= filter_yrbuilt]
data_yrbuilt = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
fig_yrbuilt = px.line(
    data_frame=data_yrbuilt,
    x='yr_built',
    y='price'
)
g1.plotly_chart(
    figure_or_data=fig_yrbuilt,
    use_container_width=True
)

g2.header(body='Average price for day')
min_date = datetime.strptime(data['date'].min(), '%d-%m-%Y')
max_date = datetime.strptime(data['date'].max(), '%d-%m-%Y')
filter_date = st.sidebar.slider(
    label='Select Date',
    min_value=min_date,
    max_value=max_date,
    value=min_date
)
data['date'] = pd.to_datetime(data['date'])
df = data.loc[data['date'] <= filter_date]
data_date = df[['date', 'price']].groupby('date').mean().reset_index()
fig_date = px.line(
    data_frame=data_date,
    x='date',
    y='price'
)
g2.plotly_chart(
    figure_or_data=fig_date,
    use_container_width=True
)

