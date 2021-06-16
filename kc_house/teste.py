import pandas as pd, numpy as np, streamlit as st, folium, geopandas, plotly.express as px


@st.cache(allow_output_mutation=True)
def get_data(path):
    read_data = pd.read_csv(path)
    read_data = read_data.drop(columns=['sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'yr_renovated'])

    read_data['date'] = pd.to_datetime(read_data['date']).dt.strftime('%d-%m-%Y')
    read_data['year'] = np.int64(pd.to_datetime(read_data['date']).dt.strftime('%Y'))
    read_data['age'] = read_data['year'] - read_data['yr_built']

    read_data['bathrooms'] = np.int64(round(read_data['bathrooms'] - 0.3))
    read_data['floors'] = np.int64(round(read_data['floors'] - 0.3))
    read_data['sqft_living'] = round(read_data['sqft_living'] / 10.764, 2)
    read_data['price'] = np.int64(read_data['price'])
    read_data['level'] = read_data['price'].apply(
        lambda x: 0 if (x >= 0) & (x < 321950) else
        1 if (x >= 321950) & (x < 450000) else
        2 if (x >= 450000) & (x < 645000) else
        3
    )
    read_data['waterfront'] = read_data['waterfront'].apply(
        lambda x: 'no' if x == 0 else 'yes'
    )
    read_data = read_data.drop(read_data[read_data['age'] < 0].index, axis=0)
    return read_data


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    read_geofile = geopandas.read_file(url)
    return read_geofile


@st.cache(allow_output_mutation=True)
def filter_dataset(dataframe, filter1, filter2):

    if (filter1 != []) & (filter2 != []):
        dataframe = dataframe.loc[dataframe['zipcode'].isin(filter_zipcode), filter_columns]
    elif (filter1 != []) & (filter2 == []):
        dataframe = dataframe.loc[dataframe['zipcode'].isin(filter_zipcode), :]
    elif (filter1 == []) & (filter2 != []):
        dataframe = dataframe.loc[:, filter_columns]
    else:
        dataframe = dataframe.copy()

    return dataframe


if __name__ == '__main__':
    data = get_data(path='Datasets/kc_house_data.csv')

    geofile = get_geofile(url='Datasets/Zip_Codes.geojson')

    df = data.copy()
    st.sidebar.title(body='Filter Dataset')
    st.title(body='Dataset')
    filter_zipcode = st.sidebar.multiselect(
        label='Select Zipcode',
        options=df['zipcode'].unique()
    )
    filter_columns = st.sidebar.multiselect(
        label='Enter columns',
        options=df.columns
    )
    filtros = filter_dataset(dataframe=df, filter1=filter_zipcode, filter2=filter_columns)
    st.dataframe(filtros.head())
