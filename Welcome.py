import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Rocket Launches Data Visualization",
        page_icon="🚀",
    )

    st.write("# Rocket Launches Data Visualization")

    st.markdown(
        """
        Welcome to Rocket Launches Data Visualization 🚀!

        In this webpage, created with streamlit, the Kaggle dataset "All Space Missions from 1957" is presented
        in a visual way.
        
        To do so numerous libraries have been used, including folium, matplotlib, pandas, seaborn, etc.

        Hope you enjoy your trip through the space! 🌌🪐👩‍🚀✨🌠
    """
    )


if __name__ == "__main__":
    run()