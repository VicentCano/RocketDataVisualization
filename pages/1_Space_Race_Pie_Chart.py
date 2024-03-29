import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap

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


def generate_pie(df, lower_bound, upper_bound):
    grouped_un = df.groupby('Country').size().reset_index(name='counts')
    grouped_un = grouped_un.sort_values(by='counts', ascending=False)

    filtered_df = df[(df['Year'] >= lower_bound) & (df['Year'] <= upper_bound)]
    grouped = filtered_df.groupby('Country').size().reset_index(name='counts')
    grouped = grouped.sort_values(by='counts', ascending=False)
    sns.set_style('darkgrid')
    pallette_dict = {}
    for country, color in zip(grouped_un['Country'].unique(), sns.color_palette("hls", 17).as_hex()):
        pallette_dict[country] = color
    fig, ax = plt.pie(grouped['counts'], colors=[pallette_dict.get(country, 'gray') for country in grouped['Country']])
    plt.title('Launches by Country')

    plt.legend(labels=grouped['Country'], loc='center left', bbox_to_anchor=(1, 0.5))

    st.pyplot(plt)
    #plt.savefig("/home/vicent/miarfid/pid/graphs2/launches_by_country.svg", bbox_inches='tight')
    plt.clf()

def generate_pie_company(df, lower_bound, upper_bound):
    grouped_un = df.groupby('Company').size().reset_index(name='counts')
    grouped_un = grouped_un.sort_values(by='counts', ascending=False)

    filtered_df = df[(df['Year'] >= lower_bound) & (df['Year'] <= upper_bound)]
    grouped = filtered_df.groupby('Company').size().reset_index(name='counts')
    grouped = grouped.sort_values(by='counts', ascending=False)

    top5 = grouped.head(30)
    sns.set_style('darkgrid')
    sns.set_palette(sns.color_palette("hls", 30))
    fig, ax = plt.pie(grouped['counts'])
    plt.title('Launches by Company')

    plt.legend(labels=top5['Company'], loc='center left', bbox_to_anchor=(1, 0.5),ncol=2)

    st.pyplot(plt)
    #plt.savefig("/home/vicent/miarfid/pid/graphs2/launches_by_country.svg", bbox_inches='tight')
    plt.clf()

st.set_page_config(page_title="Space Race Pie Charts", page_icon="🚀")
st.markdown("""# Space Race visualized in Pie Charts

Choose a range to show how the number of launches was split across different countries and companies!
""")

values = st.slider('Select a range of values', 1957, 2022, (1957, 2022))

launch_df = load_data()
generate_pie(launch_df, values[0], values[1])
generate_pie_company(launch_df, values[0], values[1])

st.write("Note that in the country pie chart the colors have been fixed to specific countries for clarity purpose. This was possible due to the small number of countries and its steadyness. This is not the case for the companies pie chart, which has varying color legends for each range, since there ia a huge number of companies and they vary a lot through the years.")



