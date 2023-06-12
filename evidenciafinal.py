# -*- coding: utf-8 -*-
"""EvidenciaFinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-rIvIpDGjuAmKgQASaLO1su7Q5a9PWFq

# **UF-6 Actividad Integradora M6**

Brenda Villa Campos A01732238
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt
from streamlit_extras.colored_header import colored_header
from streamlit_extras.chart_container import chart_container
from streamlit_extras.dataframe_explorer import dataframe_explorer
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

colored_header(
    label=":rotating_light: The Police Incident Reports from 2018 to 2020 in San Francisco :rotating_light:", 
    description = ' ',
    color_name="blue-70",
)
st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')
st.markdown('The database used for the construction of this report is presented below. Filters can be applied to the following dataframe')
df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")


mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District']= df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category']= df['Incident Category']
mapa['Incident Subcategory']= df['Incident Subcategory']
mapa['Report Type Description'] = df['Report Type Description']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
'Incident Category',
subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]
            
#subset_data

filtered_df = dataframe_explorer(subset_data, case=False)
st.dataframe(filtered_df, use_container_width=True)

st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')
st.subheader('Crime locations in San Francisco')
st.map(subset_data)

st.subheader("Crimes ocurred per day of the week")
with chart_container(subset_data):
  fig1 = px.histogram(subset_data, y='Day', color = 'Day',
                      color_discrete_sequence=["#5355B8","#82BCEB","#EDD4BE","#141785","#B87453","#EDB164","#ED9264"],
                      category_orders={"Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday","Sunday"]})
  st.plotly_chart(fig1, use_container_width=True)
    
st.subheader('Resolution status by Incident Category')
with chart_container(subset_data):
  fig2 = px.histogram(subset_data, x='Resolution', color='Incident Category', color_discrete_sequence=px.colors.qualitative.G10)
  st.plotly_chart(fig2, use_container_width=True)

st.subheader('Types of crimes committed by Police District')
with chart_container(subset_data):
  fig3 = px.histogram(subset_data, x='Incident Category', color='Police District', color_discrete_sequence=px.colors.qualitative.G10)
  st.plotly_chart(fig3, use_container_width=True)

agree = st.button('Click to see Incident Subcategories')
if agree:
  st.subheader('Subtype of crimes committed by Police District')
  fig4 = px.histogram(subset_data, x='Incident Subcategory', color='Police District', color_discrete_sequence=px.colors.qualitative.G10)
  st.plotly_chart(fig4, use_container_width=True)

st.subheader('Resolution status')
with chart_container(subset_data):
  res = subset_data['Resolution'].value_counts()
  namesRes = subset_data['Resolution'].unique()
  fig5 = px.pie(res,values ='Resolution', names = namesRes, color_discrete_sequence=["#5355B8","#82BCEB","#EDD4BE","#141785"])
  st.plotly_chart(fig5, use_container_width=True)

st.subheader('Report Type Description')
with chart_container(subset_data):
  reportType = subset_data['Report Type Description'].value_counts()
  names = subset_data['Report Type Description'].unique()
  fig6 = px.pie(reportType,values ='Report Type Description', names = names, color_discrete_sequence=["#5355B8","#82BCEB","#EDD4BE","#141785","#B87453"])
  st.plotly_chart(fig6, use_container_width=True)