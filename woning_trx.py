#%% ############# imports ##############################################
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

import seaborn as sns
import plotly.express as px

## plotly express uses mapbox for map plots, you need a token https://docs.mapbox.com/help/how-mapbox-works/access-tokens/
px.set_mapbox_access_token(open(".mapbox_token").read())

#%% ############  streamlit app  #############################################
st.title('Huizen verkocht NL. .....')

woontype = st.sidebar.selectbox(
    'Selecteer huis type',
     ['Eengezinswoning', 'Grachtenpand', 'Herenhuis', 'Villa', 'Bungalow', 
     'Landhuis', 'Woonboerderij', 'Stacaravan','Landgoed', 'Woonboot', 'Woonwagen']
)

verschil = st.sidebar.checkbox("verschil")

#%% ############# Data import ############################################
@st.cache
def load_data():
    data = pickle.load(open("woningen.pck", "rb"))
    data["Datum_akte"] = pd.to_datetime(data["Datum_akte"])
    data = data.query('Garage == "GeenGarage" ')
    return data 

data = load_data()

filtered_data_type = (
    data
    .assign(verschil = data.Vraagprijs - data.Transactieprijs)
    .query(f"Soort_woning == '{woontype}'")
    .query('Transactieprijs < 1000000')
    .query('Transactieprijs > 70000')
)
filtered_data_type = (
    filtered_data_type
    .query('verschil < 100000')
    .query('verschil > -100000')
)

st.subheader('Woningen van type %s per maand' % woontype)
hist_values = np.histogram(filtered_data_type["Datum_akte"].dt.month, bins=12, range=(0,12))[0]
st.bar_chart(hist_values)

#month_to_filter = st.sidebar.selectbox('selecteer een maand', [1,2,3,4,5,6,7,8,9,10,11,12])
#filtered_data_month_type = filtered_data_type[filtered_data_type["Datum_akte"].dt.month == month_to_filter]
#filtered_data_month_type = filtered_data_month_type.dropna(subset = ["lat","lon"])

if verschil :
    colorvar = "verschil"
else :
    colorvar = "Transactieprijs"
st.subheader('Kaart van alle woningen verkocht')
fig = px.scatter_mapbox(
    filtered_data_type,
     lat="lat",
     lon="lon",
     color=colorvar, size="Woonoppervlak",
     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=7,
     width=1000, height=800,
     hover_name=  'Type_woning'
)
st.write(fig)

#st.subheader('Prijs verdeling')
#sns.distplot(filtered_data_month_type.Vraagprijs, kde=False)
#st.pyplot()


