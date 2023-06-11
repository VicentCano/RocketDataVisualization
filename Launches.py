# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import folium
from streamlit_folium import st_folium

LOGGER = get_logger(__name__)
APP_TITLE = 'Launches by country'

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

def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('Year', year_list, 0)
    st.header(f'{year}' )
    return year

def display_country_filter(country_list):
    return st.sidebar.selectbox('Country', country_list)

@st.cache_data
def get_total_price_and_count(df):
    grouped_df = df.groupby('Country').agg(Price=('Price', 'sum'), count=('Country', 'count'))
    return grouped_df.reset_index()

def display_map(df, year, countries_geo):
    df = df[(df['Year'] == year)]

    m = folium.Map(location=[40,  0], zoom_start=1.4)
    country_counts = get_total_price_and_count(df)
    coropletas = folium.Choropleth(geo_data=countries_geo,name="choropleth",data=country_counts,columns=["Country", "count"],key_on="properties.ADMIN", fill_color="BuPu",fill_opacity=0.7,line_opacity=1.0,legend_name="Number of launches")
    coropletas.add_to(m)
    coropletas.geojson.add_child(folium.features.GeoJsonTooltip(['ADMIN'], labels=False))
    
    folium.LayerControl().add_to(m)
    st_folium(m, width=700, height=450,  returned_objects=[])

def run():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🚀",
    )
    
    launch_df = load_data()
    countries_geo = 'countries.geojson'
    st.write("# " + APP_TITLE)

    country_list = list(launch_df['Country'].unique())

    

    country_name = display_country_filter(country_list)
    year = display_time_filters(launch_df)
    display_map(launch_df, year, countries_geo)

    #Display Metrics


    
    if country_name != '00':
        st.subheader(f'Launch statistics: {country_name} {year}')  
        df_year = launch_df[(launch_df['Year'] == year)]
        if country_name in df_year['Country'].unique():
            country_stats = get_total_price_and_count(df_year)
            n_launches = country_stats[country_stats['Country'] == country_name]['count']
            p_launches = country_stats[country_stats['Country'] == country_name]['Price']
        else:
            n_launches = 0
            p_launches = 0
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Number of launches', n_launches)
        with col2:
            st.metric('Cost of launches*', str(round(float(p_launches),2)) + " million $" )
        
        st.write("*Many countries don't share the price of their launches, this statistic is based SOLELY on the sum of available data, so, in general, the real cost of launches tends to be bigger.")
if __name__ == "__main__":
    run()
