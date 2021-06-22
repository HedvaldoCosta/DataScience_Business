import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

data = 'Datasets/kc_house_data.csv'


@st.cache
def load_data():
    """
    Carrega os dados dos imóveis

    :return: Dataframe com as colunas já limpas
    """
    columns = {
        'id': 'ID',
        'date': 'data',
        'price': 'preço',
        'bedrooms': 'quartos',
        'bathrooms': 'banheiros',
        'sqft_living': 'area M2',
        'floors': 'andares',
        'waterfront': 'beira_mar',
        'yr_built': 'ano_construção',
        'zipcode': 'CEP',
        'lat': 'latitude',
        'long': 'longitude',
        'level': 'level',
        'idade': 'idade'
    }
    dataframe = pd.read_csv(data)
    dataframe = dataframe.rename(columns=columns)

    dataframe['data'] = pd.to_datetime(dataframe['data']).dt.strftime('%d-%m-%Y')
    dataframe['banheiros'] = np.int64(round(dataframe['banheiros'] - 0.3))
    dataframe['andares'] = np.int64(round(dataframe['andares'] - 0.3))
    dataframe['beira_mar'] = dataframe['beira_mar'].apply(lambda x: 'SIM' if x == 1 else 'NÃO')
    dataframe['level'] = dataframe['preço'].apply(lambda x: 1 if (x >= 75000) & (x < 321950) else
                                                            2 if (x >= 321950) & (x < 568900) else
                                                            3 if (x >= 568900) & (x < 815850) else
                                                            4 if (x >= 815850) & (x < 1062800) else
                                                            5)
    dataframe['ano'] = np.int64(pd.to_datetime(dataframe['data']).dt.strftime('%Y'))
    dataframe['idade'] = dataframe['ano'] - dataframe['ano_construção']
    dataframe = dataframe[list(columns.values())]

    return dataframe


def load_map(data_map):
    """
    :param data_map: Dataset que irá filtrar as informações do mapa
    :return: Mapa com os filtros
    """
    mapa = folium.Map(location=[data_map['latitude'].mean(), data_map['longitude'].mean()])
    marker_cluster = MarkerCluster().add_to(mapa)
    for name, row in data_map.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']],
                      popup=f'''ID: {row["ID"]}
preço: {row["preço"]}
quartos: {row["quartos"]}
banheiros: {row["banheiros"]}
andares: {row["andares"]}
area: {row["area M2"]}
idade: {row["idade"]}
''').add_to(marker_cluster)

    return folium_static(mapa)


# Carregar dados
read_data = load_data()

# SIDEBAR
## SIDEBAR DATASET
df_data = read_data.copy()
st.sidebar.title('Filtros da tabela')
filter_columns = st.sidebar.multiselect('Selecione as colunas', df_data.columns)
filter_cep = st.sidebar.multiselect('Selecione os CEPS', df_data['CEP'].unique().tolist())
## SIDEBAR MAPA
map_data = read_data.copy()
st.sidebar.title('Filtros do mapa')
filter_waterfront = st.sidebar.selectbox('Beira-Mar', map_data['beira_mar'].unique().tolist())
filter_price = st.sidebar.slider('Preço', int(map_data['preço'].min()), int(map_data['preço'].max()),
                                 int(map_data['preço'].mean()))
## SIDEBAR COMERCIAL
commercial_data = read_data.copy()
st.sidebar.title('Filtros comerciais')
filter_yr_built = st.sidebar.slider('Ano de construção', int(commercial_data['ano_construção'].min()),
                                    int(commercial_data['ano_construção'].max()),
                                    int(commercial_data['ano_construção'].mean()))
filter_bedrooms = st.sidebar.multiselect('Quartos', sorted(set(commercial_data['quartos'].unique().tolist())))
filter_bathrooms = st.sidebar.multiselect('Banheiros', sorted(set(commercial_data['banheiros'].unique().tolist())))
filter_floors = st.sidebar.multiselect('Andares', sorted(set(commercial_data['andares'].unique().tolist())))

