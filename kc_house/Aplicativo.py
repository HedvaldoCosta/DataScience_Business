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

data = data.drop(columns=['sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'yr_renovated'])

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
data = data.drop(data[data['age'] < 0].index, axis=0)

# Filtros Dataset
st.sidebar.title(body='Filter Dataset')
st.title(body='Dataset')

dataset = data.copy()
filter_zipcode = st.sidebar.multiselect(
    label='Enter zipcode',
    options=dataset['zipcode'].unique()
)
filter_columns = st.sidebar.multiselect(
    label='Enter columns',
    options=dataset.columns
)

if (filter_zipcode != []) & (filter_columns != []):
    dataset = dataset.loc[dataset['zipcode'].isin(filter_zipcode), filter_columns]
elif (filter_zipcode != []) & (filter_columns == []):
    dataset = dataset.loc[dataset['zipcode'].isin(filter_zipcode), :]
elif (filter_zipcode == []) & (filter_columns != []):
    dataset = dataset.loc[:, filter_columns]
else:
    dataset = dataset.copy()

st.dataframe(data=dataset)

# Filtros do mapa
data_map = data.copy()
st.sidebar.title(body='Filter Map')
filter_waterfront = st.sidebar.selectbox(label='Waterfront',
                                         options=data_map['waterfront'].unique())
filter_price = st.sidebar.slider(label='price',
                                 min_value=int(data_map['price'].min()),
                                 max_value=int(data_map['price'].max()),
                                 step=1,
                                 value=int(data_map['price'].mean())
                                 )
if filter_waterfront:
    data_map = data_map.loc[data_map['waterfront'].isin([filter_waterfront])]
if filter_price:
    data_map = data_map.loc[data_map['price'] <= filter_price]
mapa1, c2 = st.beta_columns((4, 1))
is_map = st.checkbox('map')
with mapa1:
    if is_map:
        folium_static(
            get_map(dataframe=data_map,
                    datageofile=data_geofile)
        )

st.sidebar.title(body='Commerce filters')
st.title(body='Commercial')

g1, g2 = st.beta_columns((3, 3))

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

st.title(body='House attributes')
st.sidebar.title(body='House filters')
# Filters
filter_bedrooms = st.sidebar.multiselect(
    label='Select bedrooms',
    options=sorted(set(data['bedrooms'].unique()))
)
filter_bathrooms = st.sidebar.multiselect(
    label='Select bathrooms',
    options=sorted(set(data['bathrooms'].unique()))
)
filter_floors = st.sidebar.multiselect(
    label='Select floors',
    options=sorted(set(data['floors'].unique()))
)
bedrooms1, bedrooms2 = st.beta_columns((3, 3))

bedrooms1.header(body='quantity bedrooms')
if filter_bedrooms:
    df = data[data['bedrooms'].isin(filter_bedrooms)]
else:
    df = data.copy()
data_bedrooms = df[['bedrooms', 'id']].groupby('bedrooms').count().reset_index()
data_bedrooms.columns = ['bedrooms', 'quantity']
fig_bedrooms = px.bar(
    data_frame=data_bedrooms,
    x='bedrooms',
    y='quantity'
)
bedrooms1.plotly_chart(
    figure_or_data=fig_bedrooms,
    use_container_width=True
)

bedrooms2.header(body='Mean price bedrooms')
data_bedrooms = df[['bedrooms', 'price']].groupby('bedrooms').mean().reset_index()
fig_bedrooms = px.bar(
    data_frame=data_bedrooms,
    x='bedrooms',
    y='price'
)
bedrooms2.plotly_chart(
    figure_or_data=fig_bedrooms,
    use_container_width=True
)

bathrooms1, bathrooms2 = st.beta_columns((3, 3))

bathrooms1.header(body='quantity bathrooms')
if filter_bathrooms:
    df = data[data['bathrooms'].isin(filter_bathrooms)]
else:
    df = data.copy()
data_bathrooms = df[['bathrooms', 'id']].groupby('bathrooms').count().reset_index()
data_bathrooms.columns = ['bathrooms', 'quantity']
fig_bathrooms = px.bar(
    data_frame=data_bathrooms,
    x='bathrooms',
    y='quantity'
)
bathrooms1.plotly_chart(
    figure_or_data=fig_bathrooms,
    use_container_width=True
)
bathrooms2.header(body='Mean price bathrooms')
data_bathrooms = df[['bathrooms', 'price']].groupby('bathrooms').mean().reset_index()
fig_bathrooms = px.bar(
    data_frame=data_bathrooms,
    x='bathrooms',
    y='price'
)
bathrooms2.plotly_chart(
    figure_or_data=fig_bathrooms,
    use_container_width=True
)

floor1, floor2 = st.beta_columns((3, 3))
floor1.header(body='Quantity floors')
if filter_floors:
    df = data[data['floors'].isin(filter_floors)]
else:
    df = data.copy()
data_floor = df[['floors', 'id']].groupby('floors').count().reset_index()
data_floor.columns = ['floors', 'Quantity']
fig_floor = px.bar(
    data_frame=data_floor,
    x='floors',
    y='Quantity'
)
floor1.plotly_chart(
    figure_or_data=fig_floor,
    use_container_width=True
)
floor2.header(body='Mean price floors')
data_floor = df[['floors', 'price']].groupby('floors').mean().reset_index()
fig_floor = px.bar(
    data_frame=data_floor,
    x='floors',
    y='price'
)
floor2.plotly_chart(
    figure_or_data=fig_floor,
    use_container_width=True)
