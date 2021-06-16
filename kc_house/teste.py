import pandas as pd, numpy as np, streamlit as st, folium, geopandas, plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


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


@st.cache(allow_output_mutation=True)
def get_map(dataframe, df_choropleth, filter_choropleth, filter1, filter2):

    if filter1:
        dataframe = dataframe.loc[dataframe['waterfront'].isin([filter_waterfront])]
    if filter2:
        dataframe = dataframe.loc[dataframe['price'] <= filter_price]
    mapa = folium.Map(
        location=[dataframe['lat'].mean(), dataframe['long'].mean()]
    )
    mapa.choropleth(
        data=df_choropleth,
        geo_data=filter_choropleth,
        columns=['zipcode', 'price'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd'
    )
    marker_cluster = MarkerCluster().add_to(mapa)
    for name, row in dataframe.iterrows():
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=f'''Price:R${row["price"]}
bedrooms: {row["bedrooms"]}
bathrooms: {row["bathrooms"]}
waterfront: {row["waterfront"]}'''
        ).add_to(marker_cluster)

    return mapa


def filter_commercial():
    st.title(body='Commerce options')
    st.sidebar.title(body='Commerce filters')

    min_yrbuilt = int(data['yr_built'].min())
    max_yrbuilt = int(data['yr_built'].max())
    filter_yrbuilt = st.sidebar.slider(label='Select Year Built',
                                       min_value=min_yrbuilt,
                                       max_value=max_yrbuilt,
                                       value=min_yrbuilt
                                       )
    st.header(body='Average price for year built')
    df1 = data.loc[data['yr_built'] <= filter_yrbuilt]
    data_yrbuilt = df1[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
    fig_yrbuilt = px.line(
        data_frame=data_yrbuilt,
        x='yr_built',
        y='price'
    )
    st.plotly_chart(
        figure_or_data=fig_yrbuilt,
        use_container_width=True
    )

    filter_bedrooms = st.sidebar.multiselect(
        label='Select bedrooms',
        options=sorted(set(data['bedrooms'].unique()))
    )
    bedrooms1, bedrooms2 = st.beta_columns((5, 5))

    bedrooms1.header(body='quantity bedrooms')
    if filter_bedrooms:
        df_bedrooms = data[data['bedrooms'].isin(filter_bedrooms)]
    else:
        df_bedrooms = data.copy()
    data_bedrooms = df_bedrooms[['bedrooms', 'id']].groupby('bedrooms').count().reset_index()
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
    data_bedrooms = df_bedrooms[['bedrooms', 'price']].groupby('bedrooms').mean().reset_index()
    fig_bedrooms = px.bar(
        data_frame=data_bedrooms,
        x='bedrooms',
        y='price'
    )
    bedrooms2.plotly_chart(
        figure_or_data=fig_bedrooms,
        use_container_width=True
    )

    filter_bathrooms = st.sidebar.multiselect(
        label='Select bathrooms',
        options=sorted(set(data['bathrooms'].unique()))
    )
    bathrooms1, bathrooms2 = st.beta_columns((3, 3))

    bathrooms1.header(body='quantity bathrooms')
    if filter_bathrooms:
        df_bathrooms = data[data['bathrooms'].isin(filter_bathrooms)]
    else:
        df_bathrooms = data.copy()
    data_bathrooms = df_bathrooms[['bathrooms', 'id']].groupby('bathrooms').count().reset_index()
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
    data_bathrooms = df_bathrooms[['bathrooms', 'price']].groupby('bathrooms').mean().reset_index()
    fig_bathrooms = px.bar(
        data_frame=data_bathrooms,
        x='bathrooms',
        y='price'
    )
    bathrooms2.plotly_chart(
        figure_or_data=fig_bathrooms,
        use_container_width=True
    )

    filter_floors = st.sidebar.multiselect(
        label='Select floors',
        options=sorted(set(data['floors'].unique()))
    )
    floor1, floor2 = st.beta_columns((3, 3))
    floor1.header(body='Quantity floors')
    if filter_floors:
        df_floors = data[data['floors'].isin(filter_floors)]
    else:
        df_floors = data.copy()
    data_floor = df_floors[['floors', 'id']].groupby('floors').count().reset_index()
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
    data_floor = df_floors[['floors', 'price']].groupby('floors').mean().reset_index()
    fig_floor = px.bar(
        data_frame=data_floor,
        x='floors',
        y='price'
    )
    floor2.plotly_chart(
        figure_or_data=fig_floor,
        use_container_width=True)


if __name__ == '__main__':
    # Lendo o dataset
    data = get_data(path='Datasets/kc_house_data.csv')
    # Lendo o geofile
    geofile = get_geofile(url='Datasets/Zip_Codes.geojson')
    # lendo o dataframe1
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
    filtros_dataset = filter_dataset(dataframe=df, filter1=filter_zipcode, filter2=filter_columns)
    st.dataframe(filtros_dataset.head())
    # lendo o mapa
    df_map = data.copy()
    st.sidebar.title(body='Filter map')
    filter_waterfront = st.sidebar.selectbox(label='Waterfront',
                                             options=df_map['waterfront'].unique())
    filter_price = st.sidebar.slider(label='price',
                                     min_value=int(df_map['price'].min()),
                                     max_value=int(df_map['price'].max()),
                                     step=1,
                                     value=int(df_map['price'].mean())
                                     )
    price_zipcode = df_map[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    filter_datageofile = geofile[geofile['ZIP'].isin(price_zipcode['zipcode'].tolist())]
    filter_mapa = get_map(dataframe=df_map, df_choropleth=price_zipcode, filter_choropleth=filter_datageofile,
                          filter1=filter_waterfront, filter2=filter_price)
    mapa1, c1 = st.beta_columns((5, 1))
    is_map = st.checkbox(label='Select map')
    with mapa1:
        if is_map:
            folium_static(filter_mapa)
    # Filtros comerciais
    filter_commercial()
