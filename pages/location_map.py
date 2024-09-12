import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os
import streamlit.components.v1 as components

st.header("2D Locaton Map")
st.write("_____________________")

plot_file = open('files/1_well_location.html','r', encoding='utf-8')
plot = plot_file.read()

# st.markdown(plot,unsafe_allow_html=True)
components.html(plot, scrolling=True, 
                width=1500, 
                height=1300
                )


### CHART WAY. MORE SLOWLY TO LOAD
# @st.cache_data
# def load_pickle(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, "rb") as f:
#             return pickle.load(f)
#     else:
#         st.error(f"File not found: {file_path}")
#         return None
# wells_df = load_pickle("files/wells_df")
# produccion = load_pickle("files/produccion")

# inyectores=produccion[produccion["qwi_[m3/dc]"]>0].identificador.unique()
# wells_df["type"] = np.where(wells_df.identificador.isin(inyectores), "inyector", "productor")

# st.header("2D Locaton Map")
# st.write("_____________________")

# df = wells_df[(wells_df.x!=0) & (wells_df.y!=0)]

# fig = px.scatter(df, x='x', y='y', color='type', hover_data=['identificador'], color_discrete_map={'inyector': 'aqua', 'productor': 'forestgreen'})
# fig.update_layout(
#     title='Wells Location',
#     scene=dict(
#         xaxis_title='X Coordinate',
#         yaxis_title='Y Coordinate',
#         zaxis_title='Depth',
#         camera=dict(projection=dict(type='orthographic')),
#         zaxis=dict(
#             autorange='reversed'
#         ),
#         aspectratio=dict(x=1, y=1, z=0.8),
#         bgcolor='lightgray'
#     ),
#     height=800,
# )
# for well_name in df.sort_values(by="identificador", ascending=True).identificador.unique():
#     well_data = df[df['identificador'] == well_name]
#     fig.add_trace(go.Scatter(
#         x=[well_data['x'].mean()], y=[well_data['y'].mean()+100],
#         mode='text',
#         text=well_name,
#         textposition="top center",
#         textfont=dict(size=10, color='gray'),
#         showlegend=False
#     ))
       
# fig.update_traces(marker=dict(size=10))

# st.plotly_chart(fig)