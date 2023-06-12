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


def generate_bar(df, top):
    country_counts = launch_df.groupby('Rocket').size().reset_index(name='count')
    top_countries = country_counts.sort_values('count', ascending=False)['Rocket'].head(top)
    df_top_countries = launch_df[launch_df['Rocket'].isin(top_countries)]

    sns.set(style="darkgrid")
    sns.set_palette("hls", 8)
    ax = sns.barplot(x="Rocket", y="count", hue='Rocket', data=df_top_countries.groupby('Rocket').size().reset_index(name='count'), dodge=False, palette=sns.color_palette("hls", top))

    ax.set_title('Number of launches per rocket')
    ax.set_xlabel("Rocket")
    ax.set_xticklabels([])
    ax.set_ylabel('Number of launches')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    st.pyplot(plt)
    plt.clf()

st.set_page_config(page_title="Top X rocket models", page_icon="🚀")
st.markdown("# Top X rocket models")
st.sidebar.header("Top X rocket models")

launch_df = load_data()

value = st.slider('Select an X to create a Top X', 3, 25, 10)

generate_bar(launch_df, value)
