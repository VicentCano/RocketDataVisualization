import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap
import datetime

@st.cache_data
def load_data():
    ##CHANGE ROUTE
    launch_df = pd.read_csv('data/space_missions.csv', encoding='latin-1')
    launch_df['Country']=launch_df['Location'].apply(lambda row: row.split(",")[-1]).astype(str).str.strip()
    launch_df['Facility']=launch_df['Location'].apply(lambda row: row.split(",")[1]).astype(str).str.strip()

    launch_df['Date'] = pd.to_datetime(launch_df['Date'],utc=True)
    launch_df['Year'] = launch_df.Date.dt.year

    launch_df['Price'] = launch_df['Price'].astype(str).str.replace(',','').astype(float)

    # create a dictionary of country names to replace
    country_dict = {"Pacific Ocean": "International", "New Mexico": "USA", "Barents Sea": "Russia", "Yellow Sea": "China", "Gran Canaria": "USA", "Pacific Missile Range Facility": "USA", 
                    "Shahrud Missile Test Site": "Iran", "USA": "United States of America"}
    
    # use .replace() to replace the country names
    launch_df["Country"].replace(country_dict, inplace=True)
    return launch_df

def display_country_filter(country_list, default):
    return st.sidebar.selectbox('Country', country_list, index = default)

def get_line_chart(df, country):
    if country != 'Total':
        filtered_df = df[df["Country"] == country]
    else:
        filtered_df = df
    launches_per_year = filtered_df.groupby('Year').size().reset_index(name='Launches')
    launches_per_year['Year'] = launches_per_year['Year']
    st.line_chart(launches_per_year.set_index('Year'))

st.set_page_config(page_title="Launch Evolution", page_icon="🚀")
st.markdown("# Launch Evolution")
st.sidebar.header("Launch Evolution")


launch_df = load_data()

country_list = list(launch_df['Country'].unique())
country_list.append("Total")
default_value = country_list.index("Total")
country_name = display_country_filter(country_list, default_value)
get_line_chart(launch_df, country_name)




