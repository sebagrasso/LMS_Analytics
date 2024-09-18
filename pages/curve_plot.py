import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import random
import math

# @st.cache_data
wells_df_global_logs_rmn_filt = pd.read_parquet('files/wells_df_global_logs_rmn_filt')

st.header("Global Well logs plot")
st.write("_____________________")


def generate_color_list(logs, seed, alpha=1):
    random.seed(seed)  # Set seed for reproducibility
    colors = []
    for _ in logs:
        r = lambda: random.randint(0, 255)
        color = f'rgba({r()},{r()},{r()},{alpha})'
        colors.append(color)
    return colors

def plot_well_logs(df, well_name, list_logs, colors):
    df = df[df['identificador'] == well_name].reset_index(drop=True).set_index("depth")
    ncols = math.ceil(len(list_logs) / 1)
    subplot_titles = [log for log in list_logs]
    fig = make_subplots(rows=1, cols=ncols, subplot_titles=subplot_titles, shared_yaxes=True)
    
    for i, log in enumerate(list_logs):
        row = (i // ncols) + 1
        col = (i % ncols) + 1
        
        if log == "capa":
            unique_categorias = df[df[log]!=0][log].unique()
            color_map = {categoria: colors[i % len(colors)] for i, categoria in enumerate(unique_categorias)}
            
            for categoria in unique_categorias:
                subset = df[df[log] == categoria]
                fig.add_trace(
                    go.Scatter(
                        x=[categoria] * len(subset),
                        y=subset.index,
                        orientation='v',
                        name=categoria,
                        showlegend=False,
                        marker=dict(color=color_map[categoria])
                    ),
                    row=row, col=col
                )
            
            fig.update_xaxes(title_text='Capa', row=row, col=col)
        else:
            fig.add_trace(go.Scatter(x=df[log], y=df.index, name=log), row=row, col=col)
            # fig.add_trace(go.Scatter(x=df[log], y=df.index, line=dict(color='brown'), fill='tozerox', name=log), row=row, col=col)
            if "perm" in log:
                fig.update_xaxes(title_text=log, type="log", row=row, col=col)
            else:
                fig.update_xaxes(title_text=log, row=row, col=col)

    fig.update_yaxes(title_text = "DEPTH", row=1, col=1)
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title_text=well_name, title_font = dict(size=30), 
                    height=1000, 
                    # width=width, 
                      showlegend=True)
    return fig


logs=['lithology_', 'res_deep:1', 'res_shallow:1', 'sped', 'vcl', 'phie', 'sw', 'dmrperm', 'edmperm']
colors = generate_color_list(logs, seed=10, alpha=0.8)
well_options = wells_df_global_logs_rmn_filt.identificador.unique()
# well_options = wells_df_global_logs_rmn_filt[["identificador", "dmrperm", "edmperm"]].dropna(subset=["dmrperm", "edmperm"]).identificador.unique()
identificador = st.selectbox(label="Select Well", options=well_options)

fig = plot_well_logs(wells_df_global_logs_rmn_filt.dropna(subset=logs, how="all"), identificador, logs, colors)
st.plotly_chart(fig, use_container_width=True)

st.write("_____________________")
def plot_logs_dists(df, list_logs):
    nrows=1
    ncols = math.ceil(len(list_logs) / nrows)
    subplot_titles = [log for log in list_logs]
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=subplot_titles, horizontal_spacing=0.02)
    
    for i, log in enumerate(list_logs):
        row = (i // ncols) + 1
        col = (i % ncols) + 1
        # fig.add_trace(go.Histogram(x=df.loc[:,log].dropna(), nbinsx=50, opacity=0.6, name=log), row=row, col=col)
        fig.add_trace(go.Box(y=df.loc[:,log].dropna(), opacity=0.6, name=log), row=row, col=col)
        fig.update_xaxes(title_text=log, row=row, col=col)

    fig.update_layout(
                    # title_text="Logs distributions", title_font = dict(size=30), 
                    height=400,
                    margin=dict(l=0, r=0, t=20, b=10),
                    showlegend=True)
    return fig
fig2 = plot_logs_dists(wells_df_global_logs_rmn_filt[wells_df_global_logs_rmn_filt.identificador==identificador], logs)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Logs Distributions")
st.write("_____________________")
