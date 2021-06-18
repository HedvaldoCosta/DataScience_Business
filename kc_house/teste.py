import pandas as pd
import streamlit as st
import numpy as np

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


# Carregar dados
read_data = load_data()

# SIDEBAR
## SIDEBAR DATASET
st.sidebar.title('Filtros da tabela')

filter_columns = st.sidebar.multiselect('Selecione as colunas', read_data.columns)
filter_cep = st.sidebar.multiselect('Selecione os CEPS', read_data['CEP'].unique().tolist())
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
## FILTROS DATASET
if (filter_cep != []) & (filter_columns != []):
    read_data = read_data.loc[read_data['CEP'].isin(filter_cep), filter_columns]
elif (filter_cep != []) & (filter_columns == []):
    read_data = read_data.loc[read_data['CEP'].isin(filter_cep), :]
elif (filter_cep == []) & (filter_columns != []):
    read_data = read_data.loc[:, filter_columns]
## FILTROS MAPA
if filter_waterfront:
    map_data = map_data.loc[map_data['beira_mar'].isin([filter_waterfront])]
elif filter_price:
    map_data = map_data.loc[map_data['preço'] <= filter_price]
## FILTROS COMERCIAIS
yr_built = read_data.loc[read_data['ano_construção'] <= filter_yr_built]
data_yr_built = yr_built[['ano_construção', 'preço']].groupby('ano_construção').mean().reset_index()

#corpo
st.title('Dataset')
if st.checkbox('Mostrar tabela com os dados'):
    st.write(read_data.head(100))

