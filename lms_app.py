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

wells_history = st.Page("pages/wells_history.py", title="Wells History", icon=":material/history:") ## OK 06-09
location_map = st.Page("pages/location_map.py", title="2D Location Map", icon=":material/map:") ## OK 06-09

nulls_analysis = st.Page("pages/nulls_analysis.py", title='Nulls Analysis', icon=":material/travel_explore:") ## OK 06-09

fluidos_xplots = st.Page("pages/fluidos_xplots.py", title='Fluids Xplots', icon=":material/close:") ## OK 06-09
submergence_liquid = st.Page("pages/submergence_liquid.py", title='Submergence vs Liquid', icon=":material/waves:") ## OK 06-09

allocation_production = st.Page("pages/allocation_production.py", title='Allocation vs Production', icon=":material/location_searching:") ## OK 06-09
layers_props = st.Page("pages/layers_props.py", title="Layers' Props | Prod.", icon=":material/variables:") ## OK 06-09

atemporal_db = st.Page("pages/atemporal_db.py", title='Database Analytics', icon=":material/database:") ## OK 06-09

temporal_db = st.Page("pages/temporal_db.py", title='Database Analytics', icon=":material/database:") ## OK 06-09

algorithmic_declinatory = st.Page("pages/algorithmic_declinatory.py", title="Algorithmic Declinatory", icon=":material/timeline:") ## OK 06-09
# estimation_vs_np = st.Page("pages/estimation_prorrat_hk_vs_np_hk.py", title='Espesor Punzado vs Estimacion prorrateada', icon=":material/water_drop:")
npevent_nph_npfc_vs_np_hk_io = st.Page("pages/npevent_nph_npfc_vs_np_hk_io.py", title='Np-EUR Estimation vs Reservoir Properties', icon=":material/water_drop:") ## OK 12-09

pg = st.navigation(
    {
        "Field Overview": [wells_history, location_map],
        "Logs": [nulls_analysis],
        "Controls vs Production": [fluidos_xplots, submergence_liquid],
        "Layers": [allocation_production, layers_props],
        "Atemporal Data": [atemporal_db],
        "Temporal Data": [temporal_db],
        "Events Cum Oil Estimation": [algorithmic_declinatory, npevent_nph_npfc_vs_np_hk_io],
    }
)

pg.run()