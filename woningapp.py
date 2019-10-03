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
st.title('Huizen verkocht in Nederland')

#%% ############# Data import ############################################
@st.cache
def load_data():
    data = pickle.load(open("woningen.pck", "rb"))
    data["Datum_akte"] = pd.to_datetime(data["Datum_akte"])
    data = data.query('Garage == "GeenGarage" ')
    return data 

data = load_data()
data = (
    data
    .query('Transactieprijs < 1000000')
    .query('Transactieprijs > 70000')
    .query('Woonoppervlak <  500')
)
soortwoningen = data.Soort_woning.unique()
soortwoningen.sort()

nofilter = st.sidebar.checkbox("Geen filter", False)
soortwoning = st.sidebar.selectbox(
    'Selecteer soort woning',
    soortwoningen
)

filtered_data_type = (
    data
    .assign(verschil = data.Transactieprijs - data.Vraagprijs )
)
filtered_data_type = (
    filtered_data_type
    .assign(perc_verschil = filtered_data_type.verschil /  filtered_data_type.Transactieprijs)
)

if not nofilter :
    filtered_data_type = filtered_data_type.query(f"Soort_woning == '{soortwoning}'")
   

filtered_data_type = (
    filtered_data_type
    .query('perc_verschil < 0.2100000')
    .query('perc_verschil > -0.2100000')
)

st.subheader('Kaart van verkochte woningen')
st.write("""
Kleur is procentueel verschil tussen verkoopprijs en vraagprijs, en grootte is gerelateerd aan de woonoppervlakte.
Dus vraagprijs 100.000 en verkoop 105.000 betekend procentueel verschil van 0.05 (5%)""")
fig = px.scatter_mapbox(
    filtered_data_type,
    lat="lat",
    lon="lon",
    color="perc_verschil", size="Woonoppervlak",
    color_continuous_scale=px.colors.cyclical.IceFire, size_max=10,  zoom=7,
    width=1100, height=800,
    hover_name=  'Type_woning'
)

st.write(fig)

#st.subheader('Prijs verdeling')
#sns.distplot(filtered_data_month_type.Vraagprijs, kde=False)
#st.pyplot()


