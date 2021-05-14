# Importando bibliotecas necessárias
import streamlit as st, pandas as pd


@st.cache( allow_output_mutation=True )
# Lendo o arquivo para a construção do código
def get_data( path ):
    read_data = pd.read_csv( path )
    return read_data


data = get_data( 'kc_house_data.csv' )
data['date'] = pd.to_datetime( data['date'] )
data['Price_m²'] = data['price'] / ( data["sqft_lot"]/10.764 )

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

if ( select_columns != [] ) & ( select_zipcode != [] ):
    data = data.loc[data['zipcode'].isin(select_zipcode), select_columns]
elif ( select_columns == [] ) & ( select_zipcode != [] ):
    data = data.loc[data['zipcode'].isin(select_zipcode), :]
elif (select_columns != []) & ( select_zipcode == [] ):
    data = data.loc[:, select_columns]
else:
    data = data.copy()

st.header(body='Visão geral')
st.dataframe(
    data=data,
    height=300
)

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
st.header(body='Medidas de tendência')
st.dataframe(
    data=data,
    height=300
)