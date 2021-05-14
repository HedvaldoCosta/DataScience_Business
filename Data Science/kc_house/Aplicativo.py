#Importando bibliotecas necessárias
import streamlit as st, pandas as pd


@st.cache( allow_output_mutation=True )

#Lendo o arquivo para a construção do código
def get_data( path ):
    read_data = pd.read_csv( path )
    return read_data


data = get_data( 'kc_house_data.csv' )
data['date'] = pd.to_datetime( data['date'] )
data['Price m²'] = data['price'] / ( data["sqft_lot"]/10.764 )


# Visão geral dos dados
st.title('Data Overview')
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

# Medidas de tendência
count_id = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
averrage_price = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()


st.write( data.head() )