# APLICAÇÃO DOS FILTROS
## FILTROS MAPA
if filter_waterfront:
    map_data = map_data.loc[map_data['beira_mar'].isin([filter_waterfront])]
elif filter_price:
    map_data = map_data.loc[map_data['preço'] <= filter_price]
## FILTROS DATASET
if (filter_cep != []) & (filter_columns != []):
    df_data = df_data.loc[df_data['CEP'].isin(filter_cep), filter_columns]
elif (filter_cep != []) & (filter_columns == []):
    df_data = df_data.loc[df_data['CEP'].isin(filter_cep), :]
elif (filter_cep == []) & (filter_columns != []):
    df_data = df_data.loc[:, filter_columns]
## FILTROS COMERCIAIS
df_yrbuilt = read_data.copy()
yr_built = df_yrbuilt.loc[df_yrbuilt['ano_construção'] <= filter_yr_built]
data_yr_built = yr_built[['ano_construção', 'preço']].groupby('ano_construção').mean().reset_index()
fig_yr_built = px.line(data_yr_built, x='ano_construção', y='preço')

df_bedrooms = read_data.copy()
if filter_bedrooms:
    df_bedrooms = df_bedrooms.loc[read_data['quartos'].isin(filter_bedrooms)]
data_bedrooms_price = df_bedrooms[['preço', 'quartos']].groupby('quartos').mean().reset_index()
data_bedrooms_count = df_bedrooms[['ID', 'quartos']].groupby('quartos').count().reset_index()
data_bedrooms_count.columns = ['quartos', 'qtd']
fig_bedrooms_mean = px.bar(data_bedrooms_price, x='quartos', y='preço')
fig_bedrooms_count = px.bar(data_bedrooms_count, x='quartos', y='qtd')

df_bathrooms = read_data.copy()
if filter_bathrooms:
    df_bathrooms = df_bathrooms.loc[read_data['banheiros'].isin(filter_bathrooms)]
data_bathrooms_mean = df_bathrooms[['preço', 'banheiros']].groupby('banheiros').mean().reset_index()
data_bathrooms_count = df_bathrooms[['ID', 'banheiros']].groupby('banheiros').count().reset_index()
data_bathrooms_count.columns = ['banheiros', 'qtd']
fig_bathrooms_mean = px.bar(data_bathrooms_mean, x='banheiros', y='preço')
fig_bathrooms_count = px.bar(data_bathrooms_count, x='banheiros', y='qtd')

df_floors = read_data.copy()
if filter_floors:
    df_floors = df_floors.loc[read_data['andares'].isin(filter_floors)]
data_floors_mean = df_floors[['preço', 'andares']].groupby('andares').mean().reset_index()
data_floors_count = df_floors[['ID', 'andares']].groupby('andares').count().reset_index()
data_floors_count.columns = ['andares', 'qtd']
fig_floors_mean = px.bar(data_floors_mean, x='andares', y='preço')
fig_floors_count = px.bar(data_floors_count, x='andares', y='qtd')
# CORPO
st.title('Dataset')
if st.checkbox('Mostrar tabela com os dados'):
    st.write(df_data.head(100))

load_map(map_data)

st.title('Área comercial')
st.plotly_chart(fig_yr_built)

bedrooms1, bedrooms2 = st.beta_columns((1, 1))
bedrooms1.plotly_chart(fig_bedrooms_mean, use_container_width=True)
bedrooms2.plotly_chart(fig_bedrooms_count, use_container_width=True)

bathrooms1, bathrooms2 = st.beta_columns((1, 1))
bathrooms1.plotly_chart(fig_bathrooms_mean, use_container_width=True)
bathrooms2.plotly_chart(fig_bathrooms_count, use_container_width=True)

floors1, floors2 = st.beta_columns((1, 1))
floors1.plotly_chart(fig_floors_mean, use_container_width=True)
floors2.plotly_chart(fig_floors_count, use_container_width=True)

