import streamlit as st
import pandas as pd
import numpy as np
import math
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os

st.set_page_config(
    page_title="LMS Analytics",
    page_icon = ":material/oil_barrel:",
    layout="wide"
)

location_map = st.Page("pages/2_html.py", title="2D Location Map", icon=":material/map:")
wells_history = st.Page("pages/wells_history.py", title="Wells History", icon=":material/history:")
algorithmic_declinatory = st.Page("pages/algorithmic_declinatory.py", title="Algorithmic Declinatory", icon=":material/timeline:")

pg = st.navigation(
    {
        "Field Overview": [location_map, wells_history],
        "Events Cum Oil Estimation": [algorithmic_declinatory],
        # "Tools": [search, history],
    }
)

pg.run()